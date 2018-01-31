#!/usr/bin/python
#-*-coding:utf-8-*- 
from multiprocessing import Process
import time

class MyProcess(Process):
	def __init__(self, loop):
		Process.__init__(self)
		self.loop = loop

	def run(self):
		for count in range(self.loop):
			time.sleep(1)
			print('Pid: ' + str(self.pid) + ' LoopCount: ' + str(count))


def main():
	for i in range(2, 5):
		p = MyProcess(i)
		p.daemon = True
		p.start()
		p.join()
	
	print "Main process Ended!"

if __name__ == '__main__':
	main()
