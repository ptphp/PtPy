import threading
from datetime import datetime
import Queue
from ptcore import trace_back,error_log

"""
wm = PtWorkManager("func",1100000,111)
wm.wait_allcomplete()
"""

class PtWorkManager(object):
    def __init__(self, func=None,work_num=1000,thread_num=2):        
        self.work_queue = Queue.Queue()
        self.threads = []
        self.__init_work_queue(func,work_num)
        self.__init_thread_pool(thread_num)            

    def __init_thread_pool(self,thread_num):
        for i in range(thread_num):
            self.threads.append(PtWork(self.work_queue))

    def __init_work_queue(self, func,jobs_num):
        for i in range(jobs_num):
            self.add_job(func, i)
 
    def add_job(self, func, *args):
        #self.work_queue.put((func, list(args)))
        self.work_queue.put((func, list(args)[0]))
        
    def stop(self):
        for item in self.threads:
            item.stop()
            
    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive():item.join()
def getNow():           
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
class PtWork(threading.Thread,object):
    isRun = True
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()
    def stop(self):
        self.isRun = False
    def run(self):        
        while self.isRun:
            try:
                do, args = self.work_queue.get(block=False)  
                do(args)
                self.work_queue.task_done()
            except Exception , e:                    
                if str(type(e)) != "<class 'Queue.Empty'>":                
                    error_log(trace_back())                    
                break
            
def getThread():
    return threading.currentThread()

def getThreadName():
    return threading.currentThread().getName()
