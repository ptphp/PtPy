#coding:utf-8
from ptpy import PtCurl
import unittest
import re

class PtCurlTest(unittest.TestCase):
    ##初始化工作  
    def setUp(self):  
        self.curl = PtCurl()  
        
    def tearDown(self):
        pass
    
    def test_get(self):
        url= "http://www.baidu.com"        
        res = self.curl.get(url)
        self.assertEqual(True, res.find("baidu") > 0, "")
        
    def test_post(self):
        url= "http://www.baidu.com"
        res = self.curl.post(url,"test=1")        
        self.assertEqual(True, res.find("baiduerr") > 0, "")
        
    def _test_request(self):
        url= "http://www.baidu.com"        
        res = self.curl.request('GET',url)
        self.assertEqual(True, res.find("baidu") > 0, "")
        res = self.curl.request('POST',url,"test=1")
        self.assertEqual(True, res.find("baiduerr") > 0, "")        
        
if __name__ =='__main__':  
    unittest.main()  