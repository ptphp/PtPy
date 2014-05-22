import unittest

from ptpy import PtRedis

class PtRedisTest(unittest.TestCase):
    redis = None
    def init_redis(self):
        self.redis = PtRedis()
    def setUp(self):
        self.init_redis()
    def test_init(self):
        self.redis = PtRedis(host='localhost', port=6379, db=0)
        self.redis.set("test","test")
        print self.redis.get("test")
        self.assertTrue(self.redis.get("test") == "test")
        self.redis = PtRedis(host='localhost', port=6379, db=1)
        self.redis.set("test","test")
        print self.redis.get("test")
        self.assertTrue(self.redis.get("test") == "test")

if __name__ == '__main__':
	unittest.main()