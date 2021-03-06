"""
This module is used to administrate mysql requests to a database. In this early phase os development the DB project is
very immature.


The submissions table holds the unique thread id provided by reddit. the thread_id is associated to a table with the sa-
me name described next.
submissions(title VARCHAR(1000),
            selftext TEXT,
            time DOUBLE,
            subreddit VARCHAR(300),
            thread_id VARCHAR(50),
            id INT NOT NULL AUTO_INCREMENT,
            PRIMARY KEY (id),
            UNIQUE KEY submission (thread_id, subreddit) );


Every row of a thread_id table contains a snapshot of a thread at a given time (computer_time).

thread_id(computer_time double,
          ratio double,
          upvotes int,
          comments int,
          id int NOT NULL auto_increment,
          PRIMARY KEY (id) )

TODO:
    *Remove print functions (soon)
    *Create documentation for methods
    *Create extract "XML method"
"""

import pymysql
import karmatrain.mysql_config as mysql_config


class MySQLConnection:
    """
    This class is used to manage DB interactions with other classes from the project.
    """
    def __init__(self):
        self.host = mysql_config.host
        self.user = mysql_config.user
        self.password = mysql_config.password
        self.db = mysql_config.db
        self.connection = self._connect()

    def _connect(self):
        self.connection = pymysql.connect(self.host,
                                          self.user,
                                          self.password,
                                          self.db,
                                          autocommit=True)
        return self.connection

    def close(self):
        self.connection.close()
        return True

    # TODO
    def insert_new_submission(self, title, thread_id, subreddit, selftext, time):
        cur = self.connection.cursor()
        selftext += ' '
        try:
            i = cur.execute("""SHOW TABLES LIKE 'submissions';
                            """)
            if i == 0:
                self._create_submissions_main_table(cur)

#            print(title,'\n', thread_id,'\n', subreddit,'\n',selftext,'\n', time)
            cur.execute(u"""
                        INSERT INTO submissions VALUES (\"%s\",\"%s\",\"%f\",\"%s\",\"%s\",NULL);
                        """ % (title, str(selftext), time, subreddit, thread_id))

            self._create_submission_table(cur, thread_id)
            cur.close()
        except:
            # TODO: exception treatment ("already exists" and others)
            cur.close()
            raise
        return True

    def delete_submission(self, thread_id):
        cur = self.connection.cursor()
        try:
            cur.execute("DROP TABLE %s ;" % thread_id)
            cur.execute("DELETE FROM submissions WHERE submissions.thread_id = \"%s\" ;" % thread_id)
        except:
            raise
        return True

    def update_submission(self, thread_id, computer_time, ratio, ups, num_comments):
        print("updated")
        try:
            cur = self.connection.cursor()
            cur.execute("""INSERT INTO {0:s}(computer_time, ratio, upvotes, comments)
                        VALUES ({1:f}, {2:f}, {3:f}, {4:d});""".format(thread_id, computer_time, ratio,
                                                                      ups, num_comments)
                        )
            print("updated2")
            cur.execute("SELECT * FROM {0:s};".format(thread_id)
                        )
            print(cur.fetchall())
            print("SELECT * FROM {0:s};".format(thread_id))

            cur.close()

        except:
            raise
        return True

    def get_submission(self, thread_id):
        try:
            cur = self.connection.cursor()
            cur.execute(u'SELECT * FROM {0:s} ;'.format(thread_id))
            sub_data = cur.fetchall()
            cur.close()
            return sub_data
        except:
            raise
        pass

    def get_list_of_submissions(self):
        try:
            cur = self.connection.cursor()
            cur.execute("SELECT thread_id FROM submissions;")
            sub_list = cur.fetchall()
            cur.close()
            return [t[0] for t in sub_list]
        except:
            raise
        pass

    @staticmethod
    def _create_submissions_main_table(cur):
        try:
            cur.execute("""CREATE TABLE submissions (
                            title VARCHAR(1000), 
                            selftext TEXT,
                            time DOUBLE,
                            subreddit VARCHAR(300),
                            thread_id VARCHAR(50),
                            id INT NOT NULL AUTO_INCREMENT,
                            PRIMARY KEY (id),
                            UNIQUE KEY submission (thread_id, subreddit) );
                    """)
        except:
            raise
        pass

    @staticmethod
    def _create_submission_table(cur, table_name):
        try:
            cur.execute("""CREATE TABLE %s (
                            computer_time double, 
                            ratio double,
                            upvotes int,
                            comments int, 
                            id int NOT NULL auto_increment, 
                            PRIMARY KEY (id) );
                    """ % table_name)
        except:
            raise
        pass



