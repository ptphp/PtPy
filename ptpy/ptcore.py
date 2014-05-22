import os
import shutil
import subprocess
import random
import sys
import hashlib
import traceback
from time import time
import json
from urllib import unquote
import cPickle

user_agents = [
    'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; ja; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; ja; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; ja; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13 (.NET CLR 3.5.30729)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.215 Safari/534.10',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; ja; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.6) Gecko/20060728 Firefox/1.5.0.6',
    'Mozilla/5.0 (X11; Linux i686) AppleWebKit/536.11 (KHTML, like Gecko) Ubuntu/12.04 Chromium/20.0.1132.47 Chrome/20.0.1132.47 Safari/536.11',
    'Opera/9.80 (Windows NT 5.1; U; ja) Presto/2.6.30 Version/10.63'
]


def ptston(cls, *args, **kw):  
    """
    @ptston
    class Classname()    
    """
    instances = {}  
    def _ptston():  
        if cls not in instances:  
            instances[cls] = cls(*args, **kw)  
        return instances[cls]  
    return _ptston

def dirList(path):
    lists = os.listdir(path)
    return lists

        
def rmDir(path):   
    path = os.path.abspath(path) 
    if os.path.isdir(path):
        shutil.rmtree(path)

def makeDir(path):    
    path = os.path.abspath(path)
    
    if os.path.isfile(path):
        path = os.path.dirname(path)
                
    if os.path.isdir(path) == False:
        makeDir(os.path.dirname(path))
        return os.mkdir(path)    
    return True

def error_log(msg):    
    msg = str(msg)
    f = open("error.log",'a+')
    f.write(msg+"\n")
    f.close()  
    

def trace_back():  
    try:          
        info = sys.exc_info()
        res = "\nException %s: %s \n" % info[:2]
        for file, lineno, function, text in traceback.extract_tb(info[2]):
            file = file.split("\\")[-1]
            res = "%s Line( %d ) in function [ %s ] : %s  ==> %s \n" % (res,lineno,function,file,text)
        return res
        #return traceback.format_exc()  
    except:  
        return '' 
    
def parseNetstat(res):
        pids = []
        try:
            d =  res.split("\r\n")
            for r in d:
                if r:
                    pid = r.split()[-1]
                    if int(pid) >0:
                        pids.append(int(pid))
        except:
            pass
        return pids
    

def getPidByPort(port):
    cmd ="netstat -nao | findstr :%d" % port
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res = p.stdout.read()
    if res:
        return parseNetstat(res)
    else:
        return []

def killPidByPort(port):
    pids = getPidByPort(port)
    #debug = PtDebug()
    for pid in pids:
        t =  "kill PID :%d" % pid
        #debug.dump(t)
        res = os.popen("taskkill /PID %d /F" % pid)
        #print res.read()
        #os.kill(pid,9)
        #TASKKILL /F /IM WinRAR.exe

def randomSleep():
    r = random.randrange(10)/100.0
    time.sleep(r)


def hex_md5(s):
    return hashlib.md5(str(s)).hexdigest()
def pathHashDir(s,level = 2):    
    h = hashlib.md5(str(s)).hexdigest()
    p = '';
    for i in range(0,level):        
        p = os.path.join(p,str(h[i]))
    return p


@ptston
class Tools(object):
    def run(self,path,param):        
        cmd = r"%s %s" % (path,param)
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

@ptston
class PtCp(object):
    def dump(self,content,path): 
        f = open(path,"w")
        cPickle.dump(content,f)
        f.close()
    def load(self,path):
        f = open(path,"r")        
        r = cPickle.load(f)
        f.close()
        return r

@ptston
class PtFile(object):    
    def set(self,path,content,append = False):
        makeDir(os.path.dirname(os.path.dirname(os.path.abspath(path))))
        if append:            
            f = open(path,"a+")
        else:
            f = open(path,"w")            
        f.write(content)
        f.close()
        
    def get(self,path):
        f = open(path,"r")
        content = f.read()
        f.close()
        return content

class PtError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
@ptston
class PtDebug(object):
    traceData = []
    def dump(self,data):
        self.traceData.append(data)
    def trace(self,data):
        res = ""
        for row in self.traceData:
            res += "<p>"
            res += json.dumps(row)
            res += "</p>"
        #res =  res.replace("\"","\\\"")
        res =  res.replace("\"","'")
        return res
class Dynload():
    """
    packageName = _data['_package']
    className = _data['_class']
    methodName = _data['_function']
    
    #dyn=Dynload(packageName,['*'])
    
    #ins=dyn.getClassInstance(className)
    #res = dyn.execMethod(ins, methodName)
    #dyn.execfunc('test','Hello','function!')
    
    #print packageName,className,methodName
    the_class = getattr(__import__(packageName, globals(), locals(),['*'], -1),className)
    instance = the_class()
    method = getattr(instance, methodName)
    #print method
    res = method(_data['_args'])        
    result['data'] = res      
    """
    def __init__(self,package,imp_list):
        self.package=package
        self.imp=imp_list
    def getobject(self):
        return __import__(self.package, globals(), locals(),self.imp, -1)
    def getClassInstance(self,classstr,*args):
        return getattr(self.getobject(),classstr)(*args)    
    def execfunc(self,method,*args):
        return getattr(self.getobject(),method)(*args)
    def execMethod(self,instance,method,*args):
        return getattr(instance,method)(*args)

def urldecode(url):
    result={}
    url=url.split("?",1)
    if len(url)==2:
        for i in url[1].split("&"):
            i=i.split("=",1)
            if len(i)==2:
                result[unquote(i[0])]=unquote(i[1])
    return result

@ptston
class PtRar(object):
    def test(self,path):
        r = subprocess.call('winrar t -r -y -ibck {0} '.format(path), shell=True)  
        return int(r) == 0
    def list(self,path):
        return 
    def unrar(self,path,undir):
        #undir mush be "/" end
        r = subprocess.call('winrar x -y -ibck {0} {1}'.format(path,undir), shell=True)  
    def ys(self,dir,path):    
        #WinRAR a Pictures.rar -r Bitmaps\*
        #os.chdir(dir)
        r = subprocess.call('winrar a -r -y -ep1 -ibck {0} {1}'.format(path,dir), shell=True) 
          