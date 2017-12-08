#!/usr/bin/python
#-*-coding:utf-8-*- 
import codecs
import binascii
import urllib
import sys

def print_argvs():
    argv_len = len(sys.argv)
    for i in range(argv_len):
        print"sys.argv[%d]: " % i, sys.argv[i]

def add_to_hex(input_string):
    if input_string is not None and input_string != ' ':
        out_String = ''
        lenStr = len(input_string)
        for i in range(lenStr//2):
            # print "/x%s" % input_string[2*i : 2*i+2]
            out_String = out_String + '\\x' + input_string[2*i : 2*i+2]
        # print out_String
        return out_String
    else:
        return None

def Chinese_2_hex(input_string, code = 'utf-8'):
    if isinstance(input_string, unicode):
        input_string = input_string.encode('utf-8')
    if code == 'utf-8':
        out = input_string.decode('utf-8').encode('utf-8')
    elif code == 'gbk':
        out = input_string.decode('utf-8').encode('gbk')
    elif code == 'gb2312':
        out = input_string.decode('utf-8').encode('gb2312')
        
    out_String = binascii.b2a_hex(out)
    out_hex = add_to_hex(out_String)
    # print out
    print out_String
    print out_hex  

    return out_hex

def hex_2_string():
    aa = 'e5bca0e4b889'
    bb = "\xe5\xbc\xa0\xe4\xb8\x89"
    cc = '\xd5\xc5\xc8\xfd'
    dd = 'd5c5c8fd'
    # print aa
    # print bb
    # print cc
    # ccc = cc.repalce('\\x', '')
    ccc = cc.replace('\\x', '')
    print ccc
    print dd
    # cccc = binascii.a2b_hex(dd).decode('gbk').encode('utf-8')
    print cc.decode('gbk').encode('utf-8')


    print binascii.a2b_hex(aa)
    if '\\x' in bb:
        print bb
        print "111"
    print len(bb)
    print len(dd)



def test1():
    s = u"张三"
    ss = Chinese_2_hex(s, 'gbk')


def main():
    if len(sys.argv) == 1:
        hex_2_string()
    else:
        pass




if __name__ == '__main__':
    main()