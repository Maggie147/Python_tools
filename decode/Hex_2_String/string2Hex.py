#!/usr/bin/python
#-*-coding:utf-8-*-
"""
__code__ = 'python_2.7'
__title__ = 'bytes(nice string) To hex'
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
    like1: "更新成功" =======> "e69bb4e696b0e68890e58a9f"
    like2: "更新成功" =======> "\xe6\x9b\xb4\xe6\x96\xb0\xe6\x88\x90\xe5\x8a\x9f"
    cmd: python test.py -u 更新成功
    cmd: python test.py -p 更新成功

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


def dealwith_input(srcStr):
    """change input string to utf-8"""
    if srcStr:
        try:
            newStr = srcStr.decode('gbk').encode('utf-8')
        except Exception as e:
            print e
        return newStr
    else:
        return None


def add_hex_head(hexStr):
    if hexStr is not None and hexStr != ' ':
        hexHeadStr = ''
        lenStr = len(hexStr)
        for i in range(lenStr//2):
            # print "/x%s" % hexStr[2*i : 2*i+2]
            hexHeadStr = hexHeadStr + '\\x' + hexStr[2*i : 2*i+2]
        # print hexHeadStr
        return hexHeadStr
    else:
        return None

def Chinese_2_hex(inStr, code='utf-8', headflag=1):
    if isinstance(inStr, unicode):
        # inStr = inStr.encode('utf-8')
        pass
    if code == 'utf8':
        encodeStr = inStr.decode('utf-8').encode('utf-8')

    elif code == 'gbk':
        encodeStr = inStr.decode('utf-8').encode('gbk')

    elif code == 'gb2312':
        encodeStr = inStr.decode('utf-8').encode('gb2312')

    hexStr = binascii.b2a_hex(encodeStr)

    if not headflag:
        return hexStr
    else:
        return add_hex_head(hexStr)


def main():
    (inputStr, codeType) = get_sysArgv()

    utf8String = dealwith_input(inputStr)

    # print isinstance(utf8String, unicode)

    hexString = Chinese_2_hex(utf8String, codeType, 0)

    print hexString



if __name__ == '__main__':
    main()