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
                                          self.db_name)       
        return self.db       
        pass

    def close(self):
        self.connection.close()
        pass
        
    #TODO    
    def insertNewSubmission(arguments):
        pass
    def updateSubmission(arguments):
        pass
    def getSubmission(arguments):
        pass
    def getListOfSubmissionsBySubreddit(arguments):
        pass
    def getListOfSubmissions(arguments):
        pass 






if __name__ == '__main__':
    MySQLConnection()
