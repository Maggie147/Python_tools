#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'python_2.7 httpget_v1.0'
__author__ = 'xxxx'
__mtime__ = '2017-04-25'

"""

import sys
import urllib
import urllib2
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
		# response = opener.open(req)

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


def savePage(debug=0, para={}, s="Start..."):
	print s
	pageData = getPage(debug, para)
	if pageData is None:
		print "getPage failed!"
		return

	filenName = para['Path']

	if filenName is not None:
		print "SaveFile Path: ", filenName
		f = open(filenName, "wb")
		f.write(pageData)
		f.close


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

	savePage(1, para)


if __name__ == "__main__":

	main()