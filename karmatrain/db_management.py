"""
This module is used to administrate mysql requests to a database.
"""


import mysql_config
import MySQLdb


class MySQLConnection:

    def __init__(self):
        self.host = mysql_config.host
        self.user = mysql_config.user
        self.password = mysql_config.password
        self.db = mysql_config.db
        self.connection = self.__connect__()
                             
    def __connect__(self): 
        self.connection = MySQLdb.connect(self.host,
                                          self.user,       
                                          self.password, 
                                          self.db)       
        return self.connection       
        pass

    def close(self):
        self.connection.close()
        pass
        
    #TODO    
    def insertNewSubmission(self,table_name):
        cur = self.connection.cursor()
        try:
            i = cur.execute("""SHOW TABLES LIKE 'submissions';
                            """)
            if i == 0:
                self._createSubmissionsTable(cur)
            
            self._createThisSubmissionTable(cur,table_name)
            #TODO: updateSubmissionsTable with the new submission info
            cur.close()
        except:
            #TODO: exception treatment ("already exists" and others)
            cur.close()
            raise
        pass
        
    def updateSubmission(self,table_name,dic):
        try:
            cur = self.connection.cursor()
            cur.execute("""INSERT INTO %s(computer_time, ratio, upvotes, comments) 
                        VALUES (%f, %f, %d, %d)"""%(table_name,dic['computer_time'],dic['ratio'],dic['ups'],dic['num_comments'])
                        )
            cur.execute("""SELECT * FROM %s"""%(table_name)
                       )   
            print cur.fetchall()
            cur.close()
        except:
            cur.close()
            raise
        pass
    def getSubmission(self,arguments):
        pass
    def getListOfSubmissionsBySubreddit(self,arguments):
        pass
    def getListOfSubmissions(self,arguments):
        pass 
        
    def _createSubmissionsTable(self,cur):
        try:
            cur.execute("""CREATE TABLE submissions (
                            permalink VARCHAR(1000) UNIQUE, 
                            title VARCHAR(1000), 
                            selftext text,
                            time double, 
                            subreddit VARCHAR(3000),
                            submission_id VARCHAR(50), 
                            id int NOT NULL auto_increment, 
                            PRIMARY KEY (id),
                            UNIQUE KEY submission (submission_id, subreddit) );
                    """)
        except:
            raise
        pass
        
    def _createThisSubmissionTable(self,cur,table_name):
        try:
            cur.execute("""CREATE TABLE %s (
                            computer_time double, 
                            ratio double,
                            upvotes int,
                            comments int, 
                            id int NOT NULL auto_increment, 
                            PRIMARY KEY (id) );
                    """%(table_name))
        except:
            raise 
        pass





if __name__ == '__main__':
    MySQLConnection().insertNewSubmission('test1')
    s_dic = {}
    s_dic['ups'] = 1
    s_dic['ratio'] = 0.99
    s_dic['computer_time'] = 0.1
    s_dic['num_comments'] = 9001
    MySQLConnection().updateSubmission('test1',s_dic)
      
