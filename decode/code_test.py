#!/usr/bin/python
#-*-coding:utf-8-*- 

import codecs
import binascii
import urllib

s= "张三"
print s
if isinstance(s, unicode):
	print s.encode('gb2312')
else:
	print s.decode('utf-8').encode('gb2312')
ss = binascii.b2a_hex(s)
print ss
print binascii.a2b_hex("e5bca0e4b889")

print"______"


a = "123abc"
print a.encode('ascii')
print bytes(a)

print "bbbb ++++++"
b = u"你好啊"
print binascii.b2a_hex(b.encode('utf-8'))   # utf-8 hex
print binascii.b2a_hex(b.encode('gbk'))     # gbk hex
print binascii.b2a_hex(b.encode('gb2312'))  # gb2312 hex

print "++++++"
print binascii.a2b_hex("e4bda0e5a5bde5958a").decode('utf-8')

print "c ++++++"
c = "Hello"
print binascii.b2a_hex(c)
print "48656c6c6f".decode('hex')

print "d ++++++"
d = "张三"
print binascii.b2a_hex(d)    						#utf-8  hex 
print "e5bca0e4b889".decode('hex')


print "f   ++++++"*40
print "-"*40
f = "是的"
print binascii.b2a_hex(f.decode('utf-8').encode('gbk'))   # gbk hex  "d5c5c8fd"
print binascii.a2b_hex("d5c5c8fd")
print binascii.a2b_hex("d5c5c8fd").decode('gbk')


print "__"*40

print "g   ++++++"
g = "3540731440"
print hex(3540731440)
print binascii.b2a_hex(g)
print bytes(g)


print "f   ++++++"
f = "1182813588"
print binascii.b2a_hex(f)
print bytes(f)

print "aaaaaaaa"
hh = "222222222"
print binascii.b2a_hex(hh)




# print "h   ++++++"
# h = "572610158"
# print binascii.b2a_hex(h)
# print bytes(h)

# print "e   ++++++"
# e = "1976946719"
# print binascii.b2a_hex(e)
# print bytes(e)

print "____________"
teststr = '\x75\xd5\xd0\x1f'
print teststr

print "____________"
teststr = '\xe9\x93\x81\xe5\x83\x8f'
print teststr


print "____________"
teststr = '\xe5\x87\xba\xe5\x85\xa5'
print teststr
'''
print"11111111111111_______________________________"

a = str("%D0%C2%C8%CB%B1%A8%B5%C0%A3%AC%C7%EB%B6%E0%B6%E0%B9%D8%D5%D5")
b = a.replace("%", "")
print b 
print binascii.a2b_hex(b)

print binascii.a2b_hex(b).decode("gb2312")

print binascii.b2a_hex(urllib.unquote(a))

print urllib.unquote(a).decode("gb2312", "unicode-escape")
'''