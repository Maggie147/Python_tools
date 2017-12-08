#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, getopt
import os

def print_argvs():
    argv_len = len(sys.argv)
    for i in range(argv_len):
        print("sys.argv[%d]: " % i, sys.argv[i])

def usage():
    print("""
        Uage: -g ,Chinese 2 gbk
        Uage: -u ,Chinese 2 utf-8
        Uage: -a ,Chinese 2 utf-8(Hex) and gbk(Hex)
        """)


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

def Chinese2utf8_hex():
    print("_"*60)
    input_Chinese = [u"加速精灵", u"安云", u"飞鱼链加速器", u"超速加速器", u"极速安全加速器", u"熊猫加速器", 
    u"二师兄", u"天行加速器", u"赤兔加速器", u"飞龙", u"加速器", u"旗舰", u"花猫加速器",
    u"非凡加速器", u"轻舟校园网代理加速器", u"百态加速器", u"风驰加速器" , u"天眼通加速器",
    u"速飞加速器", u"豆荚加速器", u"泰坦加速器", u"浪迹加速器", u"灰熊加速器", u"飞秒网游加速器",
    u"海豚加速器", u"傲盾网络加速器", u"代理网游加速器", u"流星加速器", u"代理", u"远程桌面"]
    for i in input_Chinese:
        output_utf8 = bytes(i, "utf8")
        output_gbk = bytes(i, "gbk")
        print (i)
        print ("utf-8: ", output_utf8)
        print ("gbk  : ", output_gbk)
        print ("*"*40)

def C2U_hex(input_string):
    output_string = bytes(input_string, 'utf-8')
    # print(output_string)
    return output_string

def C2GBK_hex(input_string):
    output_string = bytes(input_string, 'gbk')
    # print(output_string)
    return output_string


def main():
    if len(sys.argv) == 1:
        Chinese2utf8_hex()
    else:
        # print_argvs()
        input_string = sys.argv[2]
        output_string = ''
        output_string2 = ''
        print("input_string: ", input_string)

        if sys.argv[1] == '-u' or sys.argv[1] == '-U':
            output_string = C2U_hex(input_string)
        elif sys.argv[1] == '-g' or sys.argv[1] == '-G':
            output_string = C2GBK_hex(input_string)
        elif sys.argv[1] == '-a' or sys.argv[1] == '-A':
            output_string = C2U_hex(input_string)
            output_string2 = C2GBK_hex(input_string)
        else:
            usage()
            sys.exit()

        print("output_String: ", output_string)
        if output_string2:
            print("output_String: ", output_string2)

if __name__ == '__main__':
    main()