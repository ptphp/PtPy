#!/usr/bin/env python
# coding: utf-8
__author__ = 'Amy'
import pika

class PtAmqp:
    conn = None
    channel = None
    host = "al.ptphp.com"
    queue = None
    def connect(self):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(
               self.host))
        self.channel = self.conn.channel()
    def queue_declare(self,q):
        self.channel.queue_declare(queue=q)
        self.queue = q

    def push(self,msg):
        self.channel.basic_publish(exchange='',
                      routing_key=self.queue,
                      body=msg)
        print " [x] Sent '"+msg+"'"

    def pull(self,callback):
        print ' [*] Waiting for messages. To exit press CTRL+C'
        self.channel.basic_consume(callback,
                              queue=self.queue,
                              no_ack=True)
        self.channel.start_consuming()

    def close(self):
        self.conn.close()