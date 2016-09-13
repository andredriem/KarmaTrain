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
    $ your_submission = DataGatherer.SubmissionGather("INSERT SUBMISSION PERMALINK HERE",2,20)
    $ your_submission.watch()
    $ #This will gather karma data from the your submission for the next 2h checking the thread
    $ #for changes every 20 seconds.
    
    
    To generate gather data file (see data folder) from a specific subreddit over time:
    $ python
    $ import DataGatherer
    $ subreddit = DataGatherer.SubredditGather('circlejerk',500,24,20)
    $ subreddit.watch()
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
    def __init__(self,permalink,analysis_time,analysis_delay):
        """
        Args:
            submission (str): url (permalink) of submission.
            analysis_time (float): Time in hours the function should watch the thread
            analysis_delay (float): TIme in seconds indicating the delay to gather data
        """
        self.permalink = permalink
        self.analysis_time = analysis_time 
        self.analysis_delay = analysis_delay
        
        self.watch_thread = None
        now = time.time()
        self.deadline = now + ( self.analysis_time * 3600.0 )
        self.watch_thread = threading.Thread(target=self.__periodicUpdate__, args=(self.deadline,self.analysis_delay))
        self.__fileInit__()
        
    
       
    def update(self):
        """
        Forces an update in submission file
        """
        submission = r.get_submission(self.permalink)
        s_dic = {}
        s_dic['ups'] = submission.ups
        s_dic['ratio'] = submission.upvote_ratio
        s_dic['computer_time'] = time.time()
        s_dic['num_comments'] = submission.num_comments
              
        self.__save__(submission.id,s_dic,'a')
        pass
   
     
    def watch(self):
        """
        Keep checking thread until analisys_time ends
        
        """
        
        now = time.time()
        self.deadline = now + ( self.analysis_time * 3600.0 )
        self.watch_thread = threading.Thread(target=self.__periodicUpdate__, args=(self.deadline,self.analysis_delay))
        self.watch_thread.start()    
        pass
        
    def getThreadStatus(self):
        """
        Checks class threads status
        
        Returns:
            True if a thread called by this class is running, False otherwise
        """
        if type(self.watch_thread) == type(None):
            return False
        else:
            return self.watch_thread.isAlive()
        
        
    def __periodicUpdate__(self,deadline,delay):
        """
        For devs only:
            Since this funcion will be executing for a long time and reddit servers can go down at any time
            this function will need a proper error handling.
        """
        try:
            while time.time() <= deadline:
                self.update()
                time.sleep(delay)
        except AttributeError:
        #This erros is caused by multiple requests of reddit api
            pass
        pass
            
    def __fileInit__(self):
        submission = r.get_submission(self.permalink)
        s_dic = {}
        s_dic['title'] = submission.title
        s_dic['selftext'] = submission.selftext
        s_dic['id'] = submission.id
        s_dic['permalink'] = self.permalink
        s_dic['deadline'] = self.deadline
        s_dic['time'] = submission.created_utc
                
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
    def __init__(self,subreddit,max_posts,analysis_time,analysis_delay):
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
        self.watch_thread = threading.Thread(target=self.__newSubmissionWatcher__, args=())
        

    def watch(self):
        """
        Keep checking thread until analisys_time ends
        
        """
        self.watch_thread = threading.Thread(target=self.__newSubmissionWatcher__, args=())
        self.watch_thread.start() 
        pass

    def getThreadStatus(self):
        """
        Checks class threads status
        
        Returns:
            True if a thread called by this class is running, False otherwise
        """
        if type(self.watch_thread) == type(None):
            return False
        else:
            return self.watch_thread.isAlive()
        
    def __newSubmissionWatcher__(self):
        #TODO add core suppor
        praw_subreddit = r.get_subreddit(self.subreddit)
        sub_list = [s for s in praw_subreddit.get_new()]
        place_holder = sub_list[0].id
        print place_holder
        
        submission_counter = 0
        while submission_counter < self.max_posts:
            try:
                sub_list = [s for s in praw_subreddit.get_new(place_holder = place_holder)] 
                sub_list_id = [s.id for s in sub_list]
                if place_holder not in sub_list_id:
                    sub_list = []      
                else:
                    sub_list.pop()
                if len(sub_list) > 0:
                    printlist = [s.id for s in sub_list]
                    print printlist
                    place_holder = sub_list[0].id
                    for s in sub_list:
                        SubmissionGather(s.permalink,self.analysis_time,self.analysis_delay).watch()
                    submission_counter += len(sub_list)
            except AttributeError:
            #This error is caused by multiple requests of reddit api
                pass
        pass
        

        

    
