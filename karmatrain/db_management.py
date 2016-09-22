"""
This module is used to administrate mysql requests to a database.
"""

import pymysql
import karmatrain.mysql_config as mysql_config


class MySQLConnection:
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
                                          self.db)
        return self.connection
        pass

    def close(self):
        self.connection.close()
        pass

    # TODO
    def insert_new_submission(self, table_name):
        cur = self.connection.cursor()
        try:
            i = cur.execute("""SHOW TABLES LIKE 'submissions';
                            """)
            if i == 0:
                self._create_submissions_main_table(cur)

            # TODO add a row with submission data in submissions table
            self._create_submission_table(cur, table_name)
            cur.close()
        except:
            # TODO: exception treatment ("already exists" and others)
            cur.close()
            raise
        pass

    def delete_submission(self, table_name):
        cur = self.connection.cursor()
        try:
            cur.execute("DROP TABLE %s ;" % table_name)
            cur.execute("DELETE FROM submissions WHERE submissions.submission_id = %s" % table_name)
        except:
            raise
        pass

    def update_submission(self, table_name, dic):
        try:
            cur = self.connection.cursor()
            cur.execute("""INSERT INTO {0:s}(computer_time, ratio, upvotes, comments)
                        VALUES ({1:f}, {2:f}, {3:d}, {4:d})""".format(table_name, dic['computer_time'], dic['ratio'],
                                                                      dic['ups'], dic['num_comments'])
                        )
            cur.execute("SELECT * FROM {0:s}".format(table_name)
                        )
#            print(cur.fetchall())
            cur.close()
        except:
            raise
        pass

    def get_submission(self, sub_id):
        try:
            cur = self.connection.cursor()
            cur.execute(u'SELECT * FROM {0:s} ;'.format(sub_id))
            sub_data = cur.fetchall()
            cur.close()
            return sub_data
        except:
            raise
        pass

    def get_list_of_submissions(self):
        try:
            cur = self.connection.cursor()
            cur.execute("SELECT submission_id FROM submissions;")
            sub_list = cur.fetchall()
            cur.close()
            return sub_list
        except:
            raise
        pass

    @staticmethod
    def _create_submissions_main_table(cur):
        try:
            cur.execute("""CREATE TABLE submissions (
                            permalink VARCHAR(1000) UNIQUE, 
                            title VARCHAR(1000), 
                            selftext TEXT,
                            time DOUBLE,
                            subreddit VARCHAR(300),
                            submission_id VARCHAR(50), 
                            id INT NOT NULL AUTO_INCREMENT,
                            PRIMARY KEY (id),
                            UNIQUE KEY submission (submission_id, subreddit) );
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


if __name__ == '__main__':
    conn = MySQLConnection()
    try:
        conn.insert_new_submission('test1')
        conn.insert_new_submission('test2')
        conn.insert_new_submission('test3')
        print(conn.get_list_of_submissions())
        conn.delete_submission('test1')
        conn.delete_submission('test2')
        conn.delete_submission('test3')
        conn.close()
    except:
        raise
    pass
