#!/usr/bin/python
#-*-coding:utf-8-*- 
"""
__code__ = 'python_2.7'
__title__ = 'taskmanager.py'
__author__ = 'tx'
__mtime__ = '2017-10-20' 
"""

import random  
import time
import Queue
from multiprocessing.managers import BaseManager
#multiprocessing模块不但支持多进程，其中managers子模块还支持把多进程分布到多台机器上.

# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass


# 发送任务的队列:
task_queue = Queue.Queue()

# 接收结果的队列:
result_queue = Queue.Queue()


# 把两个Queue都注册到网络上, callable参数关联了Queue对象:
QueueManager.register('get_task_queue', callable=lambda: task_queue)
QueueManager.register('get_result_queue', callable=lambda: result_queue)

# 绑定端口5000, 设置验证码'abc':
manager = QueueManager(address=('', 5000), authkey='abc')

# 启动Queue:
manager.start()

# 获得通过网络访问的Queue对象:
task = manager.get_task_queue()
result = manager.get_result_queue()

# 放几个任务进去:
for i in range(10):
    n = random.randint(0, 10000)
    print 'Put task %d' % i
    print n
    task.put(n)

# 从result队列读取结果:
print 'Try get result...'
for i in range(10):
        r = result.get(timeout=10)
        print 'Result: %s' % r
# 关闭:
manager.shutdown()

    
  
# if __name__ == "__main__":
#     test()