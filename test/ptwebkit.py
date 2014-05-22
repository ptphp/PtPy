import unittest
import os
import logging
import cookielib
import pprint

from ptpy import PtWebkit


browser = PtWebkit(display = True)
page,res = browser.open("http://www.baidu.com")
