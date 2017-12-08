#!/usr/bin/python
#-*-coding:utf-8-*- 
"""
__code__ = 'python_2.7'
__title__ = 'test'
__author__ = 'tx'
__mtime__ = '2017-09-13' 
"""
import codecs
import binascii
import urllib
import sys

def usage():
    print """This program Change Hex To string.
    like: "e69bb4e696b0e68890e58a9f" =======> "更新成功"
    cmd: python test.py -u e69bb4e696b0e68890e58a9f
    Options include: 
    Uage: -version, Prints the version number 
    Uage: -help, Display this help
    Uage: -u, utf8 To Chinese
    Uage: -g,  gbk To Chinese 2 """


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
        # new_string = string.replace('\\x', '')
        new_string = string.replace('22', '')
        return new_string
    else:
        return None


def get_sysArgv():
    inputSting = None
    decodeTag = None
    if len(sys.argv) == 3: 
        inputSting = sys.argv[2]

        if sys.argv[1].startswith('-'):
            option = sys.argv[1][1:]
        # elif sys.argv[1].startswith('--'):
        #     option = sys.argv[1][2:]
            if option.lower() == 'version':       #lower(); upper()
                print "Version 1.0"
            elif option.lower()  == 'help':
                usage()
            elif option.lower()  == 'u':
                decodeTag = 'utf8'
            elif option.lower()  == 'g':
                decodeTag = 'gbk'
            else:
                print "Unknown Option!!!."
                usage()
                sys.exit()
    else:
        usage()
        sys.exit()
        # inputSting = "e69bb4e696b0e68890e58a9f"
        # decodeTag = 'utf8'        
    return (inputSting, decodeTag)
  

def main():
    (getIn, codeTag) = get_sysArgv()

    hexstring = dealwith_input(getIn)

    string = None

    if 'utf8' in codeTag:
        string = utf8Hex_2String(hexstring)
    elif 'gbk' in codeTag:
        string = gbkHex_2String(hexstring)

    print string



def test():
    f = "张三"
    print binascii.b2a_hex(f.decode('utf-8').encode('gbk'))   # gbk hex  "d5c5c8fd"
    print binascii.a2b_hex("d5c5c8fd")
    print binascii.a2b_hex("d5c5c8fd").decode('gbk')

    e = "1976946719"
    print binascii.b2a_hex(e)
    print bytes(e)
    print hex(int(e))



if __name__ == '__main__':
    test()