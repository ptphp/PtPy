#coding:utf-8
import sys
import pycurl
import socket
import re
import gzip
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
    

"""
curl = PtCurl()
#url = "https://www.google.com.hk"
#res = curl.request('get',url)
#print res
#sys.exit()
url = "https://wl-prod.sabresonicweb.com/SSW2010/K6K6/webqtrip.html"  
data = "alternativeLandingPage=true&lang=en&journeySpan=OW&origin=BKK&destination=REP&departureDate=2014-04-15&numAdults=1&numChildren=0&numInfants=0"
res = curl.request('post',url,data)
print len(res)
print res[0:100]
#open("k6.txt","wb").write()
#print res
m = re.findall('brandedBasketHashRef":([\d\-]+)',str(res))
print m[0]
url = "https://wl-prod.sabresonicweb.com/SSW2010/K6K6/webqtrip.html"
data = '_eventId_ajax=&execution=e1s1&ajaxSource=true&contextObject={"transferObjects":[{"componentType":"cart","actionCode":"checkPrice","queryData":{"componentId":"cart_1","componentType":"cart","actionCode":"checkPrice","queryData":null,"requestPartials":["initialized"],"selectedBasketRefs":['+m[0]+']}}]}'
print data
res = curl.request('post',url,data)
print res

"""
def headerCookie(buf):  
    print buf  
    
class PtCurl:
    cache = None
    curl = None
    contents = ''
    headers = []
    def __init__(self,debug = False,proxy = None,cookie = None,use_gzip = True):   
        self._proxy = proxy     
        self._debug = debug
        self._use_gzip = use_gzip
        self._cookie = cookie
        self.headers = [
                        'Accept-Language: en-US,en;q=0.8',
                        'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        ]
        self._user_agent = "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36"
        
        self.curl = pycurl.Curl()
    
    def reset(self):    #清空对象
        #b.truncate(0)
        self.curl.reset()
        #self.curl.setopt(pycurl.WRITEFUNCTION, b.write)
        #self.curl.setopt(pycurl.COOKIEJAR, 'cookies.txt')
        #cookies.txt存放登录得到的cookies
        #self.curl.setopt(pycurl.FOLLOWLOCATION, True)
    def request(self,method="GET",url = '',data = '',options = {}):   
        self.curl.reset()     
        method = method.upper()        
        
        b = StringIO()
        
        _options = {      
                        pycurl.URL:url,
                        pycurl.CUSTOMREQUEST:method,
                        pycurl.FOLLOWLOCATION:1,
                        pycurl.MAXREDIRS:5,
                        pycurl.NOBODY:0,
                        # 调试回调.调试信息类型是一个调试信 息的整数标示类型.在这个回调被调用时VERBOSE选项必须可用
                        # 1  详细
                        pycurl.VERBOSE               : 0,
                        pycurl.WRITEFUNCTION         : b.write,
                        pycurl.CONNECTTIMEOUT        : 3000,
                        pycurl.TIMEOUT               : 3000,
                        pycurl.HTTPHEADER            : self.headers,
                        pycurl.HEADER                : 0,
                        pycurl.SSL_VERIFYPEER        : 0,
                        pycurl.SSL_VERIFYHOST        : 0,
                        pycurl.SSL_SESSIONID_CACHE   : 1,                        
                        # Option -b/--cookie <name=string/file> Cookie string or file to read cookies from
                        # Note: must be a string, not a file object.    
                        pycurl.COOKIEFILE            : "cookie_file_name",
                    
                        # Option -c/--cookie-jar <file> Write cookies to this file after operation
                        # Note: must be a string, not a file object.
                        pycurl.COOKIEJAR             : "cookie_file_name",
                        
                        #PROXY
                        #pycurl.PROXY                 : "127.0.0.1:8888",
                        #pycurl.PROXYTYPE             : pycurl.PROXYTYPE_HTTP,
                        #pycurl.PROXYTYPE             : pycurl.PROXYTYPE_SOCKS5,
                        #pycurl.PROXYUSERPWD          : "username:password",
                        pycurl.USERAGENT             : self._user_agent,
                }
        
        _options.update(options)
        
        if self._use_gzip:
            _options[pycurl.ENCODING] = "gzip,deflate"
            
        if self._debug:
            _options[pycurl.VERBOSE] = 2
            
        if self._proxy is not None:
            _options[pycurl.PROXY] = self._proxy
            
        if self._cookie is not None:
            _options[pycurl.COOKIEFILE] = self._cookie
            _options[pycurl.COOKIEJAR] = self._cookie
          
        if method == "POST":
            _options[pycurl.POSTFIELDS] = data
            _options[pycurl.POST]       = 1

        for k in _options:
            self.curl.setopt(k,_options[k])
        
        self.curl.perform()
        self.EFFECTIVE_URL = self.curl.getinfo(self.curl.EFFECTIVE_URL)
        html = b.getvalue()
        b.close()
        self.show_info(self.curl)
        #self.curl.close()
                
        if html[:6]=='\x1f\x8b\x08\x00\x00\x00':
            html=gzip.GzipFile(fileobj=StringIO(html)).read()
            
        return html
    def close(self):
        self.curl.close()
        
    def show_info(self,c):
        return
        print '-'*80
        infos = ['EFFECTIVE_URL', 'RESPONSE_CODE', 'NUM_CONNECTS',
            'TOTAL_TIME', 'NAMELOOKUP_TIME', 'CONNECT_TIME', 'APPCONNECT_TIME',
            'PRETRANSFER_TIME', 'STARTTRANSFER_TIME', 'REDIRECT_TIME']
        for info in infos:
            print info, ':', c.getinfo(getattr(pycurl, info))
        print '-'*80
    def body_callback(self,buf):
        self.contents = self.contents + buf
        
    def get(self,url,options = {}):
        return self.request("GET", url,'',options)
        
    def post(self,url,data = '',options = {}):
        return self.request("POST", url,data,options)
