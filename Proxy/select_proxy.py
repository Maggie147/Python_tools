#!/usr/bin/python
#coding=utf-8
import urllib
import socket

def main():
    socket.setdefaulttimeout(3)
    f = open("./proxy_file/proxy")
    lines = f.readlines()
    proxys = []
    for i in range(0,len(lines)):
        ip = lines[i].strip("\n").split("\t")
        proxy_host = "http://"+ip[0]+":"+ip[1]
        proxy_temp = {"http":proxy_host}
        proxys.append(proxy_temp)
    url = "http://ip.chinaz.com/getip.aspx"

    usefulFile = open("./proxy_file/proxy_useful","w")

    for proxy in proxys:
        try:
            res = urllib.urlopen(url,proxies=proxy).read()
            # print res
            usefulFile.write(res) 
            print proxy
            print res
        except Exception,e:
            # print proxy
            # print e
            continue


if __name__ == '__main__':
    main()