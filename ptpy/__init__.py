#coding:utf-8
from ptwebkit import PtWebkit
from ptwebkittest import PtWebkitTestCase
from ptcurl import PtCurl
from ptamqp import PtAmqp


from ptdb import PtMySql,PtSqlite
from ptredis import PtRedis
from ptmemcache import PtMemcache
from ptcore import *



def killd():
    cmd ='ps -aux | grep "proxy/crawl"'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res = p.stdout.read().strip().split("\n")
    for r in res:
        t = r.split()
        p = subprocess.Popen("kill -9 %s" % t[3], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)