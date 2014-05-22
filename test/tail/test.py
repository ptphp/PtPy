#!/usr/bin/python
# encoding=utf-8
import subprocess
import threading

#https://github.com/kasun/python-tail
#http://ihavegotyou.iteye.com/blog/1987792
g_output_log = []

def monitorLog():
    global g_output_log
    popen=subprocess.Popen("tail -f -n 10 test.py",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    pid=popen.pid
    print('Popen.pid:'+str(pid))  
    while True:  
        line=popen.stdout.readline().strip()
        #line =popen.communicate()
        print "output:%s" %(line)
        g_output_log.append(line)
        if subprocess.Popen.poll(popen) is not None:  
            break
    print('DONE') 
     
if __name__ == '__main__':
    tcpdump = threading.Thread(name='tcpdump', target=monitorLog)  
    tcpdump.start()
    