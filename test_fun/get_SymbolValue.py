#!/usr/bin/python
"""
__title__ = 'get_SymbolValue_2.7'
__author__ = 'xxxx'
__mtime__ = '2017-02-10'
"""
import os
import sys
import string
import StringIO,gzip

def get_SymbolValue(buf, symbol):

	buf_list = []

	begin = 0

	if symbol['cut'] == "1":
		while True:

			head_1 = buf[begin:].find(symbol['Head'])

			if head_1 == -1:
				break

			begin2 = begin + head_1 + len(symbol['Head'])


			head_2 = buf[begin2:].find(symbol['Head'])

			if head_2 == -1:
				end = begin2
				buff = buf[begin:]
			else:
				end = begin2 + head_2

				buff = buf[begin:end]

			begin = end

			buf_list.append(buff)
	else:
		buf_list.append(buf)

	return buf_list


def main():
	buf = "aaaaaafhsifjdasjbbbbbbaaaaaafasfjasfbjfabbbbbbaaaaaafegggs"
	mark = 1
	cut = {"cut":"1", "Head":"aaaaaa", "Tail":"bbbbbb"}

	buf_list = []
	buf_list = get_SymbolValue(buf, cut)

	for i in buf_list:
		print i



if __name__ == "__main__":

    main()