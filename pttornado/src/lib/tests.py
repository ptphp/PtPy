import tornado.testing
import urllib
import unittest
import sys
import os
import pprint
import inspect
class BaseTestCase(unittest.TestCase):
    def setUp(self):
        pass
#
#class PtUnit(object):
class PtUnit(tornado.testing.AsyncHTTPTestCase):
    __method = "METHOD"
    def main(self):
        
        if self.__method in os.environ.keys() and os.environ[self.__method] :
            if hasattr(self,os.environ[self.__method]):
                getattr(self,os.environ[self.__method])()
            else:
                print "pls select method name"
        else:
            unittest.main()
        
class BaseHandlerTestCase(PtUnit):   
    proxy_host = None
    proxy_port = None
    def setUp(self):
        super(BaseHandlerTestCase, self).setUp()
        
    def get(self,path):
        response = self.fetch(path,method='GET',proxy_host = self.proxy_host,proxy_port = self.proxy_port,follow_redirects=False)
        return response
    
    def post(self,path,data):
        response = self.fetch(path,method='POST',body=urllib.urlencode(data),proxy_host = self.proxy_host,proxy_port = self.proxy_port,follow_redirects=False)
        return response 