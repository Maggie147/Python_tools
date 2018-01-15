#! /usr/bin/env python
#coding=utf-8
#================================================
#  __title__ = 'Tmail Black check'
#  __author__ = 'tx'
#  __mtime__ = '2017-12-20'
#=================================================
#
import MySQLdb
import re
import time
import types
import pprint
import socket
import struct
from datetime import datetime
import xml.etree.ElementTree as ET
import sys,time,os
sys.path.append('/home/APT/pylib/')
import storageclient

reload(sys)
sys.setdefaultencoding('utf8')


class MysqlConnect(object):
    def __init__(self, xmlpath):
        self.conffile = xmlpath
        # self.limit_count = 100000
        # self.limit_count = 100
        self.begin_id = 0
        self.total_mail = 0
        self.__readconfig()
        self.__connectmysql()

    def __readconfig(self):
        try:
            print "xmlpath: ", self.conffile
            tree = ET.parse(self.conffile)
            # tree = ET.ElementTree(file = self.conffile)
            root = tree.getroot()
            database = root.find('database')
            if not database:
                print "There is no a node named database in the file: %s"%(xmlpath)
                sys.exit(1)
            self.db_host = database.find('db_address').text
            # self.db_port = database.find('db_port').text
            self.db_name = database.find('db_name').text
            self.db_user = database.find('db_user').text
            self.db_pwd  = database.find('db_pwd').text
            if not self.db_host or not self.db_name or not self.db_user or not self.db_pwd:
                print "db info not get all!!!"
                print "host:%s, name:%s, user:%s, pwd:%s" % (self.db_host, self.db_name, self.db_user, self.db_pwd)
                sys.exit(1)
        except Exception,e:
            print "Readconfig failed error: %s \n" % e
            sys.exit(1)

    def __connectmysql(self):
        try:
            self.conn = MySQLdb.connect(self.db_host, self.db_user, self.db_pwd, self.db_name, charset="utf8")
            self.cursor = self.conn.cursor()
            self.cursor.execute("SET NAMES utf8")
            if not self.conn:
                print "connect mysql failed..."
                # self.is_connected = False
                sys.exit(1)
            # self.is_connected = True
            print "connect mysql succeed..."
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception,e:
            print 'exit error'

    def getStartMail(self, table1='TmailThreats', table2='TMail'):
        threats_sql = "select MailId from %s order by MailId desc limit 1"%table1               # TmailThreats
        mail_sql = "select Id from %s order by Id desc limit 1"%table2                          # Tmail
        try:
            self.cursor.execute(threats_sql)
            result = self.cursor.fetchall()
            if result:
                self.begin_id = result[0][0]
            else:
                print "no data in TmailThreats!!"
                pass

            self.cursor.execute(mail_sql)
            mail_status = self.cursor.fetchall()
            if mail_status:
                self.total_mail = mail_status[0][0]
            else:
                print "no data in Tmail, not get mail_maxid!!!"
                pass
            return True
        except Exception as e:
            print e, "get_startMail error!!!"
            return False

    def getMailInfo(self, start, limit, MailTName='TMail'):
        mailSql = "select Id, INET_NTOA(IPaddress), INET_NTOA(DstIPaddress), Content\
        from %s where Id > %d order by Id limit %d;" % (MailTName, int(start), limit)

        count = self.cursor.execute(mailSql)
        mail_infos = self.cursor.fetchall()
        if not mail_infos:
            print "TMailContent didn't find datas!"
            return
        self.begin_id += count
        for mailInfo in mail_infos:
            yield mailInfo


def get_domain(buf):
    if not buf:
        return None
    try:
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', buf)
    except Exception as e:
        print e, "del html error!!!"
        dd = buf

    try:
        # restr = r"([a-zA-Z0-9][a-zA-Z0-9\-]{0,62}\.[a-zA-Z0-9][a-zA-Z0-9-]{0,62}\.[a-z]{2,6})\.?"
        restr = r'(http|https)://([a-zA-Z0-9][a-zA-Z0-9\-]{0,62}\.[a-zA-Z0-9][a-zA-Z0-9-]{0,62}\.[a-z]{2,6})\.?'

        patter = re.compile(restr, re.VERBOSE | re.IGNORECASE |re.DOTALL)
        vaule = patter.findall(str(dd))
        if not vaule:
            # print "not get domain!!!"
            return None
        return vaule
    except Exception as e:
        print e, "get domain error!!!"
        return None

class BlackInfo(object):
    def __init__(self, ippath, dimainpath):
        self.blackip_path = ippath
        self.bdomain_path = dimainpath
        self.blackip = []
        self.blackdns = {}
        self.__readBlackIp(self.blackip_path)
        self.___readBlackDns(self.bdomain_path)


    def __readBlackIp(self, filedir):
        if not os.path.exists(filedir):
            print "Error: no dir for " + filedir
            sys.exit(1)
        for line in open(filedir):
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
            self.blackip.append(datas)
        self.blackip = sorted(self.blackip, key=lambda x:x[0])


    def ___readBlackDns(self, filename):
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
            self.__write_data_list(dns, self.blackdns, dns_data)
            # print "^^^"*30
            # pprint.pprint(self.blackdns)

    def __write_data_list(self, dns, dnslist, datas):
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
            self.__write_data_list(n_dns, dnslist[key], datas)

    # judge ip
    def binary_search(self, i_IP):
        low = 0
        high = len(self.blackip) - 1
        if i_IP == None or i_IP == 0:
            return False
        while low < high:
            mid = (high + low) // 2
            if self.blackip[mid][0] < int(i_IP):
                low = mid - 1
            elif self.blackip[mid][0] > int(i_IP):
                high = mid + 1
            else:
                return mid
                # return True
        return False

    def is_black_IP(self, ip):
        try:
            ip_tmp = ip
            IP_tmp = socket.ntohl(struct.unpack("I", socket.inet_aton(ip_tmp))[0])
            # print IP_tmp
            ret = None
            ret = self.binary_search(IP_tmp)
            if not ret:
                print "not find"
                return False
            # print self.blackip[ret]
            return ret

            # find_ip = self.blackip[ret][0]
            # find_ip_tmp = socket.inet_ntoa(struct.pack("I", socket.htonl(find_ip)))
            # print find_ip_tmp
        except Exception, e:
            print e
            return False


    def _is_type(self, dns, dnslist):
        index = dns.rfind('.')
        if index == -1:
            key = dns
            if not dnslist.has_key(key):
                print "^^^^"*30, "1"
                return False
            if not dnslist[key].has_key('null'):
                print "^^^^"*30, "2"
                return False
            if type(dnslist[key]['null']) is types.ListType:
                # length = len(dnslist[key]['null'])
                # i = 0
                # while i < length:
                #     try:
                #         # datalist.append(dnslist[key]['null'][i])
                #         print "find it: ", dnslist[key]['null'][i]
                #         # return True
                #     except Exception, e:
                #         print e
                #     i += 1
                print "find it: ", key, dnslist[key]['null'], type(dnslist[key]['null'])
                return dnslist[key]['null']
            print "^^^^"*30, "3"
            return True
        else:
            n_dns = dns[0:index]
            key = dns[index+1:]
            if not dnslist.has_key(key):
                print "^^^^"*30, "4"
                return False
            if dnslist[key].has_key('null'):
                if type(dnslist[key]['null']) is types.ListType:
                    # length = len(dnslist[key]['null'])
                    # i = 0
                    # while i < length:
                    #     try:
                    #         # datalist.append(dnslist[key]['null'][i])
                    #         print "find it: ", dnslist[key]['null'][i]
                    #         # return True
                    #     except Exception, e:
                    #         print e
                    #     i += 1
                    print "find it: ", key, dnslist[key]['null'], type(dnslist[key]['null'])
                    return dnslist[key]['null']
                print "^^^^"*30, "5"
                return True
            if not self._is_type(n_dns, dnslist[key]):
                print "^^^^"*30, "6"
                return False
            print "^^^^"*30, "7"
            return True

    def is_black_dns(self, i_dns, datalist):
        print "check domain"
        data = i_dns
        if data[len(data) - 1] == '.':
            data = data[0:len(data) - 1]
        if data[0] == '.':
            data = data[1:]
        ret = self._is_type(data, self.blackdns)
        print ret
        if ret:
            return True
        else:
            print "not find domain"
            return False


def get_domain(buf):
    if not buf:
        return None
    try:
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', buf)
    except Exception as e:
        print e, "del html error!!!"
        dd = buf

    try:
        # restr = r"([a-zA-Z0-9][a-zA-Z0-9\-]{0,62}\.[a-zA-Z0-9][a-zA-Z0-9-]{0,62}\.[a-z]{2,6})\.?"
        restr = r'(http|https)://([a-zA-Z0-9][a-zA-Z0-9\-]{0,62}\.[a-zA-Z0-9][a-zA-Z0-9-]{0,62}\.[a-z]{2,6})\.?'

        patter = re.compile(restr, re.VERBOSE | re.IGNORECASE |re.DOTALL)
        vaule = patter.findall(str(dd))
        if not vaule:
            # print "not get domain!!!"
            return None
        return vaule
    except Exception as e:
        print e, "get domain error!!!"
        return None

def main():
    blackip_path = "/home/share/ip_conf/blackip.conf"
    bdomain_path = "/home/share/dns_conf/black_domain.conf"
    xmlpath = "/home/APT/conf/SysSet.xml"

    binfo = BlackInfo(blackip_path, bdomain_path)
    ###################################
    domain = "021id.net"
    ret = binfo.is_black_dns(domain, binfo.blackdns)
    ###################################

'''
    mail = MysqlConnect(xmlpath)
    ret  = mail.getStartMail()
    if not ret:
        print "get start Mail failed!!!"
        sys.exit(1)

    print "mail black check start..."
    # print "start_id", mail.begin_id
    # print "total_mail: ", mail.total_mail


    while True:
        if mail.begin_id >= mail.total_mail:
            print "no new mail!!!"
            print "keep alive..."
            time.sleep(60)
            # break

        for mailInfo in mail.getMailInfo(mail.begin_id, limit=100):
            print "Mail_Id:", mailInfo[0]
            print "Src_IP: ", mailInfo[1]
            print "Dst_IP: ", mailInfo[2]

            blackInfo = {'SrcipSrc':None, 'SrcipType':None, 'SrcipTime':None,\
            'DstipSrc':None, 'DstipType':None, 'DstipTime':None, 'ContResult':None}

            # ip = "96.81.131.84"
            # ret = binfo.is_black_IP(ip)
            # # ret = binfo.is_black_IP(mailInfo[1])
            # if ret:
            #     print ret
            #     # print binfo.blackip[ret]
            #     blackInfo['SrcipTime'] = binfo.blackip[ret][1]
            #     blackInfo['SrcipSrc'] = int(binfo.blackip[ret][2])
            #     blackInfo['SrcipType'] = int(binfo.blackip[ret][3])

            # ret = binfo.is_black_IP(mailInfo[2])
            # # ret = binfo.is_black_IP(mailInfo[2])
            # if ret:
            #     print ret
            #     # print binfo.blackip[ret]
            #     blackInfo['DstipTime'] = binfo.blackip[ret][1]
            #     blackInfo['DstipSrc'] = int(binfo.blackip[ret][2])
            #     blackInfo['DstipType'] = int(binfo.blackip[ret][3])


            # domains_tmp = get_domain(mailInfo[3])
            # if domains_tmp:
            #     for domain in domains_tmp:
            #         if "silence.com" in domain[1]:
            #             continue
            #         print "Domian: ", domain[1]
            #         #do something
            #         domain_test = "021id.net"
            #         ret = binfo.is_black_dns(domain_test)
                    ###################################

            # pprint.pprint(blackInfo)
'''


if __name__ == '__main__':
    main()