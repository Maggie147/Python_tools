#!/usr/bin/python
#-*-coding:utf-8-*- 

import codecs
import binascii
import urllib

print"begin_______________________________"

a = str("%D0%C2%C8%CB%B1%A8%B5%C0%A3%AC%C7%EB%B6%E0%B6%E0%B9%D8%D5%D5")
print a

b = a.replace("%", "")
# print binascii.a2b_hex(b)
print binascii.a2b_hex(b).decode("gb2312")


print "url decode_______________________________"
print binascii.b2a_hex(urllib.unquote(a))   # byte stream to asii_hex

print urllib.unquote(a).decode("gb2312", "unicode-escape")


print"-------------------------------"
test = "e4bda0e5a5bde5958a"

print binascii.a2b_hex("e4bda0e5a5bde5958a")

test2 = "你好啊"
print test2.encode('hex')

# print bytes().fromhex('010210')
print bytes(map(ord, '\x01\x02\x31\x32'))
print bytes([0x01,0x02,0x31,0x32])
print str(bytes(b'\x01\x0212'))[2:-1]

print "11111111111111111111111"
aa = "example"
print type(aa)
print bytes(aa)
print type(aa)

bb = b"example_b"
print type(bb)
print bb
print str(bb)
print type(bb)
