import unittest

from ptpy import PtMySql
class PtMySqlTest(unittest.TestCase):
    mysql = None
    def init_mysql(self):
        self.mysql = PtMySql('127.0.0.1','test','root','root')
    def setUp(self):
        self.init_mysql()
    def test_init(self):
        mysql = PtMySql('127.0.0.1','test','root','root')
        self.assertTrue(mysql.conn is not None)
        mysql = PtMySql('127.0.0.1','test',user='root',passwd = 'root')
        self.assertTrue(mysql.conn is not None)
        mysql = PtMySql('127.0.0.1','test',user='root',passwd = 'root',port="3306")
        self.assertTrue(mysql.conn is not None)
    def test_get_now(self):
        now = self.mysql.getNow()
        print now
    def test_runSql(self):
        print self.mysql.runSql("create table test()")
        print self.mysql.query("drop table test;")

if __name__ == '__main__':
	unittest.main()