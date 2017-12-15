#! /usr/bin/env python
#coding=utf-8
#================================================
#  __title__ = 'Tmail Black check  DB_Way'
#  __author__ = 'tx'
#  __mtime__ = '2017-12-12'
#=================================================
#
import MySQLdb
import re
import time
import pprint
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

# mail_srcip = "5.62.153.248"
# mail_dstip = "192.168.6.135"
# domain = "021id.net"


class MailblackCkeck(object):
    def __init__(self):
        # self.limit_count = 100000
        self.limit_count = 100
        self.begin_id = 0
        self.total_mail = 0
        self.cycle_num = 0
        self.check_num = 0
        self.readconfig(xmlpath)
        self.connectmysql()

        print "get start Mail Info..."
        ret = self.get_startMail('TmailThreats', 'TMail')
        if ret[0] >= ret[1]:
            print "not received New Mail!!!"
            sys.exit(1)

        self.begin_id += ret[0]
        self.total_mail = ret[1]

        print "mail black check start..."
        print "start_id", self.begin_id
        print "total_mail: ", self.total_mail


        while True:
            if self.begin_id >= self.total_mail:
                print "no new mail!!!"
                # break
                print "keep alive..."
                time.sleep(60)

            self.cycle_num += 1
            self.mail_black_check(self.begin_id)
            # time.sleep(5)

        print "cycle_num: ", self.cycle_num

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

    def get_startMail(self, table1='TmailThreats', table2='TMail'):
        sql1 = "select MailId from %s order by MailId desc limit 1"%table1
        # sql1 = "select Id from %s order by Id desc limit 1"%table1             # TmailThreats
        sql2 = "select Id from %s order by Id desc limit 1"%table2               # Tmail
        start_id = 0
        mail_maxid = 1
        try:
            self.cursor.execute(sql1)
            result = self.cursor.fetchall()
            if result:
                start_id = result[0][0]
                # print "TmailThreats start_id: ", start_id
            else:
                print "no data in TmailThreats!!"
                pass

            self.cursor.execute(sql2)
            mail_status = self.cursor.fetchall()
            if mail_status:
                mail_maxid = mail_status[0][0]
                # print "mail_maxid: ", mail_maxid
            else:
                print "no data in Tmail, not get mail_maxid!!!"
                pass

            return (start_id, mail_maxid)
            # return (5, mail_maxid)
        except Exception as e:
            print e, "get_startMail error!!!"
            return (start_id, mail_maxid)


    def ip_search(self, table, ip):
        try:
            result = {}
            sql = "select * from %s where IP = \'%s\';" % (table, ip)
            # print sql
            self.cursor.execute(sql)
            ip_blacks = self.cursor.fetchall()
            if ip_blacks:
                # print "find ip[%s]"%ip
                for ip_black in ip_blacks:
                    # result = {'IP':None, 'Time':None, 'Src':None, 'Type':None}
                    # result['Id'] = ip_black[0]
                    result['IP'] = ip_black[1]
                    result['Time'] = ip_black[2]
                    result['Src'] = ip_black[3]
                    result['Type'] = ip_black[4]
                    return result
            else:
                # print "no find ip[%s]"%ip
                return result
        except Exception as e:
            print e, "ip_search error"
            return result


    def domain_search(self, table, domain):
        try:
            result = {}
            args = '%'+domain+'%'
            sql = "select * from %s where Domain like \'%s\';" % (table, args)
            # print sql
            self.cursor.execute(sql)
            ip_blacks = self.cursor.fetchall()
            if ip_blacks:
                for ip_black in ip_blacks:
                    result['Domain'] = ip_black[1]
                    result['Time']   = ip_black[2]
                    result['Src']    = ip_black[3]
                    result['Type']   = ip_black[4]
                    return result
            else:
                # print "no find domain[%s]"%domain
                return result
            return result
        except Exception as e:
            print e, "ip_search error"
            return result

    def mail_black_check(self, start):
        mailcon_sql1 = "select Id, INET_NTOA(IPaddress), INET_NTOA(DstIPaddress), Content\
        from TMail where Id > %d order by Id limit %d;" % (int(start), self.limit_count)
        count = self.cursor.execute(mailcon_sql1)                                                    # print self.cursor.rowcount
        # print "count: ", count
        self.begin_id += count
        mail_infos = self.cursor.fetchall()
        if not mail_infos:
            print "TMailContent didn't find datas!"
            return
        for mailInfo in mail_infos:                                                                  # mailInfo[0], mailInfo[1], mailInfo[2], mailInfo[3] = Id, srcip , dstip, content
            print "Mail_Id: ", mailInfo[0]
            blackInfo = {'SrcipSrc':None, 'SrcipType':None, 'SrcipTime':None,\
                        'DstipSrc':None, 'DstipType':None, 'DstipTime':None, 'ContResult':None}

            print "check ip..."
            srcip_result = self.ip_search('ip_threats', mailInfo[1])
            #srcip_result = self.ip_search('ip_threats', "96.81.131.84")                               # for test
            # (blackInfo['SrcipSrc'], blackInfo['SrcipType'], blackInfo['SrcipTime']) = (int(srcip_result['Src']), int(srcip_result['Type']), int(srcip_result['Time']))if srcip_result else (None, None, None)
            if srcip_result:
                blackInfo['SrcipSrc'] = int(srcip_result['Src'])
                blackInfo['SrcipType'] = int(srcip_result['Type'])
                blackInfo['SrcipTime'] = srcip_result['Time']

            dstip_result = self.ip_search('ip_threats', mailInfo[2])
            if srcip_result:
                blackInfo['DstipSrc'] = int(dstip_result['Src'])
                blackInfo['DstipType'] = int(dstip_result['Type'])
                blackInfo['DstipTime'] = dstip_result['Time']

            print "check domain..."
            domains = get_domain(mailInfo[3])
            if domains:
                for domain_tmp in domains:
                    if "silence.com" in domain_tmp[1]:
                        continue
                    # print "domain: ", domain_tmp[1]
                    try:
                        domain  = domain_tmp[1].split('.')
                        domain_result = self.domain_search('domain_threats', domain[0].strip()+domain[1].strip())
                        if not domain_result:
                            domain_result = self.domain_search('domain_threats', domain[1].strip()+domain[2].strip())
                        if domain_result:
                            if blackInfo['ContResult']:
                                blackInfo['ContResult'] = str(blackInfo['ContResult']) + ';' + str(domain_result['Src'])+'_'+ str(domain_result['Type'])+'_'+ str(domain_result['Time'])
                            else:
                                blackInfo['ContResult'] = str(domain_result['Src'])+'_'+ str(domain_result['Type'])+'_'+ str(domain_result['Time'])
                    except Exception as e:
                        print e, "find domain error!!!"
                        continue


            if ((blackInfo['SrcipSrc'] and blackInfo['SrcipType']) or \
                (blackInfo['DstipSrc'] and blackInfo['DstipType']) or \
                (blackInfo['ContResult'])):
                try:
                    print "^^"*30, "blackInfo start"
                    pprint.pprint(blackInfo)
                    print "<<"*30, "blackInfo end"

                    self.insert(mailInfo[0], blackInfo)
                    print "<<<"*30, "insert end\n"
                    continue
                except Exception as e:
                    print e, "insert error"
                    continue
        self.check_num += count
        return


    def insert(self, Id, blackInfo):
        try:
            mail_sql = "select * from TMail where Id = %s;" % Id
            self.cursor.execute(mail_sql)
            mailInfo = self.cursor.fetchone()
        except Exception as e:
            print e, "find mail by Id failed!!!"
            return

        NodeValue = {}
        NodeValue['MailId'] = int(Id)                         # mailInfo[0]
        NodeValue['AppName'] = mailInfo[1]
        NodeValue['MailFrom'] = mailInfo[2]
        NodeValue['MailTo'] = mailInfo[3]
        NodeValue['Subject'] = mailInfo[4]
        NodeValue['Content'] = mailInfo[5]
        # NodeValue['Subject'] = "aa"
        # NodeValue['Content'] = "bb"
        NodeValue['AttachFile'] = mailInfo[6]
        NodeValue['AttachPath'] = mailInfo[7]
        NodeValue['Type']= mailInfo[8]
        NodeValue['IPaddress'] = int(mailInfo[10])
        NodeValue['DstIPaddress'] = int(mailInfo[11])
        NodeValue['Mac'] = mailInfo[12]
        NodeValue['SrcPort'] = int(mailInfo[14])
        NodeValue['DstPort'] = int(mailInfo[15])
        NodeValue['FromCode'] = mailInfo[16]
        NodeValue['MailHeader'] = mailInfo[17]
        NodeValue['StreamFP'] = mailInfo[18]
        NodeValue['StreamFN'] = mailInfo[19]
        try:
            NodeValue['SendTime'] = time.mktime(time.strptime(str(mailInfo[9]), '%Y-%m-%d %H:%M:%S'))
        except Exception as e:
            NodeValue['SendTime'] = ''
        try:
            NodeValue['TimeB'] = time.mktime(time.strptime(str(mailInfo[13]), '%Y-%m-%d %H:%M:%S'))
        except Exception as e:
            NodeValue['TimeB'] = ''

        NodeValue['SrcipSrc'] = blackInfo['SrcipSrc']
        NodeValue['SrcipType'] = blackInfo['SrcipType']
        NodeValue['SrcipTime'] = blackInfo['SrcipTime']
        NodeValue['DstipSrc'] = blackInfo['DstipSrc']
        NodeValue['DstipType'] = blackInfo['DstipType']
        NodeValue['DstipTime'] = blackInfo['DstipTime']
        NodeValue['ContResult'] = blackInfo['ContResult']

        print "======================= Tmail_Threats dbdata =================="
        for key in NodeValue.keys():
           if key == 'Content':
               pass
           else:
               print "%s: %s"%(key, NodeValue[key])
        ret = storageclient.Insert('TmailThreats', NodeValue)
        print "ret: ", ret
        return

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception,e:
            print 'exit error'

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
     MailblackCkeck()



if __name__ == '__main__':
    main()
