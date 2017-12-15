#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import os, sys, re
import time
import pickle
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Process
sys.path.append('.')
import logging
import MySQLdb
import testdata_get
import testdata_feat_extractor
from sklearn.datasets import load_svmlight_file

class IsBlackWhite(object):
	def __init__(self):
		self.black_dns = {}
		self.white_dns = {}
		self.black_dnsIP = []
		#self._read_black_dns(mydb)
		self._read_white_dns()
		#self._read_black_IP(mydb)
	
	def _read_black_IP(self, mydb):
		i_id = -1
		s_num = 3000
		while True:
			sql = 'select Id, IPaddress from Blacklist_IP where Id > %s order by Id asc limit %s'
			params = (i_id, s_num, )

			raws = mydb.searchSql(sql, params)

			for raw in raws:
				i_id = int(raw[0])
				self.black_dnsIP.append(int(raw[1]))
			time.sleep(0.1)

			if len(raws) < s_num:
				break
		self.black_dnsIP.sort()

	def _read_black_dns(self, mydb):
		i_id = -1
		s_num = 3000
		while True:
			sql = 'select Id, Dns from TBlack_Dns where Id > %s order by Id asc limit %s'
			params = (i_id, s_num, )

			raws = mydb.searchSql(sql, params)

			for raw in raws:
				i_id = int(raw[0])
				self._write_one_black_dns(raw[1])
			time.sleep(0.1)

			if len(raws) < s_num:
				break

	def _read_white_dns(self, ):



		i_id = -1
		s_num = 1000
		while True:
			sql = 'select Id, Dns from TWhite_Dns where Id > %s order by Id asc limit %s'
			params = (i_id, s_num, )

			raws = mydb.searchSql(sql, params)

			for raw in raws:
				i_id = int(raw[0])
				self._write_one_white_dns(raw[1])
			time.sleep(0.1)

			if len(raws) < s_num:
				break

	def is_black_dnsIP(self, i_dnsIP):
		low = 0
		height = len(self.black_dnsIP) - 1

		if i_dnsIP == None:
			return False
		while low < height:
			mid = (height + low)/2
			if self.black_dnsIP[mid] < int(i_dnsIP):
				low = mid + 1
			elif self.black_dnsIP[mid] > int(i_dnsIP):
				height = mid - 1
			else:
				return True
		return False

	def is_black_dns(self, i_dns):
		self._split_dns(i_dns)
		if self.black_dns.has_key(self.dns_level_1) == False:
			return False

		if self.dns_level_num >= 1:
			if self.black_dns[self.dns_level_1].has_key('null') == True:
				return True

		if self.dns_level_num >= 2:
			if self.black_dns[self.dns_level_1].has_key(self.dns_level_2) == False:
				return False
			if self.black_dns[self.dns_level_1][self.dns_level_2].has_key('null') == True:
				return True

		if self.dns_level_num >= 3:
			if self.black_dns[self.dns_level_1][self.dns_level_2].has_key(self.dns_level_3) == False:
				return False
			if self.black_dns[self.dns_level_1][self.dns_level_2][self.dns_level_3].has_key('null') == True:
				return True

		if self.dns_level_num >= 4:
			if self.black_dns[self.dns_level_1][self.dns_level_2][self.dns_level_3].has_key(self.dns_level_4) == False:
				return False
			if self.black_dns[self.dns_level_1][self.dns_level_2][self.dns_level_3][self.dns_level_4].has_key('null') == True:
				return True

		if self.dns_level_num >= 5:
			if self.black_dns[self.dns_level_1][self.dns_level_2][self.dns_level_3][self.dns_level_4].has_key(self.dns_level_5) == False:
				return False
			if self.black_dns[self.dns_level_1][self.dns_level_2][self.dns_level_3][self.dns_level_4][self.dns_level_5].has_key('null') == True:
				return True

		return False

	def is_white_dns(self,i_dns):
		self._split_dns(i_dns)
		if self.white_dns.has_key(self.dns_level_1) == False:
			return False

		if self.dns_level_num >= 1:
			if self.white_dns[self.dns_level_1].has_key('null') == True:
				return True

		if self.dns_level_num >= 2:
			if self.white_dns[self.dns_level_1].has_key(self.dns_level_2) == False:
				return False
			if self.white_dns[self.dns_level_1][self.dns_level_2].has_key('null') == True:
				return True

		if self.dns_level_num >= 3:
			if self.white_dns[self.dns_level_1][self.dns_level_2].has_key(self.dns_level_3) == False:
				return False
			if self.white_dns[self.dns_level_1][self.dns_level_2][self.dns_level_3].has_key('null') == True:
				return True

		if self.dns_level_num >= 4:
			if self.white_dns[self.dns_level_1][self.dns_level_2][self.dns_level_3].has_key(self.dns_level_4) == False:
				return False
			if self.white_dns[self.dns_level_1][self.dns_level_2][self.dns_level_3][self.dns_level_4].has_key('null') == True:
				return True
				
		if self.dns_level_num >= 5:
			if self.white_dns[self.dns_level_1][self.dns_level_2][self.dns_level_3][self.dns_level_4].has_key(self.dns_level_5) == False:
				return False
			if self.white_dns[self.dns_level_1][self.dns_level_2][self.dns_level_3][self.dns_level_4][self.dns_level_5].has_key('null') == True:
				return True

		return False

	def _write_one_black_dns(self, i_dns):
		self._split_dns(i_dns)
		if self.black_dns.has_key(self.dns_level_1) == False:
			self.black_dns[self.dns_level_1] = {}

		if self.dns_level_num == 1:
			self.black_dns[self.dns_level_1]['null'] = None
			return

		if self.black_dns[self.dns_level_1].has_key(self.dns_level_2) == False:
			self.black_dns[self.dns_level_1][self.dns_level_2] = {}

		if self.dns_level_num == 2:
			self.black_dns[self.dns_level_1][self.dns_level_2]['null'] = None
			return

		if self.black_dns[self.dns_level_1][self.dns_level_2].has_key(self.dns_level_3) == False:
			self.black_dns[self.dns_level_1][self.dns_level_2][self.dns_level_3] = {}

		if self.dns_level_num == 3:
			self.black_dns[self.dns_level_1][self.dns_level_2][self.dns_level_3]['null'] = None
			return    

		if self.black_dns[self.dns_level_1][self.dns_level_2][self.dns_level_3].has_key(self.dns_level_4) == False:
			self.black_dns[self.dns_level_1][self.dns_level_2][self.dns_level_3][self.dns_level_4] = {}

		self.black_dns[self.dns_level_1][self.dns_level_2][self.dns_level_3][self.dns_level_4]['null'] = None
		
	def _write_one_white_dns(self, i_dns):
		self._split_dns(i_dns)
		if self.white_dns.has_key(self.dns_level_1) == False:
			self.white_dns[self.dns_level_1] = {}

		if self.dns_level_num == 1:
			self.white_dns[self.dns_level_1]['null'] = None
			return

		if self.white_dns[self.dns_level_1].has_key(self.dns_level_2) == False:
			self.white_dns[self.dns_level_1][self.dns_level_2] = {}

		if self.dns_level_num == 2:
			self.white_dns[self.dns_level_1][self.dns_level_2]['null'] = None
			return

		if self.white_dns[self.dns_level_1][self.dns_level_2].has_key(self.dns_level_3) == False:
			self.white_dns[self.dns_level_1][self.dns_level_2][self.dns_level_3] = {}

		if self.dns_level_num == 3:
			self.white_dns[self.dns_level_1][self.dns_level_2][self.dns_level_3]['null'] = None
			return    

		if self.white_dns[self.dns_level_1][self.dns_level_2][self.dns_level_3].has_key(self.dns_level_4) == False:
			self.white_dns[self.dns_level_1][self.dns_level_2][self.dns_level_3][self.dns_level_4] = {}

		if self.dns_level_num == 4:
			self.white_dns[self.dns_level_1][self.dns_level_2][self.dns_level_3][self.dns_level_4]['null'] = None
			return

		if self.white_dns[self.dns_level_1][self.dns_level_2][self.dns_level_3][self.dns_level_4].has_key(self.dns_level_5) == False:
			self.white_dns[self.dns_level_1][self.dns_level_2][self.dns_level_3][self.dns_level_4][self.dns_level_5] = {}

		self.white_dns[self.dns_level_1][self.dns_level_2][self.dns_level_3][self.dns_level_4][self.dns_level_5]['null'] = None
		

	def _split_dns(self, i_dns):
		self.dns_level_num = 0
		self.dns_level_1 = None
		self.dns_level_2 = None
		self.dns_level_3 = None
		self.dns_level_4 = None
		self.dns_level_5 = None
		datas = i_dns.split('.')
		lenth = len(datas)

		i = 1
		while True:
			data = str(datas[lenth-i])
			if i == 1:
				self.dns_level_1 = data
			if i == 2:
				self.dns_level_2 = data
			if i == 3:
				self.dns_level_3 = data
			if i == 4:
				self.dns_level_4 = data
			if i == 5:
				self.dns_level_5 = data

			self.dns_level_num = self.dns_level_num + 1

			if lenth - i == 0:
				if self.dns_level_num > 5:
					self.dns_level_num = 5
				break
			i = i + 1


if __name__ == '__main__':
	all_txt = open('TDnsIpAction-1501320493.tmp').read( )
	
	str_1 = ''
	j = 0
	for b in all_txt.split('\n'):
		
		i = b.split('\t')
		if len(i) != 12:
			continue
		#print len(i)
		#print i
		j += 1
		#print '-----------:' + str(j)
		#print i[8]
		str_1 = str_1 + i[0] + "\t" + i[1] + "\t" + i[2] + "\t" + i[3] + "\t" + i[4] + "\t" + i[5] + "\t" + i[6] + "\t" + i[7] + "\t" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(i[8]))) + "\t" + i[9] + "\t"  + "0" + "\t" + i[10] + "\t" + i[11] + "\n"
	

	f = open('TDnsIpResult-2343546712.dump', "w+")
	f.write(str_1)