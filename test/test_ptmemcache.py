import unittest

from ptpy import PtMemcache

class PtMemcas(unittest.TestCase):
        
    def test_init(self):
        self.mc = PtMemcache(host='127.0.0.1', port=11211)
        self.mc.set("test","test")
        print self.mc.get("test")
        self.assertTrue(self.mc.get("test") == "test")

if __name__ == '__main__':
	unittest.main()