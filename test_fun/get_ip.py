#!/usr/bin/python
#-*-coding:utf-8-*-

import os
import socket
import fcntl, struct

ip_pre = "248.142"

def getIP(ip_pre, ifname="eth0"):  
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	localIP = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])

	if ip_pre in str(localIP):
		return str(localIP)

def get_ip1():
	out = os.popen("ifconfig | grep 'inet addr:' | grep -v '127.0.0.1' | cut -d: -f2 | awk '{print $1}' | head -1").read()
	return out	

#better
def get_ip2(ifname="eth0"):  
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])

def gethostByname():
	hostName = socket.gethostname()
	localIP = socket.gethostbyname(hostName)
	return localIP

def gethostByname_ex():
	hostName = socket.gethostname()
	ipList = socket.gethostbyname_ex(hostName)
	return ipList


if __name__ == "__main__":
    ip = getIP(ip_pre, "eth0")
	ip = get_ip2("eth0")
	# ip = get_ip2("lo")
	print ip
