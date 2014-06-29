#!/usr/bin/env python
#coding=utf8

import logging
from tornado.web import HTTPError
from handler import BaseHandler
from lib.route import route

@route(r'/', name='index') #首页
class IndexHandler(BaseHandler):    
    def get(self):    
        print 11            
        self.render("site/index.html",test=1)


@route(r'/signin', name='signin') #登录
class SignInHandler(BaseHandler):    
    def get(self):
        if self.get_current_user():
            self.redirect("/")
            return
        
        oauth = None
        if 'oauth' in self.session:
            oauth = self.session['oauth']
        
        self.render("site/signin.html", oauth = oauth, next = self.next_url)
    
    def post(self):
        if self.get_current_user():
            self.redirect("/")
            return
        
        mobile = self.get_argument("mobile", None)
        password = self.get_argument("password", None)
        
        if mobile and password:
            try:
                pass
            except Exception, ex:
                logging.error(ex)
                self.flash("此用户不存在")
        else:
            self.flash("请输入用户名或者密码")
        
        self.render("site/signin.html", next = self.next_url)

@route(r'/signup', name='signup') #注册
class SignUpHandler(BaseHandler):
    
    def get(self):
        if self.get_current_user():
            self.redirect("/")
            return
        
        oauth = None
        if 'oauth' in self.session:
            oauth = self.session['oauth']
        
        self.render("site/signup.html", oauth = oauth)
    
    def post(self):
        if self.get_current_user():
            self.redirect("/")
            return
        
        mobile = self.get_argument("mobile", None)
        password = self.get_argument("password", None)
        apassword = self.get_argument("apassword", None)
        vcode = self.get_argument("vcode", None)
        
        self.render("site/signup.html")

@route(r'/signout', name='signout') #退出
class SignOutHandler(BaseHandler):
    
    def get(self):
        if "user" in self.session:
            del self.session["user"]
            self.session.save()
        self.redirect(self.next_url)

@route(r'/resetpassword', name='resetpassword') #忘记密码
class ResetPasswordHandler(BaseHandler):
    
    def get(self):
        if self.get_current_user():
            self.redirect("/")
            return
        
        self.render("site/resetpassword.html")
        
    def post(self):
        self.render("site/resetpassword.html")

@route(r'/p/([^/]+)', name='staticpage') #栏目页
class StaticPageHandler(BaseHandler):
    
    def get(self, slug):
        try:
            page = Page.get(slug = slug)
        except:
            raise HTTPError(404)
            return        
        self.render("static/%s" % page.template, page = page)