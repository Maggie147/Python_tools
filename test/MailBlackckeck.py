#! /usr/bin/env python
#coding=utf-8
#================================================
#  __title__ = 'Tmail Black check'
#  __author__ = 'tx'
#  __mtime__ = '2017-12-11'
#=================================================
#
import MySQLdb
import re
import time
from datetime import datetime
import xml.etree.ElementTree as ET
import sys,time,os
sys.path.append('/home/APT/pylib/')
import storageclient

reload(sys)
sys.setdefaultencoding('utf8')

xmlpath = "/home/APT/conf/SysSet.xml"
blackip_path = "/home/share/ip_conf/blackip.conf"
bdomain_path = "/home/share/dns_conf/black_domain.conf"

class MailblackCkeck(object):
    def __init__(self):
        self.limit_count = 100000
        # self.limit_count = 10
        self.begin_id = 0
        self.last_id = 0
        self.readconfig(xmlpath)
        self.connectmysql()
        if not self.blackip_read(blackip_path):
            print "read blackip file failed!!!"
            sys.exit(1)
        # if not self.blackdomain_read(bdomain_path):
        #     print "read black domain file failed!!!"
        #     sys.exit(1)
        self.mailip_check()

    def readconfig(self, xmlpath):
        try:
            print xmlpath
            tree = ET.parse(xmlpath)
            root = tree.getroot()
            database = root.find('database')
            self.db_name = database.find('db_name').text
            self.db_user = database.find('db_user').text
            self.db_pwd  = database.find('db_pwd').text
            self.db_host  = database.find('db_address').text
            print self.db_name,self.db_user,self.db_pwd,self.db_host
        except Exception,e:
            print "Readconfig failed error: %s \n" %e
            sys.exit(1)

    def connectmysql(self):
        try:
            self.conn = MySQLdb.connect(self.db_host, self.db_user, self.db_pwd, self.db_name,charset="utf8")
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

    def blackip_read(self, fpath):
        self.blackip_list=[]
        try:
            file=open(fpath)
            lines=file.readlines()
            for item in lines:
                info  = item.split('|')
                blackinfo = {'IP':None, 'Time':None, 'Src':None, 'Type':None}
                blackinfo['IP'] = info[0].strip()
                blackinfo['Time'] = info[1].strip()
                blackinfo['Src']  = info[2].strip()
                blackinfo['Type'] = info[3].strip()
                self.blackip_list.append(blackinfo)
            print "read file '%s' succeed.." % fpath
            print "Blacklist len:[%d]" % len(self.blackip_list)
            file.close()
            return True
        except Exception,e:
            print " Blacklist_IP read error!: %s" %e
            return False

    def blackdomain_read(self, fpath):
        self.bdomain_list=[]
        try:
            file=open(fpath)
            lines=file.readlines()
            for item in lines:
                blackinfo = {'Domain':None, 'Time':None, 'Src':None, 'Type':None}
                info  = item.split('|')
                blackinfo['Domain'] = info[0].strip()
                blackinfo['Time'] = info[1].strip()
                blackinfo['Src']  = info[2].strip()
                blackinfo['Type'] = info[3].strip()
                self.bdomain_list.append(blackinfo)
            print "read file '%s' succeed.." % fpath
            print "Blacklist len:[%d]" % len(self.bdomain_list)
            file.close()
            return True
        except Exception,e:
            print " Blacklist_domain read error!: %s"%e
            return False

    def mailip_check(self):
        print "mail ip check start..."

        mailcon_sql1 = "select Id, INET_NTOA(IPaddress), INET_NTOA(DstIPaddress), Content\
        from TMail where Id >= %s order by Id limit %d;" % (str(self.begin_id), self.limit_count)
        self.cursor.execute(mailcon_sql1)
        # mailcon_orig = self.cursor.fetchmany()
        mailcon_orig = self.cursor.fetchall()
        # print self.cursor.rowcount
        if not mailcon_orig:
            print "[*] TMailContent didn't find datas!"
            return False
        for mailInfo in mailcon_orig:     # mailInfo[0], mailInfo[1], mailInfo[2] = srcip , dstip, content
            # for black_item in self.blackip_list:
                # if mailInfo[1] in black_item['IP'] or mailInfo[2] in black_item['IP']:
                # # if True:
                #     self.insert(mailInfo[0], black_item)
                #     break
                # else:
                #     continue
            ret = binary_search(self.blackip_list, mailInfo[1])
            if not ret:
                ret = binary_search(self.blackip_list, mailInfo[2])
                if not ret:
                    continue
                else:
                    self.insert(mailInfo[0], black_item)
                    continue
            else:
                self.insert(mailInfo[0], black_item)
                continue

            # for black_item in self.bdomain_list:
            #     # if black_item['Domain'] in content:
            #     if True:
            #         self.insert(mailInfo[0], black_item)
            #         break
            #     else:
            #         continue
            # self.last_id = mailInfo[0]
            continue
        print "mailip check over!!!"

    def mailip_check_test(self):
        mailcon_sql1 = "select Id, INET_NTOA(IPaddress), INET_NTOA(DstIPaddress), Content\
        from TMail where Id >= %s order by Id limit %d;" % (str(self.begin_id), self.limit_count)
        self.cursor.execute(mailcon_sql1)
        mailcon_orig = self.cursor.fetchall()
        # print self.cursor.rowcount
        if not mailcon_orig:
            print "[*] TMailContent didn't find datas!"
            return False
        for mailInfo in mailcon_orig:
            if True:
                self.insert(mailInfo[0])
                break
            else:
                continue

    def insert(self, Id, blackInfo):
        try:
            mail_sql = "select * from TMail where Id = %s;" % Id
            self.cursor.execute(mail_sql)
            mailInfo = self.cursor.fetchone()
        except Exception as e:
            raise e
            return

        NodeValue = {}
        NodeValue['AppName'] = mailInfo[1]
        NodeValue['MailFrom'] = mailInfo[2]
        NodeValue['MailTo'] = mailInfo[3]
        # NodeValue['Subject'] = mailInfo[4]
        # NodeValue['Content'] = mailInfo[5]
        NodeValue['Subject'] = "aa"
        NodeValue['Content'] = "bb"
        NodeValue['AttachFile'] = mailInfo[6]
        NodeValue['AttachPath'] = mailInfo[7]
        NodeValue['Type']= mailInfo[8]
        NodeValue['SendTime'] = time.mktime(time.strptime(str(mailInfo[9]), '%Y-%m-%d %H:%M:%S'))
        NodeValue['IPaddress'] = int(mailInfo[10])
        NodeValue['DstIPaddress'] = int(mailInfo[11])
        NodeValue['Mac'] = mailInfo[12]
        NodeValue['TimeB'] = time.mktime(time.strptime(str(mailInfo[13]), '%Y-%m-%d %H:%M:%S'))
        NodeValue['SrcPort'] = int(mailInfo[14])
        NodeValue['DstPort'] = int(mailInfo[15])
        NodeValue['FromCode'] = mailInfo[16]
        NodeValue['MailHeader'] = mailInfo[17]
        NodeValue['StreamFP'] = mailInfo[18]
        NodeValue['StreamFN'] = mailInfo[19]
        try:
            NodeValue['ThreatsSrc'] = int(blackInfo['Src'])
            NodeValue['ThreatsType'] = int(blackInfo['Type'])
        except Exception as e:
            print e
            NodeValue['ThreatsSrc'] = ''
            NodeValue['ThreatsType'] = ''

        print "======================= Tmail_Threats dbdata =================="
        for key in NodeValue.keys():
           if key == 'Content':
               pass
           else:
               print "%s: %s"%(key, NodeValue[key])
        ret = storageclient.Insert('TmailThreats', NodeValue)
        print "ret: ", ret
        return
        # return True

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception,e:
            print 'exit error'


def binary_search(lis, key):
    left = 0
    right = len(lis) -1
    time = 0
    while left <= right:
        time += 1
        mid = (left +right)//2
        # print mid
        if key == lis[mid]['IP']:
            print "times:%s"%time
            return mid
        elif key > lis[mid]['IP']:
            left = mid -1
        else:
            right = mid +1
    print "time:%s"%time
    return False

def main():
    MailblackCkeck()

if __name__ == '__main__':
    main()