#!/usr/bin/env python
#coding=utf8

import datetime
import logging
from handler import UserBaseHandler
from lib.route import route
from lib.util import vmobile

@route(r'/user', name='user') #用户后台首页
class UserHandler(UserBaseHandler):    
    def get(self):
        user = self.get_current_user()
        try:
            self.session['user'] = user
            self.session.save()
        except:
            pass
        
        self.render('user/index.html')

@route(r'/user/profile', name='user_profile') #用户资料
class ProfileHandler(UserBaseHandler):
    
    def get(self):
        self.render('user/profile.html')
    
    def post(self):        
        self.redirect('/user/profile')
