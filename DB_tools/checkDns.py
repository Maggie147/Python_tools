#! /usr/bin/python
# -*- coding: UTF-8 -*-

import os, sys, re, types
import time, random
import pickle
import shutil
import socket, struct
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Process
sys.path.append('/home/APT/pylib/checkDns')
import logging
import testdata_get
import testdata_feat_extractor
from sklearn.datasets import load_svmlight_file
import pdb

S_DATA_DIR = r'/home/APT/tmp/DNS_tmp'

#获取SVM分类模型
model_data = pickle.load(open('/home/APT/pylib/checkDns/pki/svmmodelnew.pki','rb'))
clf = model_data['svmmodel']

class DnsBlackWhiteCheck(object):
	def __init__(self):
		white_dns_file = r'/home/APT/pylib/checkDns/conf/TWhite_Dns.txt'
		black_dns_file = r'/home/APT/pylib/checkDns/conf/TBlack_Dns.txt'
		black_ip_dir = r'/home/share/ip_conf'
		sys_black_dns_dir = r'/home/share/dns_conf'
		self.black_dns = {}
		self.white_dns = {}
		self.sys_black_dns = {}
		self.black_dnsIP = []
		self._read_black_IP(black_ip_dir)
		self._read_black_dns(black_dns_file)
		self._read_white_dns(white_dns_file)
		self._read_sys_black_dns(sys_black_dns_dir)

	def is_black_dnsIP(self, i_dnsIP, datalist):
		low = 0
		high = len(self.black_dnsIP) - 1
		if i_dnsIP == None or i_dnsIP == 0:
			return False
		while low < high:
			mid = (high + low) / 2
			if self.black_dnsIP[mid][0] < int(i_dnsIP):
				low = mid + 1
			elif self.black_dnsIP[mid][0] > int(i_dnsIP):
				high = mid - 1
			else:
				datalist.append(self.black_dnsIP[mid][1])
				datalist.append(self.black_dnsIP[mid][2])
				datalist.append(self.black_dnsIP[mid][3])
				return True
		return False

	def is_sys_black_dns(self, i_dns, datalist):
		data = i_dns
		if data[len(data) - 1] == '.':
			data = data[0:len(data) - 1]
		if data[0] == '.':
			data = data[1:]
		if self._is_type(data, self.sys_black_dns, datalist) is True:
			return True
		else:
			return False

	def is_black_dns(self, i_dns, datalist):
		data = i_dns
		if data[len(data) - 1] == '.':
			data = data[0:len(data) - 1]
		if data[0] == '.':
			data = data[1:]
		if self._is_type(data, self.black_dns, datalist) is True:
			return True
		else:
			return False

	def is_white_dns(self, i_dns, datalist):
		data = i_dns
		if data[len(data) - 1] == '.':
			data = data[0:len(data) - 1]
		if data[0] == '.':
			data = data[1:]
		if self._is_type(data, self.white_dns, datalist) is True:
			return True
		else:
			return False

	def _is_type(self, dns, dnslist, datalist):
		index = dns.rfind('.')
		if index == -1:
			key = dns
			if not dnslist.has_key(key):
				return False
			if not dnslist[key].has_key('null'):
				return False
			if type(dnslist[key]['null']) is types.ListType:
				length = len(dnslist[key]['null'])
				i = 0
				while i < length:
					try:
						datalist.append(dnslist[key]['null'][i])
					except Exception, e:
						print e
					i += 1
			return True
		else:
			n_dns = dns[0:index]
			key = dns[index+1:]
			if not dnslist.has_key(key):
				return False
			if dnslist[key].has_key('null'):
				if type(dnslist[key]['null']) is types.ListType:
					length = len(dnslist[key]['null'])
					i = 0
					while i < length:
						try:
							datalist.append(dnslist[key]['null'][i])
						except Exception, e:
							print e
						i += 1
				return True
			if not self._is_type(n_dns, dnslist[key], datalist):
				return False
			return True

	def _read_black_IP(self, filedir):
		if not os.path.exists(filedir):
			print "Error: no dir for " + filename
			sys.exit(1)

		decode_filename = os.path.join(filedir, 'TeaDecode')
		old_filename = os.path.join(filedir, 'Teablackip.conf')
		filename = os.path.join(filedir, 'blackIP.tmp.aaa')
		command = '%s %s %s' %(decode_filename, old_filename, filename)
		res = os.system(command)
		if res != 0:
			print "Error: Decryption failure for Teablackip.conf"
			return
		self._read_file_black_ip(filename)

		old_filename = os.path.join(filedir, 'Teablackuserip.conf')
		filename = os.path.join(filedir, 'blackIP.tmp.bbb')
		command = '%s %s %s' %(decode_filename, old_filename, filename)
		res = os.system(command)
		if res != 0:
			print "Error: Decryption failure for Teablackuserip.conf"
			return
		self._read_file_black_ip(filename)

		self.black_dnsIP = sorted(self.black_dnsIP, key=lambda x:x[0])

	def _read_file_black_ip(self, filename):
		for line in open(filename):
			try:
				if line[len(line) - 1] == '\n':
					line = line[0:len(line)-1]
			except Exception, e:
				continue

			datas = line.split('|')
			try:
				datas[0] = socket.ntohl(struct.unpack("I", socket.inet_aton(str(datas[0])))[0])
			except Exception, e:
				print e
				continue

			self.black_dnsIP.append(datas)
		os.remove(filename)

	def _read_black_dns(self, filename):
		if not os.path.exists(filename):
			print "Error: no file for " + filename
			sys.exit(1)
		for line in open(filename):
			try:
				if line[len(line) - 1] == '\n':
					line = line[0:len(line)-1]
			except Exception, e:
				continue

			datas = line.split('|')
			try:
				dns = datas[0]
				dns_data = []
				dns_data.append(datas[1])
				dns_data.append(datas[2])
				dns_data.append(datas[3])
			except Exception, e:
				print e
				continue

			dns_len = len(dns)
			if dns_len < 3:
				continue

			if dns[dns_len - 1] == '.':
				dns = dns[0:dns_len-1]
			if dns[0] == '.':
				dns = dns[1:]
			self._write_data_list(dns, self.black_dns, dns_data)

	def _read_sys_black_dns(self, filedir):
		if not os.path.exists(filedir):
			print "Error: no dir for " + filedir
			sys.exit(1)
		old_filename = os.path.join(filedir, 'dns.txt')
		decode_filename = os.path.join(filedir, 'TeaDecode')
		filename = os.path.join(filedir, 'systemBlackDns.txt')
		command = '%s %s %s' %(decode_filename, old_filename, filename)
		res = os.system(command)
		if res != 0:
			print "Error: Decryption failure for dns.txt"
			return
		for line in open(filename):
			try:
				if line[len(line) - 1] == '\n':
					line = line[0:len(line)-1]
			except Exception, e:
				continue

			datas = line.split('|')
			try:
				dns = datas[0]
				dns_data = []
				dns_data.append(datas[1])
				dns_data.append(datas[2])
				dns_data.append(datas[3])
			except Exception, e:
				print e
				continue

			dns_len = len(dns)
			if dns_len < 3:
				continue

			if dns[dns_len - 1] == '.':
				dns = dns[0:dns_len-1]
			if dns[0] == '.':
				dns = dns[1:]
			self._write_data_list(dns, self.sys_black_dns, dns_data)

		os.remove(filename)

	def _read_white_dns(self, filename):
		if not os.path.exists(filename):
			print "Error: no file for " + filename
			sys.exit(1)
		for line in open(filename):
			data_len = len(line) - 1
			if data_len < 3:
				continue
			data = line[0:data_len]
			if data[data_len - 1] == '.':
				data = data[0:data_len-1]
			if data[0] == '.':
				data = data[1:]
			self._write_data_list(data, self.white_dns, None)

	def _write_data_list(self, dns, dnslist, datas):
		index = dns.rfind('.')
		if index == -1:
			key = dns
			if not dnslist.has_key(key):
				dnslist[key] = {}
			dnslist[key]['null'] = datas
		else:
			n_dns = dns[0:index]
			key = dns[index+1:]
			if not dnslist.has_key(key):
				dnslist[key] = {}
			self._write_data_list(n_dns, dnslist[key], datas)


class DealWithFile(object):
	def __init__(self):
		self.base_dir = r'/home/APT/data_dump/DNS'
		self.base_data = {}
		self.base_data['count'] = 0
		self.base_data['ioutime'] = 0
		self.base_data['data'] = ''
		self.black_data = {}
		self.black_data['count'] = 0
		self.black_data['ioutime'] = 0
		self.black_data['data'] = ''
		self.random_data = {}
		self.random_data['count'] = 0
		self.random_data['ioutime'] = 0
		self.random_data['data'] = ''
		self.long_dns_data = {}
		self.long_dns_data['count'] = 0
		self.long_dns_data['ioutime'] = 0
		self.long_dns_data['data'] = ''
		self.single_dns_data = {}
		self.single_dns_data['count'] = 0
		self.single_dns_data['ioutime'] = 0
		self.single_dns_data['data'] = ''

	def read_file_data(self, fileDir, mydata):
		if not os.path.exists(fileDir):
			print 'Error: no dir for ' + fileDir
			return -1
		files = os.listdir(fileDir)
		if not files:
			self._write_file()
		time.sleep(2)
		for file in files:
			filename = os.path.join(fileDir, file)
			if not os.path.exists(filename):
				continue
			try:
				self._deal_file_data(filename, mydata)
				self._write_file()
			except Exception, e:
				print e
			os.remove(filename)

	def _write_one_data(self, datalist, max_num, max_time, file):
		if datalist['count'] > max_num or (datalist['count'] > 0 and int(time.time()) - datalist['ioutime'] > max_time):
			times = int(time.time())
			filename = self.base_dir + '/' + file + '-' + str(times) + '.dump'
			if os.path.exists(filename):
				filename = self.base_dir + '/' + file + '-' + str(times + random.randint(100,999)) + '.dump'
			try:
				fp = open(filename, "ab")
				fp.write(datalist['data'])
				fp.close()
				datalist['data'] = ''
				datalist['count'] = 0
				datalist['ioutime'] = 0
			except Exception, e:
				print e

	def _write_file(self):
		if not os.path.exists(self.base_dir):
			print 'Error: no dir for ' + self.base_dir
			print 'begin to create dir...'
			os.mkdir(self.base_dir)

		#self._write_one_data(self.base_data, 100, 18, 'TDnsResult')
		#self._write_one_data(self.black_data, 10, 10, 'TDnsBlack')
		#self._write_one_data(self.random_data, 50, 10, 'TDnsRandom')
		#self._write_one_data(self.long_dns_data, 50, 10, 'TDnsLong')
		#self._write_one_data(self.single_dns_data, 50, 10, 'TDnsSignel')

		self._write_one_data(self.base_data, 1000000, 1800, 'TDnsResult')
		self._write_one_data(self.black_data, 100000, 300, 'TDnsBlack')
		self._write_one_data(self.random_data, 500000, 1800, 'TDnsRandom')
		self._write_one_data(self.long_dns_data, 50000, 1800, 'TDnsLong')
		self._write_one_data(self.single_dns_data, 500000, 1800, 'TDnsSignel')

	def _deal_file_data(self, filename, mydata):
		random_dns = list()
		random_raws = list()
		try:
			fp = open(filename)
			lines = fp.read().split('\n')
		except Exception, e:
			print e
			return
		for line in lines:
			if len(line) < 3:
				continue
			raws = line.split('\t')
			if len(raws) != 12:
				continue
			i = 0
			data_list = []
			print raws[0]
			if self._is_valid_hostname(raws[0]) is False:
				i = '3'
				self._is_write_raws_base(i, raws, self.base_data)
			elif mydata.is_sys_black_dns(raws[0], data_list) is True:
				i = '2'
				try:
					times = str(data_list[0])
					srcID = str(data_list[1])
					typeID = str(data_list[2])
					timeArray = time.strptime(times, "%Y%m%d")
					times = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
				except Exception, e:
					print e
					continue
				self._is_write_raws_sys_black(i, raws, self.base_data, times, srcID, typeID)
				self._is_write_raws_black_random(i, raws, self.black_data)
				self._is_single_long(raws, i)
			elif mydata.is_black_dns(raws[0], data_list) is True:
				i = '2'
				try:
					times = str(data_list[0])
					srcID = str(data_list[1])
					typeID = str(data_list[2])
					timeArray = time.strptime(times, "%Y%m%d")
					times = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
				except Exception, e:
					print e
					continue
				self._is_write_raws_sys_black(i, raws, self.base_data, times, srcID, typeID)
				self._is_write_raws_black_random(i, raws, self.black_data)
				self._is_single_long(raws, i)
			elif mydata.is_black_dnsIP(raws[6], data_list) is True:
				i = '2'
				try:
					times = str(data_list[0])
					srcID = str(data_list[1])
					typeID = str(data_list[2])
					timeArray = time.strptime(times, "%Y%m%d")
					times = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
				except Exception, e:
					print e
					continue
				self._is_write_raws_sys_black(i, raws, self.base_data, times, srcID, typeID)
				self._is_write_raws_black_random(i, raws, self.black_data)
				self._is_single_long(raws, i)
			elif mydata.is_white_dns(raws[0], data_list) is True:
				i = 0
				continue
			else:
				random_dns.append(raws[0])
				random_raws.append(raws)
		if len(random_dns) > 0:
			count = len(random_dns)
			try:
				file = testdata_feat_extractor.feat_extract(random_dns)
				file = testdata_get.getTestData(file, count)
				X_test, y_test = load_svmlight_file(file)
				result = clf.predict(X_test)
			except Exception, e:
				print e

		num = 0
		for raws in random_raws:
			try:
				i = int(result[num])
			except Exception, e:
				i = 0
			i = str(i)
			self._is_write_raws_base(i, raws, self.base_data)
			self._is_single_long(raws, i)

			if i == '1':
				self._is_write_raws_black_random(i, raws, self.random_data)

			num += 1

	def _is_single_long(self, raws, iflag):
		if raws[6] == '0':
			if self.single_dns_data['count'] == 0:
				self.single_dns_data['ioutime'] = int(time.time())
			self.single_dns_data['count'] += 1
			self.single_dns_data['data'] += raws[0] + "\t" + raws[1] + "\t" + raws[2] + "\t" + raws[3] + "\t" + raws[4] + "\t" + raws[5] + "\t" + raws[6] + "\t" + raws[7] + "\t" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(raws[8]))) + "\t" + raws[9] + "\t"  + iflag + "\t" + raws[10] + "\t" + raws[11] + "\n"
		if len(raws[0]) > 80:
			if self.long_dns_data['count'] == 0:
				self.long_dns_data['ioutime'] = int(time.time())
			self.long_dns_data['count'] += 1
			self.long_dns_data['data'] += raws[0] + "\t" + raws[1] + "\t" + raws[2] + "\t" + raws[3] + "\t" + raws[4] + "\t" + raws[5] + "\t" + raws[6] + "\t" + raws[7] + "\t" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(raws[8]))) + "\t" + raws[9] + "\t"  + iflag + "\t" + raws[10] + "\t" + raws[11] + "\n"

	def _is_write_raws_black_random(self, i, raws, datalist):
		self._is_init_ioutime0(datalist)
		datalist['data'] += raws[0] + "\t" + raws[1] + "\t" + raws[2] + "\t" + raws[3] + "\t" + raws[4] + "\t" + raws[5] + "\t" + raws[6] + "\t" + raws[7] + "\t" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(raws[8]))) + "\t" + raws[9] + "\t" + raws[10] + "\t" + raws[11] + "\n"
		datalist['count'] += 1

	def _is_write_raws_sys_black(self, i, raws, datalist, times, srcID, typeID):
		self._is_init_ioutime0(datalist)
		datalist['data'] += raws[0] + "\t" + raws[1] + "\t" + raws[2] + "\t" + raws[3] + "\t" + raws[4] + "\t" + raws[5] + "\t" + raws[6] + "\t" + raws[7] + "\t" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(raws[8]))) + "\t" + raws[9] + "\t"  + i + "\t" + raws[10] + "\t" + raws[11] + "\t" + times + "\t" + srcID + "\t" + typeID + "\n"
		datalist['count'] += 1

	def _is_write_raws_base(self, i, raws, datalist):
		self._is_init_ioutime0(datalist)
		datalist['data'] += raws[0] + "\t" + raws[1] + "\t" + raws[2] + "\t" + raws[3] + "\t" + raws[4] + "\t" + raws[5] + "\t" + raws[6] + "\t" + raws[7] + "\t" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(raws[8]))) + "\t" + raws[9] + "\t"  + i + "\t" + raws[10] + "\t" + raws[11] + "\n"
		datalist['count'] += 1

	def _is_init_ioutime0(self, datalist):
		if datalist['count'] == 0:
			datalist['ioutime'] = int(time.time())

	def _is_valid_hostname(self, hostname):
		if len(hostname) > 255:
			return False
		hostname = hostname.strip('.')
		allowed = re.compile(r'(?!-)[A-Z|0-9|\-|\/]{1,63}(?<!-)$', re.IGNORECASE)
		try:
			if all(allowed.match(x) for x in hostname.split('.')):
				return True
			else:
				return False
		except Exception, e:
			return False

if __name__ == '__main__':
	if not os.path.exists(S_DATA_DIR):
		print 'No the dir of %s' %(S_DATA_DIR)
		print "sleep 10's"
		time.sleep(10)

	#pdb.set_trace()
	mydns = DnsBlackWhiteCheck()
	myData = DealWithFile()

	while True:
		myData.read_file_data(S_DATA_DIR, mydns)
		time.sleep(60)
