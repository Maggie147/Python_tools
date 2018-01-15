#! /usr/bin/env python
#coding=utf-8
'''
mysql_tools.py
@Created On 2018-02-15
@Updated On 2018-02-15
@Author: tx
'''
import MySQLdb
import xml.etree.ElementTree as ET
# from xml.etree import ElementTree

import re
import time
import pprint
from datetime import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class SqlConnector(object):
    def __init__(self, conffile):
        self.readconfig(conffile)
        self.connectmysql()

    def readconfig(self, conffile):
        try:
            print conffile
            tree = ET.parse(conffile)
            # tree = ET.ElementTree(file = conffile)
            root = tree.getroot()
            node = root.find('database')
            if node is None:
                print "There is no a node named database in the file: %s"%(conffile)
                sys.exit(1)

            db = node.find('db_name')
            if db is None:
                print 'There is no a node named db_name in the conf file: %s' % (conffile)
                sys.exit(1)
            user = node.find('db_user')
            if user is None:
                print 'There is no a node named db_user in the conf file: %s' % (conffile)
                sys.exit(1)
            pwd = node.find('db_pwd')
            if pwd is None:
                print 'There is no a node named db_pwd in the conf file: %s' % (conffile)
                sys.exit(1)
            ip = node.find('db_address')
            if ip is None:
                print 'There is no a node named db_address in the conf file: %s' % (conffile)
                sys.exit(1)
            # port = node.find('db_port')
            # if port is None:
            #     print 'There is no a node named db_port in the conf file: %s' % (conffile)
            #     sys.exit(1)

            self.db_host = ip.text
            self.db_name = db.text
            self.db_user = user.text
            self.db_pwd  = pwd.text

            if not self.db_host or not self.db_name or not self.db_user or not self.db_pwd:
                sys.exit(1)

            print "host:%s, port:None, name:%s, user:%s, pwd:%s" % (self.db_host, self.db_name, self.db_user, self.db_pwd)

        except Exception,e:
            print "Readconfig failed error: %s \n" % e
            sys.exit(1)

    def connectmysql(self):
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


    def find_one(self, table_name, filed, query):
        try:
            sql = "select * from %s where %s = %s;" % (table_name, filed, query)
            self.cursor.execute(sql)
            info = self.cursor.fetchone()
            return info
        except Exception as e:
            print e, "find mail by Id failed!!!"
            return None


    def find_many(self, table_name,  filed=None, query=None, limit=10):
        try:
            if filed and query:
                sql = "select * from %s where %s = %s order by Id limit %d;" % (table_name, filed, query, limit)
            else:
                sql = "select * from %s order by Id limit %d;" % (table_name, limit)

            self.cursor.execute(sql)
            info = self.cursor.fetchall()
            # info = self.cursor.fetchmany()
            return info
        except Exception as e:
            print e, "find mail by Id failed!!!"
            return None


def insert_test(cur, conn, table_name, info):
    try:
        sql = "insert into %s(Id, Num, Time) values(null, '%s',  %d)" % (table_name,
            MySQLdb.escape_string(info['Num'].strip()), info['Time'])
        # print sql
        cur.execute(sql)
        conn.commit()
        print "'%s' success"%sql
    except MySQLdb.Error, e:
        print "'%s' failed!!!"%sql
        print e


def test():
    xmlpath = './conf/SysSet.xml'
    Mysql = SqlConnector(xmlpath)

    TestTable = "TestTable"

    # for i in range(1, 10):
    #     insertInfo = {'Num':str(i), 'Time':int(time.time())}
    #     insert_test(Mysql.cursor, Mysql.conn, TestTable, insertInfo)

    result = Mysql.find_one(TestTable, 'Num', '5')
    print result

    print "find all: "
    result2 = Mysql.find_many(TestTable, limit=10)
    for i in result2:
        print i


if __name__ == '__main__':
    test()
