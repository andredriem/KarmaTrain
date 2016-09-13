# -*- coding: utf-8 -*-
"""
This module provides the user a diverse set of tools for gathering statistical karma data from a
specific subreddit or submission. It generates files containing several json elements. The first json
contains information about the thread, the following contain karma data over time. Each file is
identified by it's submission ID.



Exemples:

    To generate gather data file (see data folder) from a specific post over time:
    $ python
    $ import DataGatherer
    $ your_submission = DataGatherer.SubmissionGather("INSERT SUBMISSION PERMALINK HERE")
    $ your_submission.watch(2,20)
    $ #This will gather karma data from the your submission for the next 2h checking the thread
    $ #for changes every 20 seconds.
    
    
    To generate gather data file (see data folder) from a specific subreddit over time:
    $ python
    $ import DataGatherer
    $ subreddit = DataGatherer.SubredditGather('circlejerk')
    $ subreddit.watch(500,24,20)
    $ #This will gather karma data for the next 500 submissions from /r/circlejerk for the next 24h
    $ #checking each thread for changes every 20 seconds.   
    
Todo:
    *Do error handling in __periodicUpdate__
    *Finish __newSubmissionWatcher__

"""



import praw
import json
import time
import threading

r = praw.Reddit('Submission data gatherer')
    
class SubmissionGather:
    """
    This class is used to gather karma data from a specific submission
    """
    def __init__(self,submission_permalink):
        """
        Args:
            submission (str): url (permalink) of submission.
        """
        self.thread_running_flag = False
        self.permalink = submission_permalink
        self.__fileInit__()
        
    
       
    def update(self):
        """
        Forces an update in submission file
        """
        submission = r.get_submission(self.permalink)
        s_dic = {}
        s_dic['ups'] = submission.ups
        s_dic['ratio'] = submission.upvote_ratio
        s_dic['time'] = submission.created_utc
        s_dic['computer_time'] = time.time()
              
        self.__save__(submission.id,s_dic,'a')
        pass
   
     
    def watch(self,analysis_time,analysis_delay):
        """
        Keep checking thread until analisys_time ends
        
        Attributes:
            analysis_time (float): Time in hours the function should watch the thread
            analysis_delay (float): TIme in seconds indicating the delay to gather data
        """
        
        now = time.time()
        deadline = now + ( analysis_time * 3600.0 )
        watch_thread = threading.Thread(target=self.__periodicUpdate__, args=(deadline,analysis_delay))
        watch_thread.start()    
        pass
        
    def getThreadStatus(self):
        """
        Checks class threads status
        
        Returns:
            True if a thread called by this class is running, False otherwise
        """
        return self.thread_running_flag
        
        
    def __periodicUpdate__(self,deadline,delay):
        #TODO Server error handling
        """
        For devs only:
            Since this funcion will be executing for a long time and reddit servers can go down at any time
            this function will need a proper error handling.
        """
        self.thread_running_flag = True
        while time.time() <= deadline:
            self.update()
            time.sleep(delay)
        self.thread_running_flag = False
        pass
            
    def __fileInit__(self):
        submission = r.get_submission(self.permalink)
        s_dic = {}
        s_dic['title'] = submission.title
        s_dic['selftext'] = submission.selftext
        s_dic['id'] = submission.id
        s_dic['permalink'] = self.permalink
                
        self.__save__(submission.id,s_dic,'w')
        pass

    def __save__(self,s_id,s_dic,mode):
        f = open(s_id,mode)
        f.write(json.dumps(s_dic))
        f.close()
        pass
        
class SubredditGather:
    """
    This class is used to gather karma data for an specific number of upcomming submissions in a chosen subreddit
    """
    def __init__(self,subreddit):
        """
        Args:
            subreddit (str): name of subreddit.
        """
        self.thread_running_flag = False
        self.subreddit = subreddit
        

    def watch(self,max_posts,analysis_time,analysis_delay):
        """
        Keep checking thread until analisys_time ends
        
        Attributes:
            max_posts (int): maximum number of posts to be gathered
            analysis_time (float): number of hours each submission will be followed
            analysis_delay (float): number of seconds to wait between data gathering
        """
        watch_thread = threading.Thread(target=self.__newSubmissionWatcher__, args=(max_posts,analysis_time,analysis_delay))
        watch_thread.start() 
        pass

    def getThreadStatus(self):
        """
        Checks class threads status
        
        Returns:
            True if a thread called by this class is running, False otherwise
        """
        return self.thread_running_flag
        
    def __newSubmissionWatcher__(self,max_posts,analysis_time,analysis_delay):
        self.thread_running_flag = True
        #TODO finish this function
        self.thread_running_flag = False
        
