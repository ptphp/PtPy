#coding:utf-8
import unittest
from ptpy.ptcurl import PtCurl
import pycurl
import re
import json
import urlparse
import datetime
import time
import cStringIO


class TestK6(unittest.TestCase):
                
    def parse_res(self,res):
        res_ = json.loads(res.strip())
        outbounds = res_['content'][0]['model']['outbounds']
        for outbound in outbounds:
            #pprint.pprint(outbound)
            print "*"*20
            print outbound["itineraryPartData"]['aircraftType']
            print outbound["itineraryPartData"]['airlineCodes']
            print outbound["itineraryPartData"]['departureCode']
            print outbound["itineraryPartData"]['arrivalCodes']
            print outbound["itineraryPartData"]['departureDate']
                    
    def test_open(self):
        
        origin = "BKK"
        destination = "REP"
        departureDate = "2014-04-21"
        url = "https://wl-prod.sabresonicweb.com/SSW2010/K6K6/webqtrip.html"
        
        postData = "alternativeLandingPage=true&lang=en&journeySpan=OW&"
        postData += "origin=" + origin + "&"
        postData += "destination=" + destination + "&"
        postData += "departureDate=" + departureDate + "&"
        postData += "numAdults=1&numChildren=0&numInfants=0"
                
        #return
        curl = PtCurl()
        curl.headers = [
                        "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36",
                        'Connection: keep-alive',
                        'Accept-Language: en-US,en;q=0.8',
                        'Accept-Encoding: gzip,deflate',
                        'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        "Content-Type:application/x-www-form-urlencoded"
                         ]
        
        res = curl.post(url, postData, {
                                  pycurl.VERBOSE:1
                                  })
        e_url = curl.EFFECTIVE_URL
        execution =  urlparse.urlparse(e_url).query.replace("execution=","")
        
        
        d_date = "2014/04/25 00:00:00"
        
        format="%Y/%m/%d %H:%M:%S"
        dt = datetime.datetime.strptime(d_date, format)
        refer_url = e_url;
        headers = curl.headers
        headers.append("Referer:https://wl-prod.sabresonicweb.com/SSW2010/K6K6/webqtrip.html?execution="+execution)
        headers.append("X-Requested-With:XMLHttpRequest")
        for i in range(30*6):
            print "*"*40
            time.sleep(1)        
            i = i + 1     
            t = (dt+datetime.timedelta(i)).strftime(format).strip() 
            url = "https://wl-prod.sabresonicweb.com/SSW2010/K6K6/webqtrip.html"
            data = '_eventId_ajax=&execution='+execution+'&ajaxSource=true&contextObject={"transferObjects":[{"componentType":"flc","actionCode":"dateChanged","queryData":{"componentId":"flc_1","componentType":"flc","actionCode":"dateChanged","queryData":null,"basketHashRefs":[null],"departureDate":"'+t+'","returnDate":null,"requestPartials":["__oneway"]}}]}'
            
            
            res = curl.post(url, data, {
                                      pycurl.VERBOSE:1,
                                      pycurl.HTTPHEADER:headers
                                      })
            print t
            if res:                
                res_ = json.loads(res.strip())
                outbounds = res_['content'][0]['model']['outbounds']
                for outbound in outbounds:
                    #pprint.pprint(outbound)
                    print "*"*20
                    print outbound["itineraryPartData"]['aircraftType']
                    print outbound["itineraryPartData"]['airlineCodes']
                    print outbound["itineraryPartData"]['departureCode']
                    print outbound["itineraryPartData"]['arrivalCodes']
                    print outbound["itineraryPartData"]['departureDate']
                
        
        
if __name__ == "__main__":
    unittest.main()
    
    
    