import os
import random
import cookielib
import re
import urllib2
import urllib
from mimetypes import MimeTypes
import urlparse

from ptdb import PtSqlite
from ptthread import PtWorkManager
from ptcore import PtCp,PtFile
from ptcore import hex_md5, pathHashDir, makeDir, rmDir, user_agents,\
    error_log, trace_back
    
    
class NoRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        pass
    def http_error_302(self, req, fp, code, msg, headers):
        pass
    

    
class PtSpider(object):      
    def __init__(self):
        self.http = PtUrllib() 
        self.http.cache =True
        self.file = PtFile()
        self.cp = PtCp()
        self.db = PtSqlite()
        
    def md5(self,s):
        return hex_md5(s)
    def hash_dir(self,s,level = 3):
        return pathHashDir(s,level)
    def makeDir(self,filename):
        makeDir(os.path.dirname(filename))
    def rmDir(self,d):
        rmDir(d)
        
class PtUrllib(object):
    cache_dir      = '.cache'
    cookie_file    = 'cookie.txt'
    cache          = False    
    user_agent = None
    opener = None
    debuglevel = 0
    cookie_jar = None
    redirect30x = True
    proxy = None
    def __init__(self):
        #self.user_agent = random.choice(user_agents)
        self.user_agent = random.choice(user_agents)
        
    def getUrlCacheFile(self,url,level = 3):    
        return os.path.join(os.path.abspath(self.cache_dir),pathHashDir(url,level),hex_md5(url)+".txt")
    
    def checkUrlCacheExits(self,url,level = 3):
        path = self.getUrlCacheFile(url,level)
        return os.path.isfile(path)        
        
    def delUrlCache(self,url,level = 3):             
        path = self.getUrlCacheFile(url,level)        
        if os.path.isfile(path):
            os.remove(path)
            
    def setOpener(self):   
        handlers = []           
        httpHandler = urllib2.HTTPHandler(debuglevel=self.debuglevel)
        httpsHandler = urllib2.HTTPSHandler(debuglevel=self.debuglevel)
        self.cookie_jar = cookielib.MozillaCookieJar(self.cookie_file)
        
        try:
            self.cookie_jar.load(ignore_discard=True, ignore_expires=True)
        except Exception , what:
            self.cookie_jar.save(self.cookie_file,ignore_discard=True, ignore_expires=True)
        
        handlers.append(httpHandler)
        handlers.append(httpsHandler)
        handlers.append(urllib2.HTTPCookieProcessor(self.cookie_jar))
        
        if self.proxy is not None:
            #{'http':'http://XX.XX.XX.XX:XXXX'}
            proxy_support = urllib2.ProxyHandler(self.proxy)  
            handlers.append(proxy_support)
            
        if self.redirect30x == False:
            handlers.append(NoRedirectHandler)
        
        self.opener = urllib2.build_opener(*handlers)        
    def dom(self,r):
        #return PyQuery(unicode(r,'utf-8'))
        pass
        #return PyQuery(r)
    
    def wm(self,func,w_num,t_num):
        wm = PtWorkManager(func,w_num,t_num)
        wm.wait_allcomplete()
        
    def find(self,p,s):
        m = re.search(p,s)
        
        if m:
            return m.group(1)
        else:
            return ''   
    def get(self,url,info = {},timeout = 20):
        return self.urlopen(url,method = "get",data={},info =info,timeout = timeout )
    
    def post(self,url,data,info = {},timeout = 20):
        return self.urlopen(url,method = "post",data = data,info =info,timeout = timeout);
        
    def urlopen(self,url,method = 'get',data = {},info = {},timeout = 30): 
        _url = ''
        if method == "post":
            query = urllib.urlencode(data)
            _url = url
            url = url + "?" + query
            
               
        if self.cache:            
            if self.checkUrlCacheExits(url):                
                return self.getCacheContent(url)
        
        if self.opener is None:
            self.setOpener()   
            
        v = {}
        
        for k in info:
            v[k]  = info[k]
        
        v['url']     = url    
        v['local']    = self.getUrlCacheFile(url)        
        v['headers'] = ''
        v['cache']   = False
        v['body']    = ''
        
        self.setUrlCache(url,v)
                               
        try:
            if method == "get":                
                req = urllib2.Request(url)
            else:
                req = urllib2.Request(_url,query)
                            
            req.add_header("User-Agent", self.user_agent)
            r = self.opener.open(req,timeout = timeout)
        except urllib2.HTTPError, e:
            self.delUrlCache(url)
            error_log(url+"\n"+trace_back()+"\n")
            return None
        except Exception , e:
            self.delUrlCache(url)
            error_log(url+"\n"+trace_back()+"\n")
            return None   
             
        self.saveCookie()
        
        v['headers'] = dict(r.headers)  
        v['body']    = r.read()
        
        self.setUrlCache(url,v)
        r.close()
        return v 
    
    def setUrlCache(self,url,v,level = 3):
        #if self.cache == False:
        #    return        
        vv = {}
        vv['url']     = v['url']        
        vv['headers'] = v['headers']        
        vv['cache']   = True
        vv['body']    = v['body'] 
        vv['local']    = v['local']        
        cp = PtCp()        
        path = self.getUrlCacheFile(url,level)
        makeDir(os.path.dirname(path))
        cp.dump(vv, path)
        
    def saveCookie(self):
        self.cookie_jar.save(self.cookie_file,ignore_discard=True, ignore_expires=True)
        
    def getCacheContent(self,url):
        cp = PtCp()
        path = self.getUrlCacheFile(url)        
        return cp.load(path)
        
    def getResponseUrl(self,response):
        return response.geturl()
    
    def getResponseLen(self,response):
        return int(dict(response.headers).get('content-length', 0))  
    
class PtCacheHandler():
    host = ''
    root_dir = "C:\\Users\\Joseph\\Desktop\\download"

    def precess(self,buffer,url,header): 
        if buffer == '':
            try:
                buffer = urllib2.urlopen(url,None,5).read()
            except Exception,e: 
                print e
                
        self.save(buffer, url, header)

    def parseHeader(self,rawHeaderPairs):
        r = ''
        for re in rawHeaderPairs:
            if re[0] == 'Content-Type':
                r= re[1]
        if r and ";" in r:
            r = r.split(';')[0]
        return r
            #print re[0],re[1]
    def getMimeType(self,buffre,url,mtype):
        
        if '?' in url:
            url = url.split('?')[0]
            
        mime = MimeTypes()
        ext = os.path.splitext(url)[1]
        if mtype == 'text/html' and ext == '':
            if url[-1] == '/':
                l = len(url)-1
                
                url = url[0:-1]                         
            url = url+'/index.html'
            ext = '.html'
            
        #ext1 = mime.guess_extension(mtype,True)
        #print ext1
        mime_type = mime.guess_type(url)        
        #print url
        if ext:
            #print url
            u = urlparse.urlparse(url)
            #print u.netloc,u.path
            print self.host
            if self.host:
                root_dir = self.root_dir+"/"+self.host
                
            file_path = os.path.join(root_dir,u.netloc+u.path)
            print file_path
            #if not os.path.isfile(file_path):
            makeDir(os.path.dirname(file_path))
            f = open(file_path,"wb")            
            f.write(buffre)            
        #print url,ext,mime_type
        
    def save(self,buffre,url,header): 
        mime_type = self.parseHeader(header)        
        self.getMimeType(buffre,url,mime_type)
        
        
