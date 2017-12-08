#!/usr/bin/python
#-*-coding:utf-8-*- 
"""
__code__ = 'python_2.7'
__title__ = 'hex_gbk to string'
__author__ = 'tx'
__mtime__ = '2017-09-13' 
"""

import codecs
import binascii
import sys


def usage():
    print """This program Change gbk_Hex To string. 
    like: "d5c5c8fd" =======> "张三"
    cmd: python gbkHex_2String.py d5c5c8fd
    Options include: 
    Uage: -version, Prints the version number 
    Uage: -help, Display this help """


def gbkHex_2String(gbk8Hex):
    """
    chang gbk hex (like: 'd5c5c8fd') to string (like: '张三')
    """
    if gbk8Hex:
        deString = binascii.a2b_hex(gbk8Hex).decode('gbk').encode('utf-8')
        return deString
    else:
        return None


def dealwith_input(string):
    if string:
        new_string = string.replace('22', '')
        return new_string
    else:
        return None


def get_sysArgv():
    inputSting = None
    if len(sys.argv) == 1:
        usage()
        sys.exit()
    else:
        if sys.argv[1].startswith('-'):
            option = sys.argv[1][1:]
        # if sys.argv[1].startswith('--'):
        #     option = sys.argv[1][2:]
            if option.lower() == 'version':       #lower(); upper()
                print "Version 1.0"
            elif option.lower()  == 'help':
                usage()
            else:
                print "Unknown option."
            sys.exit()
        else:
            inputSting = sys.argv[1]
    return inputSting


def main():
    getIn = get_sysArgv()
    newstring = dealwith_input(getIn)
    # print utf8Hex_2String.__doc__
    out = gbkHex_2String(newstring)
    print out


if __name__ == '__main__':
    main()
