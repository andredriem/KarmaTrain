# -*- coding: utf-8 -*-
"""
This module provides the user a diverse set of tools for gathering statistical karma data from a
specific subreddit or submission. It generates files containing several json elements. The first json
contains information about the thread, the following contain karma data over time. Each file is
identified by it's submission ID. The files are stored in the folder you are currently working with.
All classes in this module works using threading and multiprocessing (TODO) so be careful when using.
Examples:
    As a module:
    
    To generate gather data file (see data folder) from a specific post over time:
    $ python
    $ import data_gatherer
    $ your_submission = data_gatherer.SubmissionGather("INSERT SUBMISSION PERMALINK HERE",2,20)
    $ your_submission.watch()
    $ #This will gather karma data from the your submission for the next 2h checking the thread
    $ #for changes every 20 seconds.
    
    
    To generate gather data file (see data folder) from a specific subreddit over time:
    $ python
    $ import data_gatherer
    $ subreddit = data_gatherer.SubredditGather('circlejerk',500,24,20)
    $ subreddit.watch()
    $ #This will gather karma data for the next 500 submissions from /r/circlejerk for the next 24h
    $ #checking each thread for changes every 20 seconds.   
    
    Calling the application with command-line arguments like this will produce the same results:
    % python data_gatherer.py circlejerk 500 24 20
    *be careful that this module does not check for input consistency TODO
    
Todo:
    *Integrate with db_management
    *Multiprocessing support at __newSubmissionWatcher__ and see if I can make that fucking spaghetti more
    readable
    *consistency check at command-line calls
"""

import sys
import praw
import json
import time
import threading

r = praw.Reddit('Submission data gatherer')


class SubmissionGather:
    """
    This class is used to gather karma data from a specific submission
    """

    def __init__(self, permalink, analysis_time, analysis_delay):
        """
        Args:
            permalink (str): url (permalink) of submission.
            analysis_time (float): Time in hours the function should watch the thread
            analysis_delay (float): TIme in seconds indicating the delay to gather data
        """
        self.permalink = permalink
        self.analysis_time = analysis_time
        self.analysis_delay = analysis_delay

        self.watch_thread = None
        now = time.time()
        self.deadline = now + (self.analysis_time * 3600.0)
        self.watch_thread = threading.Thread(target=self._periodic_update, args=(self.deadline, self.analysis_delay))
        self._file_init()

    def update(self):
        """
        Forces an update in submission file
        """
        submission = r.get_submission(self.permalink)
        s_dic = {'ups': submission.ups, 'ratio': submission.upvote_ratio, 'computer_time': time.time(),
                 'num_comments': submission.num_comments}

        self._save(submission.id, s_dic, 'a')
        pass

    def watch(self):
        """
        Keep checking thread until analysis_time ends
        """

        now = time.time()
        self.deadline = now + (self.analysis_time * 3600.0)
        self.watch_thread = threading.Thread(target=self._periodic_update, args=(self.deadline, self.analysis_delay))
        self.watch_thread.start()
        pass

    def thread_status(self):
        """
        Checks class threads status
        
        Returns:
            True if a thread called by this class is running, False otherwise
        """
        if isinstance(self.watch_thread, None):
            return False
        else:
            return self.watch_thread.isAlive()

    def _periodic_update(self, deadline, delay):
        """
        For devs only:
            Since this function will be executing for a long time and reddit servers can go down at any time
            this function will need a proper error handling.
        """
        try:
            while time.time() <= deadline:
                self.update()
                time.sleep(delay)
        except AttributeError:
            # This error is caused by multiple requests of reddit api
            pass
        pass

    def _file_init(self):
        submission = r.get_submission(self.permalink)
        s_dic = {'title': submission.title, 'selftext': submission.selftext, 'id': submission.id,
                 'permalink': self.permalink, 'deadline': self.deadline, 'time': submission.created_utc}

        self._save(submission.id, s_dic, 'w')
        pass

    @staticmethod
    def _save(s_id, s_dic, mode):
        f = open(s_id, mode)
        f.write(json.dumps(s_dic))
        f.close()
        pass


class SubredditGather:
    """
    This class is used to gather karma data for an specific number of upcoming submissions in a chosen subreddit
    """

    def __init__(self, subreddit, max_posts, analysis_time, analysis_delay):
        """
        Args:
            subreddit (str): name of subreddit.
            max_posts (int): maximum number of posts to be gathered
            analysis_time (float): number of hours each submission will be followed
            analysis_delay (float): number of seconds to wait between data gathering
        """
        self.analysis_time = analysis_time
        self.analysis_delay = analysis_delay
        self.subreddit = subreddit
        self.max_posts = max_posts
        self.watch_thread = threading.Thread(target=self._new_submission_watcher, args=())

    def watch(self):
        """
        Keep checking thread until analysis_time ends
        
        """
        self.watch_thread = threading.Thread(target=self._new_submission_watcher, args=())
        self.watch_thread.start()
        pass

    def thread_status(self):
        """
        Checks class threads status.
        
        Returns:
            True if a thread called by this class is running, False otherwise
        """
        if isinstance(self.watch_thread, None):
            return False
        else:
            return self.watch_thread.isAlive()

    def _new_submission_watcher(self):
        # TODO add multiprocessing support
        # TODO make this function less spaghetti (very hard)
        praw_subreddit = r.get_subreddit(self.subreddit)
        sub_list = [s for s in praw_subreddit.get_new()]
        place_holder = sub_list[0].id
        print(place_holder)

        submission_counter = 0
        while submission_counter < self.max_posts:
            try:
                sub_list = [s for s in praw_subreddit.get_new(place_holder=place_holder)]
                sub_list_id = [s.id for s in sub_list]

                # TODO raise an error instead of turning list empty
                if place_holder not in sub_list_id:
                    sub_list = []
                else:
                    sub_list.pop()

                if len(sub_list) > 0:
                    print_list = [s.id for s in sub_list]
                    print(print_list)
                    place_holder = sub_list[0].id
                    for s in sub_list:
                        SubmissionGather(s.permalink, self.analysis_time, self.analysis_delay).watch()
                    submission_counter += len(sub_list)
            except AttributeError:
                # This error is caused by multiple requests of reddit api
                pass
        pass


if __name__ == '__main__':
    # TODO Check arguments consistency in the future
    argv = sys.argv
    if len(argv) != 5:
        print('this application is expected to be initialized with 4 arguments')
    else:
        SubredditGather(argv[1], int(argv[2]), float(argv[3]), float(argv[4])).watch()
