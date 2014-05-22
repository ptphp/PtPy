from ptpy.ptcurl import PtCurl
import unittest
import urlparse
import pycurl
import re

class Parse():
    def __init__(self):
        self.curl = PtCurl()
        
    def open(self):     
        pass
    
class TestSq(unittest.TestCase):
    def setUp(self):
        self.parse = Parse()
        
    def test_open(self):
        curl = PtCurl(debug = True,proxy = "127.0.0.1:8888",cookie = "malindoair.txt" )
        res = curl.get("http://www.malindoair.com/en")
        
        url = "https://search.malindoair.com/default.aspx?aid=91&df=UK&edepCity=&earrCity=&culture=en-GB&afid=0&b2b=0&St=fa&hotelcode=&councode=&adult2=0&child2=0&infant2=0&DFlight=false&roomcount=1&currency=MYR&cpromo=&Jtype=1&depCity=DAC&arrCity=DPS&depDate=22%2F04%2F2014&adult1=1&child1=0&infant1=0&childage1r1=0&childage1r2=0&childage1r3=0&childage2r1=0&childage2r2=0&childage3r1=0&promocode="
        res = curl.get(url)

        m = re.search("window.location.href = '([^']+)';",res)
        url = "https://search.malindoair.com/" + m.group(1)
        res = curl.get(url)
                
        res = curl.post("https://search.malindoair.com/Flight.aspx/GetFlightSearch","{}",
                        {
                         pycurl.REFERER:url,
                         pycurl.HTTPHEADER:[
                            "Content-Type: application/json; charset=UTF-8",
                            "X-Requested-With: XMLHttpRequest",
                            ]
                         })
        
if __name__ == "__main__":
    unittest.main()