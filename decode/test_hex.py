#!/usr/bin/python
#-*-coding:utf-8-*- 



import codecs

str = '\xcf\xc2\xb0\xb2\xd7\xb0'

print str.decode('gbk').encode('utf-8')