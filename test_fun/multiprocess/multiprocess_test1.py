#!/usr/bin/python
#-*-coding:utf-8-*- 
import multiprocessing
import time

def process(num):
	time.sleep(num)
	print 'Process: ', num


def main():
	for i in range(5):
		p = multiprocessing.Process(target=process, args=(i,))
		p.start()

	print("CPU number:" + str(multiprocessing.cpu_count()))

	for p in multiprocessing.active_children():
		print('Child process name: ' + p.name + 'id: ' + str(p.pid))

	print('Process Ended')
	
if __name__ == '__main__':
	main()
