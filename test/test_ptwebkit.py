import unittest
import os
import logging
import cookielib
import pprint

from ptpy import PtWebkit
from ptpy import PtWebkitTestCase



from ptwebkit_flask_app import app

PORT = 5000

base_url = 'http://localhost:%s/' % PORT

class PtWebkitTest(PtWebkitTestCase):
    port = PORT
    display = True
    log_level = logging.INFO

    @classmethod
    def create_app(cls):
        return app

    def test_open(self):
    	pass
        #page, resources = self.ptwebkit.open("http://www.baidu.com")
        #self.assertEqual(page.url, base_url)
        #pprint.pprint(resources)
        self.assertTrue("baidu" in self.ptwebkit.content)
    def test_set_proxy(self):
        self.ptwebkit.set_proxy("http")
        page, resources = self.ptwebkit.open("http://www.google.com")
        for res in resources:
            print res.url
        
if __name__ == '__main__':
	unittest.main()