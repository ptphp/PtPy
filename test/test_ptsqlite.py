import unittest
import os
from ptpy import PtSqlite

class PtSqliteTest(unittest.TestCase):
    sqlite = None
    db_path = "/tmp/test.db"
    def init_sqlite(self):
        self.sqlite = PtSqlite()
    def setUp(self):
        self.init_sqlite()

    def test_open(self):         
        self.sqlite.open(self.db_path)        
        self.assertTrue(os.path.exists(self.db_path))
    def test_delete_db(self):
        self.sqlite.open(self.db_path)        
        self.sqlite.deleteDb(self.db_path)
        self.assertTrue(False == os.path.exists(self.db_path))
        
if __name__ == '__main__':
	unittest.main()