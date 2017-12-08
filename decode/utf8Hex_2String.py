#!/usr/bin/python
#-*-coding:utf-8-*- 
"""
__code__ = 'python_2.7'
__title__ = 'hex_utf8 to string'
__author__ = 'tx'
__mtime__ = '2017-09-13' 
"""

import codecs
import binascii
import urllib
import sys

def usage():
    print """This program Change utf8_Hex To string. 
    like: "e69bb4e696b0e68890e58a9f" =======> "更新成功"
    cmd: python utf8Hex_2String.py e69bb4e696b0e68890e58a9f
    Options include: 
    Uage: -version, Prints the version number 
    Uage: -help, Display this help """



def utf8Hex_2String(utf8Hex):
    """
    chang utf8 hex (like: 'e69bb4e696b0e68890e58a9f') to string (like: '更新成功')
    """
    if utf8Hex:
        deString = binascii.a2b_hex(utf8Hex)
        # deString = binascii.a2b_hex(utf8Hex).decode('utf-8')      # bouth ok
        # print deString
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
    out = utf8Hex_2String(newstring)
    print out


if __name__ == '__main__':
    main()
