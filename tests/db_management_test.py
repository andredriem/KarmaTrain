import unittest

import karmatrain.db_management as db_management

# CONSTANTS FOR TESTING

SD1 = {"title": "title1", "selftext": "selftext1", "subreddit": "brasil", "time": 1234, "thread_id": "1DFGG"}
SD2 = {"title": "title2", "selftext": "selftext1", "subreddit": "brasil2", "time": 1234, "thread_id": "2DFGG"}
SD3 = {"title": "title3", "selftext": "selftext1", "subreddit": "brasil3", "time": 1234, "thread_id": "3DFGG"}

SD_EXTRA = {"title": "title3", "selftext": "selftext1", "subreddit": "brasil3", "time": 1234, "thread_id": "4DFGG"}

ST1 = {"thread_id": "1DFGG", "computer_time": 1, "ratio": 0.1, "ups": 99, "num_comments": 9001}
ST2 = {"thread_id": "1DFGG", "computer_time": 2, "ratio": 0.1, "ups": 98, "num_comments": 9002}
ST3 = {"thread_id": "1DFGG", "computer_time": 3, "ratio": 0.1, "ups": 0, "num_comments": 9003}

UPDATE_SUBMISSION_EXPECTED_RESULT = ((1.0, 0.1, 99, 9001, 1), (2.0, 0.1, 98, 9002, 2), (3.0, 0.1, 0, 9003, 3))

ST_LIST = [ST1, ST2, ST3]

THREAD_ID_LIST = []


class TestMySQLConnection(unittest.TestCase):

    def setUp(self):
        try:
            self.conn = db_management.MySQLConnection()
        except:
            # TODO Find specific error later
            self.skipTest("Can't connect to database")

    pass

    def test_methods(self):
        """I made a monolithic unit test because otherwise I would have to write hundreds of lines to set up different
        environments"""

        # test insert_new_submission method
        self.assertEqual(
            self.conn.insert_new_submission(SD1["title"], SD1["thread_id"], SD1["subreddit"], SD1["selftext"],
                                            SD1["time"]),
            True)
        THREAD_ID_LIST.append(SD1["thread_id"])

        # test update_submission method
        for st in ST_LIST:
            self.conn.update_submission(st["thread_id"], st["computer_time"], st["ratio"], st["ups"],st["num_comments"])
        self.assertEqual(self.conn.get_submission(SD1["thread_id"]), UPDATE_SUBMISSION_EXPECTED_RESULT)

        # test get_list_of_submissions method
        self.assertEqual(self.conn.get_list_of_submissions(), ['1DFGG'])

        # test delete_submission
        self.conn.delete_submission(SD1["thread_id"])
        self.assertEqual(self.conn.get_list_of_submissions(), [])
        THREAD_ID_LIST.remove('1DFGG')


        pass


    @classmethod
    def tearDownClass(cls):
        print("cleaning up database...", end='')
        conn = db_management.MySQLConnection()
        cur = conn.connection.cursor()
        try:
            cur.execute("DROP TABLE submissions")
            for thread_id in THREAD_ID_LIST:
                cur.execute(u"DROP TABLE {0:s}".format(thread_id))
            print("  DONE!")
        except:
            print(" FAILED to clean up database after test")
        pass

    def tearDown(self):
        self.conn.close()
        pass


if __name__ == '__main__':
    unittest.main()
    pass
