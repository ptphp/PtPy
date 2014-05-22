#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import subprocess
import threading
import time
"""Simplified chat demo for websockets.

Authentication, error handling, etc are left as an exercise for the reader :)
"""

import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload
import tornado.websocket
import os.path
import uuid

from tornado.options import define, options

   

class MonitorLog(threading.Thread):
    wc = None
    def __init__(self,wc):
        threading.Thread.__init__(self)  
        self.wc = wc
        
    def run(self):
        popen=subprocess.Popen(['tail','-f','out.log'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        pid=popen.pid
        logging.info('Popen.pid:%s',str(pid))  
        while True:  
            line=popen.stdout.readline().strip()
            #line =popen.communicate()
            logging.info("output:%s" % (line))
            self.wc.do_response_msg(line)
            if subprocess.Popen.poll(popen) is not None:  
                break

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/chatsocket", ChatSocketHandler),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            debug = True
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", messages=ChatSocketHandler.cache)

class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    cache_size = 200
    
    def allow_draft76(self):
        # for iOS 5.0 Safari
        return True

    def open(self):
        print "open"
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        print "close"
        ChatSocketHandler.waiters.remove(self)

    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

    @classmethod
    def send_updates(cls, chat):
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)
                
    def do_response_msg(self,msg):
        chat = {
            "id": str(uuid.uuid4()),
            "body":msg,
            }
        chat["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=chat))

        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)
        
    def on_message(self, message):
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        global myqueue
        if "start" in parsed.keys():            
            print parsed
            m = MonitorLog(self)
            m.start()
  
                    
define("port", default=8880, help="run on the given port", type=int)
define("host", default="127.0.0.1", help="run on the given host", type=str)

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    logging.info("server start http://%s:%d", options.host,options.port)
    loop = tornado.ioloop.IOLoop.instance().start()
    
if __name__ == "__main__":
    main()
