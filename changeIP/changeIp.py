# -*- encoding: utf-8-*-
#================================================
#  __title__ = 'exchange ip'
#  __author__ = 'tx'
#  __mtime__ = '2017-09-05'
#=================================================
#
import io
import sys
import os
import time
import socket
import struct
import ctypes

g_iDEBUG = 1

def DEBUG(*value):
    if g_iDEBUG == 1:
        t = time.strftime("%Y-%m-%d %H:%M:%S")
        filename = sys.argv[0][sys.argv[0].rfind(os.sep)+1:]
        print "[python][%s,%s]:" % (filename, t),
        for i in value:
            print i,
        print ""


def Int2n_EXChange(h_ip):
    if h_ip < 0:
        # h_ip = ctypes.c_int32(int(h_ip)).value
        # print h_ip
        h_ip = struct.unpack("l", struct.pack("i", h_ip))[0]
    # h_ip = ctypes.c_int32(int(h_ip)).value
    n_ip = socket.inet_ntoa(struct.pack("!I", socket.htonl(h_ip)))
    n_ip2 = socket.inet_ntoa(struct.pack("I", socket.htonl(h_ip)))   #ok
    print n_ip
    print n_ip2


def N2int_EXChange(ip_string):
    temp = socket.inet_aton(ip_string)
    print temp
    ip_int = socket.ntohl(struct.unpack("i", socket.inet_aton(ip_string))[0]) 
    # ip_int = struct.unpack("!I", socket.inet_aton(ip_string))[0]
    print ip_int


def test_int2n():
    ip = -1062730065
    # ip = 1077545662
    # ip = 3232237191
    n_ip = Int2n_EXChange(ip)


def test_n2int():
    ip_string = "192.168.6.101"
    ip_int = N2int_EXChange(ip_string)
    # print ip_int


def main():
    # test_int2n()
    test_n2int()

if __name__ == "__main__":
    main()