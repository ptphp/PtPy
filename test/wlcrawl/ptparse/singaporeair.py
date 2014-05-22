from ptpy.ptcurl import PtCurl
import unittest
import urlparse
import pycurl
import re
import urllib
import time

class SqParse():
    def __init__(self):
        self.curl = PtCurl()
        
    def get_execution(self,url = "http://www.singaporeair.com/SAA-flow.form?execution=e4s1"):
        return urlparse.urlparse(url).query.replace("execution=","")
    
    def open(self):     
        self.curl = PtCurl(debug = True,proxy = "127.0.0.1:8888",cookie = "singaporeair.txt" )
        url = "http://www.singaporeair.com/"    
        res = self.curl.get(url)          
        
        url = "http://www.singaporeair.com/SAA-flow.form"
        res = self.curl.get(url)            
        refer =  self.curl.EFFECTIVE_URL    
        self.curl.get("http://www.singaporeair.com/breakingAlert.form",
                      {
                       pycurl.HTTPHEADER:[
                                          "X-Requested-With: XMLHttpRequest"
                                          ]
                       }
                      )
        
        location =  self.curl.EFFECTIVE_URL
        r = {}
        r['r'] = refer
        r['s'] = str(time.time()).replace(".","")+"0"
        AKSB = urllib.urlencode(r)
        execution = self.get_execution_from_form(res)
        print execution
        #execution = self.get_execution(refer)
        #print execution
       
        url = "http://www.singaporeair.com/booking-flow.form?execution=" + execution.strip()
        origin = "PEK"
        dest = "BKK"
        d_month = "042014"
        d_day = "22"        
        r_month = "052014"
        r_day = "5"
        
        data = "_payByMiles=on&_pwmFlightSearchCheckBox=on&recentSearches=&origin=PVG&destination=BKK&departureDay=23&departureMonth=042014&_tripType=on&returnDay=14&returnMonth=052014&cabinClass=Y&numOfAdults=1&numOfChildren=0&numOfInfants=0&_eventId_flightSearchEvent=&isLoggedInUser=false&numOfChildNominees=&numOfAdultNominees="
        
        res = self.curl.post(url, data,{
                                        pycurl.HTTPHEADER:[
                                                           "Content-Type: application/x-www-form-urlencoded"
                                                           ],
                                        pycurl.REFERER:refer,
                                        pycurl.COOKIE:"AKSB="+AKSB
                                        })
        
        #location = self.curl.EFFECTIVE_URL
        
        #print len(res)
        
        #self.curl.get(location,{
        #                   pycurl.VERBOSE:2,
        #                   })
        
    def get_execution_from_form(self,form = '<form id="searchForm" class="jQvalidateForm" action="/booking-flow.form?execution=e1s1" method="post">'):
        m = re.search("id=\"searchForm\" class=\"jQvalidateForm\" action=\"/booking-flow.form\?execution=([^\"]+)",form)
        return m.group(1)
class TestSq(unittest.TestCase):
    def setUp(self):
        self.parse = SqParse()
    def test_get_execution_from_form(self):
        execution = self.parse.get_execution_from_form()
        self.assertTrue("s" in execution, "execution is not valid")
    def test_get_execution(self):
        execution = self.parse.get_execution()
        self.assertTrue("s" in execution, "execution is not valid")
        
    def test_open(self):
        self.parse.open()

if __name__ == "__main__":
    unittest.main()