#!/usr/bin/env python
#coding=utf8

import time
import simplejson
from handler import AdminBaseHandler
from lib.route import route

@route(r'/admin/', name='admin_index11') #首页
@route(r'/admin/index.html', name='admin_index') #首页
class IndexHandler(AdminBaseHandler):    
    def get(self):
        self.render('manage/index.html')
        
        
@route(r'/admin/([^.]+).html', name='admin_index1') #首页
class DashboardHandler(AdminBaseHandler):    
    def get(self,page):
        self.render('manage/'+page+'.html')

