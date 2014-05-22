#!/usr/bin/env python
#coding=utf8

import logging
from tornado.web import HTTPError
from tornado.web import asynchronous
from handler import BaseHandler
from lib.route import route
from tornado.ioloop import IOLoop
import time
import os
import subprocess
import tornado.iostream

@route(r'/tools/tail', name='tools_tail') #
class TailHandler(BaseHandler):
    @asynchronous
    def get(self):
        file_path = "tail.txt"            
        self.file = open(file_path, "r")
        self.pos = self.file.tell()
        def _read_file():
            line = self.file.read()
            last_pos = self.file.tell()
            if not line:
                self.file.close()
                self.file = open(file_path, 'r')
                self.file.seek(last_pos)
                pass
            else:
                self.write(line)
                self.flush()
            IOLoop.instance().add_timeout(time.time() + 1, _read_file)            
        _read_file()

@route(r'/tools/tail1', name='tools_tail1') #
class Tail1Handler(BaseHandler):
    @asynchronous
    def get(self):
        print "GOT REQUEST"
        self.p = subprocess.Popen(
            ["tail", "-f", "tail.txt", "-n+1"],
            stdout=subprocess.PIPE)

        self.write("<pre>")
        self.write("Hello, world\n")
        self.flush()

        self.stream = tornado.iostream.PipeIOStream(self.p.stdout.fileno())
        self.stream.read_until("\n", self.line_from_nettail)

    def on_connection_close(self, *args, **kwargs):
        """Clean up the nettail process when the connection is closed.
        """
        print "CONNECTION CLOSED!!!!"
        self.p.terminate()
        tornado.web.RequestHandler.on_connection_close(self, *args, **kwargs)

    def line_from_nettail(self, data):
        self.write(data)
        self.flush()
        self.stream.read_until("\n", self.line_from_nettail)