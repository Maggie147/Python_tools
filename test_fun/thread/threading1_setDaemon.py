#!/usr/bin/python
#-*-coding:utf-8-*- 
"""
__code__ = 'python_2.7'
__title__ = 'threading setDaemon test'
__author__ = 'tx'
__mtime__ = '2017-09-14' 
"""

#setDaemon: child, father both run, but father end, no wait child run to end, end both.

import threading  
import time  
class MyThread(threading.Thread):  
        def __init__(self,id):  
                threading.Thread.__init__(self)  
                self.id = id  

        def run(self):  
                # x = 0  
                # time.sleep(10)  
                # print "This is " + self.getName()
                for i in range(5):  
                        time.sleep(2)  
                        print "I am the child", str(i)
  
if __name__ == "__main__":  
        t1=MyThread(999) 
        """
        把主线程A设置为守护线程, A执行结束了，就不管子线程B是否完成,一并和主线程A退出.这就是setDaemon方法的含义，这基本和join是相反的。
        此外，还有个要特别注意的：必须在start() 方法调用之前设置，如果不设置为守护线程，程序会被无限挂起。   
        """
        t1.setDaemon(True)   
        t1.start()              
        # print "I am the father thread."
        for i in range(5):  
                time.sleep(1)  
                print "I am the father", str(i)