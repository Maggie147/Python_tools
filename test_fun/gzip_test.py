#!/usr/bin/python

import os
import sys
import urllib2,httplib
import StringIO,gzip

def processFile(inputfile, outputfile):
	fin = open(inputfile, 'r')
	fout = open(outputfile, 'w')

	fp = fin.read(1024)
	pos = fp.find("\r\n\r\n")
	print pos
	fin.seek(pos)
	fin.tell()
	data = fp.split("\r\n\r\n")[1]
	compressedstream = StringIO.StringIO(data)
	gziper = gzip.GzipFile(fileobj=compressedstream)
	data2 = gziper.read()
	print "hello"
	print data2
	fout.write(data2)

	fin.close()
	fout.close()

def main():
	processFile('/home/ls/study_python_test/test.txt', '/home/ls/study_python_test/out.txt')
 	