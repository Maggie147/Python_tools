#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
__code__ = 'python_2.7'
__title__ = 'utf8-2-chinese'
__author__ = 'tx'
__mtime__ = '2017-09-13'

"""
import binascii
import codecs


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
        new_string = string.replace('\\x', '')
        new_string = new_string.replace('22', '')
        return new_string
    else:
        return None


def main():
    # strings = '\xe8\xbe\xbe\xe5\xa4\xa7'

    # print(codecs.encode(strings, 'raw_unicode_escape').decode('utf-8'))

    strings = '=E8=BE=BE=E5=A4=A7'
    strings = strings.replace('=', '\\x')
    print strings

    now_string = dealwith_input(strings)
    out = utf8Hex_2String(now_string)
    print out


if __name__ == "__main__":
    main()