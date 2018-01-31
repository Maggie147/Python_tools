#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'python_2.7 urlget_v1.0'
__author__ = 'xxxx'
__mtime__ = '2017-04-25'

"""

import sys
import os
import urllib
import urllib2
import re
# import cookielib
# import gzip

# sys.path.append("../Common/pylib")
reload(sys)
sys.setdefaultencoding('utf8')


def usage(processName):
	print "Usage: %s URL  Path" % processName
	print "For example:"
	print "		..."


def getPage(debug=0, para={}, s= "get Page starting..."):
	print s
	print "get page URL: ", para['URL']
	# headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}	
	data = None
	req = urllib2.Request(para['URL'])

	try:
		response = urllib2.urlopen(req)

		page = response.read()
		# print page

		type = sys.getfilesystemencoding()
		# print type
		data = page.decode(type).encode('utf8')
		# print data
		return data

	except urllib2.HTTPError as e:
		print "The server couldn't fulfill the request"
		print "Error code: ", e.code
		print "Return content: ", e.read()

	except urllib2.URLError as e:
		print "Failed to reach the "
		print e.reason

	else:
		#other thing
		pass

	filenName = para['Path']
	if filenName is not None:
		print "SavePage Path: ", filenName
		f = open(filenName, "wb")
		f.write(pageData)
		f.close


def getURL(debug=0, para={}, s= "get URL starting..."):
	print s
	f = open(para['Path'], "r")
	cotent = f.read()
	f.close()

	webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
	# webpage_regex = re.compile(r'\".*?\"', re.IGNORECASE)

	urlFile = open('../File/url.dat', 'w')
	target_url = webpage_regex.findall(cotent)
	print "all URL: "
	for i in range(len(target_url)):
		# print target_url[i]
		print >> urlFile, target_url[i]

	urlFile.close()


def main():

	para = {}

	argc = len(sys.argv)
	if argc == 1:
		para['URL']  = "http://www.baidu.com"   #http://www.sina.com.cn/
		para['Path'] = "../File/savePage.html"
	elif argc == 3:
		para['URL'] = sys.argv[1]
		para['Path'] = sys.argv[2]
	else:
		usage(sys.argv[0])
		sys.exit(-1)

	getPage(1, para)

	getURL(1, para)
	print "GoodBye!"


if __name__ == "__main__":

	main()