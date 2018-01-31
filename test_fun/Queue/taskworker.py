#!/usr/bin/python
#-*-coding:utf-8-*- 
"""
__code__ = 'python_2.7'
__title__ = 'taskworker.py'
__author__ = 'tx'
__mtime__ = '2017-10-20' 
"""

import random  
import time
import Queue
import sys
from multiprocessing.managers import BaseManager


# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass

# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')


server_addr = '127.0.0.1'
# server_addr = '192.168.248.200'
print "Connect to server %s..."% server_addr

# 端口和验证码注意保持与taskmanager.py设置的完全一致:
worker = QueueManager(address=(server_addr, 5000), authkey='abc')
worker.connect()

# 获得通过网络访问的Queue对象:
task = worker.get_task_queue()
result = worker.get_result_queue()

# 从task队列取任务,并把结果写入result队列:
for i in range(10):
	try:
		n = task.get(timeout=1)
		print "run task %d * %d..."%(n, n)
		r = '%d * %d = %d'%(n, n, n*n)
		time.sleep(1)
		result.put(r)

	except Queue.Empty:     
		print 'task queue is empty.'

print "worker exit."

    
  
# if __name__ == "__main__":
#     test()