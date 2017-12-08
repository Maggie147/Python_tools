#!/sur/bin/python
# -*- coding: utf-8 -*-

import codecs
import sys
import binascii


def main():

    if len(sys.argv) > 1:
        str = sys.argv[1]
        # str = str.decode('utf-8')           # utf8 2 unicode
        # str = str.replace('x', '\x')
    else:
        str = '\xe5\x91\xb5\xe5\x91\xb5\xe5\x93\x92'
 
    print str
    print str.decode('utf-8')


    # strings = '\xe5\x91\xb5\xe5\x91\xb5\xe5\x93\x92'
    # # strings = '\xe4\xb8\xad\xe5\x9b\xbd'
    # # deSting = strings.decode('gbk').encode('utf-8')
    # deSting = strings.decode('utf-8').encode('gbk', 'ignore')
    # print deSting
    # deSting = strings.decode('utf-8')
    # print deSting
    # print "____________"
    teststr = '\x75\xd5\xd0\x1f'
    print teststr

    print "____________"
    teststr2 = '\x33\x35\x34\x30\x37\x33\x31\x34'
    print teststr2

    ssss = '远程桌面'
    aaaaaaaaaaaaa= binascii.b2a_hex(ssss.encode("gbk"))
    print aaaaaaaaaaaaa

if __name__ == "__main__":
    main()
