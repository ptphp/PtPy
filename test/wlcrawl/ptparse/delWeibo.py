#delWeibo.py
# -*- coding: utf-8 -*-
from urllib import urlencode
from StringIO import StringIO
from sys import argv
from urlparse import parse_qsl
import pycurl
import re
#以上为本脚本的依赖
 
b = StringIO()
c = pycurl.Curl()
#这两行定义对象，c为cURL，用以发送http请求，b用于存放cURL得到的response
 
def fake_write(x):pass
 
def sigint(signum, frame):
    global b, c
    del b, c
    import sys
    print '\n\nsigint received, exiting...'
    sys.exit()
 
import signal
signal.signal(signal.SIGINT, sigint)
 
def reset():	#清空对象
    b.truncate(0)
    c.reset()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.COOKIEJAR, 'cookies.txt')
#cookies.txt存放登录得到的cookies
    c.setopt(pycurl.FOLLOWLOCATION, True)
    return b, c
 
def login(username, password):
    reset()
    c.setopt(pycurl.URL, 'http://3g.sina.com.cn/prog/wapsite/sso/login_submit.php')
    c.perform()
 
    data = b.getvalue()
    vk = re.search(r'''name="vk"\s+?value="(.*?)"''', data).group(1)
    pname = re.search(r'''name="password_(\d+)"''', data).group(1)
 
    reset()
    c.setopt(pycurl.POST, True)
    c.setopt(pycurl.URL, 'http://3g.sina.com.cn/prog/wapsite/sso/login_submit.php')
    c.setopt(pycurl.POSTFIELDS, urlencode({
        'mobile': username,
        'password_'+pname: password,
        'vk': vk,
        'remember': 'on',
        'submit': '1'
    }))
#以上post参数通过curl发送到login_submit.php
    c.perform()
    return b.getvalue()
 
def del_tweets():
    while True:
        reset()
        c.setopt(pycurl.URL, 'http://t.sina.cn/dpool/ttt/home.php?cat=1')
        c.perform()
	#获取包含tweets的页面
        data = b.getvalue()
        data =  re.findall(r'href="mblogDeal\.php\?([^"]+?act=del[^"]+)"', data)
	#这两行用正则表达式得到tweets的id
        if not data:
            break
        for i in data:
            j = parse_qsl(i)
            qs = dict(j)
            qs['act'] = 'dodel'
            qs = '&'.join(['='.join(k) for k in qs.items()])
            url = 'http://t.sina.cn/dpool/ttt/mblogDeal.php?' + qs
	#得到删除所有tweets的url列表
 
            reset()
            c.setopt(pycurl.WRITEFUNCTION, fake_write)
            c.setopt(pycurl.URL, url)
            try:
                c.perform()
                print url
            except:pass
 
def unfollow():
    while True:
        reset()
        c.setopt(pycurl.URL, 'http://t.sina.cn/dpool/ttt/attention.php?cat=0')
        c.perform()
        data = b.getvalue()
        data =  re.findall(r'href="attnDeal\.php\?([^"]+?act=del[^"]+)"', data)
        if not data:
            break
        for i in data:
            j = parse_qsl(i)
            qs = dict(j)
            qs['act'] = 'delc'
            qs = '&'.join(['='.join(k) for k in qs.items()])
            url = 'http://t.sina.cn/dpool/ttt/attnDeal.php?' + qs
 
            reset()
            c.setopt(pycurl.WRITEFUNCTION, fake_write)
            c.setopt(pycurl.URL, url)
            try:
                c.perform()
                print url
            except:pass
 
def remove_followers(black=False):
    while True:
        reset()
        c.setopt(pycurl.URL, 'http://t.sina.cn/dpool/ttt/attention.php?cat=1')
        c.perform()
        data = b.getvalue()
        data =  re.findall(r'href="attnDeal\.php\?([^"]+?act=remove[^"]+)"', data)
        if not data:
            break
        for i in data:
            j = parse_qsl(i)
            qs = dict(j)
            qs['act'] = 'removec'
            if black:
                qs['black'] = '1'
            qs = '&'.join(['='.join(k) for k in qs.items()])
            url = 'http://t.sina.cn/dpool/ttt/attnDeal.php?' + qs
 
            reset()
            c.setopt(pycurl.WRITEFUNCTION, fake_write)
            c.setopt(pycurl.URL, url)
            try:
                c.perform()
                print url
            except:pass
 
if __name__ == '__main__':
    username, password = argv[1:]
#从命令行中获取参数，存放于username和password变量
    login(username, password)
#登录
    del_tweets()
#删除tweets
    #unfollow()
    #remove_followers()