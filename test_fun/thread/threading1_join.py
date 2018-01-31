#!/usr/bin/python
#-*-coding:utf-8-*- 
"""
__code__ = 'python_2.7'
__title__ = 'threading join test'
__author__ = 'tx'
__mtime__ = '2017-09-14' 
"""

#join: father thread wait befor join child , than run other

import threading  
import time  
class MyThread(threading.Thread):  
        def __init__(self,id):  
                threading.Thread.__init__(self)  
                self.id = id  
        def run(self):  
                # x = 0  
                # time.sleep(10)  
                # print self.id 
                for i in range(5):  
                        time.sleep(2)  
                        print "I am the child", str(i) 
  
if __name__ == "__main__":  
        t1=MyThread(999)  
        # t1.setDaemon(True)
        t1.start()          # join: main thread wait t1 end. bei join 
        t1.join()        
        for i in range(5):  
                time.sleep(1)  
                print "I am the father", str(i)