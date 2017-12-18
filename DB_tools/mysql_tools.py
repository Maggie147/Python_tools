#! /usr/bin/env python
#coding=utf-8
#================================================
#  __title__ = 'mysql_tools'
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
# from xml.etree import ElementTree
import sys,time,os
# sys.path.append('./pylib/')
import storageclient

reload(sys)
sys.setdefaultencoding('utf8')

xmlpath = "./conf/DBSet.xml"


class SqlConnector(object):
    def __init__(self):
        self.xmlpath = xmlpath

        self.readconfig(xmlpath)
        self.connectmysql()

    def readconfig(self, xmlpath):
        try:
            print xmlpath
            tree = ET.parse(xmlpath)
            # tree = ET.ElementTree(file = xmlpath)
            root = tree.getroot()
            database = root.find('database')
            if not database:
                print "There is no a node named database in the file: %s"%(xmlpath)
                sys.exit(1)
            self.db_host = database.find('db_address').text if database.find('db_address') else None
            self.db_port = database.find('db_port').text if database.find('db_port') else None
            self.db_name = database.find('db_name').text if database.find('db_name') else None
            self.db_user = database.find('db_user').text if database.find('db_user') else None
            self.db_pwd  = database.find('db_pwd').text  if database.find('db_pwd')  else None
            if not self.db_host or not self.db_port or not self.db_name or not self.db_user or not db_pwd:
                print "db info not get all!!!"
                print "host:%s, port:%s, name:%s, user:%s, pwd:%s" % (self.db_host, self.db_host, self.db_name, self.db_user, self.db_pwd)
                sys.exit(1)
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


    def find_one(self, filed, query, table_name):
        try:
            sql = "select * from %s where %s = %s;" % (table_name, filed, query)
            self.cursor.execute(sql)
            info = self.cursor.fetchone()
        except Exception as e:
            print e, "find mail by Id failed!!!"
            return info

    def find_man(self, filed, query, table_name, limit):
        try:
            sql = "select * from %s where %s = %s order by Id limit %d;" % (table_name, filed, query, limit)
            self.cursor.execute(sql)
            # info = self.cursor.fetchall()
            info = self.cursor.fetchman()
        except Exception as e:
            print e, "find mail by Id failed!!!"
            return info

def main():
    sqlCursor = SqlConnector()
    result = sqlCursor.find()

if __name__ == '__main__':
    main()