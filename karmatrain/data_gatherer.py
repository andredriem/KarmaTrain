# -*- coding: utf-8 -*-
"""
This module provides the user a diverse set of tools for gathering statistical karma data from a
specific subreddit or submission. It generates files containing several json elements. The first json
contains information about the thread, the following contain karma data over time. Each file is
identified by it's submission ID.



Exemples:

    To generate gather data file (see data folder) from a specific post over time:
    $ python
    $ import data_gatherer
    $ your_submission = data_gatherer.Submission("INSERT SUBMISSION PERMALINK HERE")
    $ your_submission.watch(2,20)
    $ #This will gather karma data from the your submission for the next 2h checking the thread
    $ #for changes every 20 seconds.
    
    
    To generate gather data file (see data folder) from a specific subreddit over time:
    $ python
    $ import data_gatherer
    $ subreddit = data_gatherer.Subreddit('circlejerk',500,24,20)
    $ #This will gather karma data for the next 500 submission from /r/circlejerk for the next 24h
    $ #checking each thread for changes every 20 seconds.   
    
Todo:
    *Finish Submission.watch()
    *Finish Subreddit class

"""



import praw
import json
import time

r = praw.Reddit('Submission data gatherer')
    
class Submission:
    """This class is used to gather karma data from a specific submission
    """
    def __init__(self,submission_permalink):
        """
        Args:
            submission (str): url (permalink) of submission.
        """
        
        self.permalink = submission_permalink
        self.__fileInit__()
    
    @classmethod    
    def update(self):
        """Forces an update in submission file
        """
        submission = r.get_submission(self.permalink)
        s_dic = {}
        s_dic['ups'] = submission.ups
        s_dic['ratio'] = submission.upvote_ratio
        s_dic['time'] = submission.created_utc
        s_dic['computer_time'] = time.time()
              
        self.__save__(submission.id,s_dic,'a')
        pass
   
    @classmethod 
    #TODO schedules a new thread to gather data from submission
    def watch(self):
        pass
            
    def __fileInit__(self):
        submission = r.get_submission(self.permalink)
        s_dic = {}
        s_dic['title'] = submission.title
        s_dic['selftext'] = submission.selftext
        s_dic['id'] = submission.id
        s_dic['permalink'] = self.permalink
                
        self.__save__(submission.id,s_dic,'w')

    def __save__(self,s_id,s_dic,mode):
        f = open(s_id,mode)
        f.write(json.dumps(s_dic))
        f.close()
        
class Subreddit:
    def __init__(self,subreddit,max_posts,analysis_time,analysis_delay):
        self.subreddit = subreddit
        self.max_posts = max_posts
        self.analysis_time = analysis_time
        self.analysis_delay = analysis_delay
        self.first_submission = self.__defineFirstSubmission__()

    def __defineFirstSubmission__(self):
        pass
        
        
