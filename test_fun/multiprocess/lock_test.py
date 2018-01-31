#!/usr/bin/python
#-*-coding:utf-8-*- 
from multiprocessing import Process, Lock
import time

class MyProcess(Process):
	def __init__(self, loop, lock):
		Process.__init__(self)
		self.loop = loop
		self.lock = lock

	def run(self):
		for count in range(self.loop):
			time.sleep(1)
			self.lock.acquire()
			print('Pid: ' + str(self.pid) + ' LoopCount: ' + str(count))
			self.lock.release()

def main():
	lock = Lock()
	for i in range(10, 15):
		p = MyProcess(i, lock)
		p.start()

	print "Main process Ended!"

if __name__ == '__main__':
	main()
