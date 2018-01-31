#!/usr/bin/python
#-*-coding:utf-8-*-
"""
__code__ = 'python_2.7'
__title__ = 'hex To bytes(nice string)'
__mtime__ = '2018-01-31'
"""
import codecs
import binascii
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def usage():
    print """This program Change Hex To string.
    like: "e69bb4e696b0e68890e58a9f" =======> "更新成功"
    cmd: python test.py -u e69bb4e696b0e68890e58a9f
    cmd: python test.py -p d5c5c8fd

    Options include:
    Uage: -version, Prints the version number
    Uage: -help, Display this help
    Uage: -u, utf8 To Chinese
    Uage: -g, gbk To Chinese """
    sys.exit()


def get_sysArgv():
    try:
        inStr = None
        codeType = None
        if len(sys.argv) != 3:
            usage()

        if sys.argv[1].startswith('-'):
            option = sys.argv[1][1:]
        elif sys.argv[1].startswith('--'):
            option = sys.argv[1][2:]
        else:
            usage()

        if option.lower() == 'version':       #lower(); upper()
            print "Version 1.0"
        elif option.lower()  == 'help':
            usage()
        elif option.lower()  == 'u':
            codeType = 'utf8'
        elif option.lower()  == 'g':
            codeType = 'gbk'
        else:
            print "Unknown Option!!!."
            usage()

        inStr = sys.argv[2]

        return (inStr, codeType)
    except Exception as e:
        print e
        sys.exit()


def dealwith_input(string):
    if string:
        # new_string = string.replace('\\x', '')
        new_string = string.replace('22', '')
        new_string = new_string.replace('=', '')
        new_string = new_string.replace('%', '')
        return new_string
    else:
        return None


def utf8Hex_2String(utf8Hex):
    """
    chang utf8 hex (like: 'e69bb4e696b0e68890e58a9f') to string (like: '更新成功')
    """
    if utf8Hex:
        deString = binascii.a2b_hex(utf8Hex)

        # print "!!!!:", codecs.encode(deString, 'raw_unicode_escape').decode('utf-8')   codecs
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



def main():
    (getIn, codeTag) = get_sysArgv()

    hexstring = dealwith_input(getIn)

    if 'utf8' in codeTag:
        string = utf8Hex_2String(hexstring)
    elif 'gbk' in codeTag:
        string = gbkHex_2String(hexstring)

    print string


if __name__ == '__main__':
    main()