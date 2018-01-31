#!/usr/bin/python

import os
import sys
import time
import binascii


# reload(sys)
# sys.setdefaultencoding('utf8')


def FindRelation(inbuf):
	output = []
	begin = 0

	while True:

		place1 = inbuf[begin:].find(" ")

		if place1 == -1:
			break  

		begin2 = begin + place1 + len(" ")
		place2 = inbuf[begin2:].find(" ")  

		if place2 == -1:
			end = begin2
			buff = inbuf[begin:]
		else:

			end = begin2 + place2

			buff = inbuf[begin:end]

		begin = end
		output.append(buff)

	return output




def main():
	buf = "04 f2 0b 1b 10 fe 6f ad ae c0 f9 96 a3 96 98 f6 e7 6f de b8 23 36 55 7e 3b 4a 4c b6 92 50 24 d3 3a ad 0d 34 d2 aa f3 a0 69 63 3b 1e 35 1f 66 6e b3 3f 77 54 ed 07 71 39 41 54 9a 68 a7 a7 db a6 fd"

	value = FindRelation(buf)

	value_list = ""

	for i in value:
		a = "\\x" + str(i)
		print a
		a = a.replace(' ', '')
		a = a.strip()
		value_list = value_list + a

	# value_list = value_list.replace('', ' ')
	value_list = value_list.strip()

	print value_list

	# print "\\x"

if __name__ == "__main__":
    main()
