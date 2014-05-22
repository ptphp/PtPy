# coding: utf-8
import unittest,time
from ptpy.ptamqp import PtAmqp
class test_ptamqp(unittest.TestCase):
    def setUp(self):
        self.amq = PtAmqp()
        self.amq .connect()
        self.amq.queue_declare("hello")
    def test_push(self):
        #sudo rabbitmqctl list_queues
        amq = self.amq
        for i in range(200):
            amq.push("from python 中文 i:"+str(i))
            time.sleep(1)
        amq.close()
    def test_pull(self):
        amq = self.amq
        def callback(ch, method, properties, body):
            print " [x] Received %s" % (body,)
        amq.pull(callback)

if __name__ == '__main__':
    unittest.main()
