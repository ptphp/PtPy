#!/usr/bin/env python
#coding=utf8
import os
import time
import signal
import logging
import memcache

import tornado.web
import tornado.autoreload
import tornado.testing
from tornado.httpserver import HTTPServer
from tornado.options import define, parse_command_line, options

from jinja2 import Environment, FileSystemLoader
from jinja2 import MemcachedBytecodeCache

from lib.filter import register_filters
from lib.route import Route
from lib.session import MemcacheSessionStore
from lib.tests import BaseHandlerTestCase,BaseTestCase  # @UnresolvedImport

from handler import site, admin, user

from config import settings  # @UnresolvedImport
import urllib


class HandlerTestCase(BaseHandlerTestCase):
    def get_app(self):
        settings['debug'] = True
        settings['xsrf_cookies'] = False
        return Application(settings)

class Application(tornado.web.Application):
    def __init__(self,settings):
        bcc = None
        self.memcachedb = memcache.Client([settings['memcache_host']])
        self.session_store = MemcacheSessionStore(self.memcachedb)
        if settings['debug'] == False:
            bcc = MemcachedBytecodeCache(self.memcachedb)
            
        self.jinja_env = Environment(
                    loader = FileSystemLoader(settings['template_path']),
                    bytecode_cache = bcc,
                    auto_reload = settings['debug'],
                    autoescape = False)

        self.jinja_env.filters.update(register_filters())
        self.jinja_env.tests.update({})
        self.jinja_env.globals['settings'] = settings
        
        handlers = [
                    tornado.web.url(r"/style/(.+)", tornado.web.StaticFileHandler, dict(path=settings['static_path']), name='static_path'),
                    tornado.web.url(r"/upload/(.+)", tornado.web.StaticFileHandler, dict(path=settings['upload_path']), name='upload_path')
                    ] + Route.routes()
        #print settings['debug']
        tornado.web.Application.__init__(self, handlers, **settings)


def runserver():
    if options.debug == True:        
        settings['debug'] = True
    else:
        settings['debug'] = False

    logging.info('Server debug mode : %s',settings['debug'])

    http_server = HTTPServer(Application(settings), xheaders=True)
    http_server.listen(options.port)
    
    loop = tornado.ioloop.IOLoop.instance()
    logging.info('Server autoreload apply ...')
    tornado.autoreload.start(loop)    
    def shutdown():
        logging.info('Server stopping ...')
        http_server.stop()
        
        logging.info('IOLoop wil  be terminate in 1 seconds')   
        deadline = time.time() + 1
        
        def terminate():
            now = time.time()
            
            if now < deadline and (loop._callbacks or loop._timeouts):
                loop.add_timeout(now + 1, terminate)
            else:
                loop.stop()
                logging.info('Server shutdown')
        
        terminate()
    
    def sig_handler(sig, frame):
        logging.warn('Caught signal:%s', sig)
        loop.add_callback(shutdown)
    
    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)
    
    logging.info('Server running on \nhttp://127.0.0.1:%d'%(options.port))
    loop.start()


define('debug', default=False, metavar='True|False',type=bool)
define('port', default=8081, type=int)

if __name__ == '__main__':
    parse_command_line()    
    runserver()
