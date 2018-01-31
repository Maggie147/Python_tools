#!/usr/bin/python
#-*-coding:utf-8-*- 
"""
__code__ = 'python_2.7'
__title__ = 'threading no join test'
__author__ = 'tx'
__mtime__ = '2017-09-14' 
"""

import threading  
import time  
class MyThread(threading.Thread):  
        def __init__(self,id):  
                threading.Thread.__init__(self)  
                self.id = id  
        def run(self):  
                x = 0  
                time.sleep(10)  
                print self.id  
  
if __name__ == "__main__":  
        t1=MyThread(999)  
        t1.start() 
        for i in range(5):  
                print i