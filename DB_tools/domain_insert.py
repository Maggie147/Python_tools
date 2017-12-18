#coding=utf-8

# __title__ = 'domain_Insert'
# __author__ = 'tx'
# __mtime__ = '2017-12-12'

import os
import sys
import string
import xml.etree.ElementTree as ET
import MySQLdb
import time

configPath = "/home/APT/conf/SysSet.xml"
blackip_path = "/home/share/dns_conf/black_domain.conf"
# blackip_path = "./black_domain.txt"

DB = {}
def readConfig(xmlpath):
    global DB
    try:
        tree = ET.parse(xmlpath)
        root = tree.getroot()
        database = root.find('database')
        db_host  = database.find('db_address').text
        db_name = database.find('db_name').text
        db_user = database.find('db_user').text
        db_pwd  = database.find('db_pwd').text
        DB['DB_Host'] = db_host
        DB['DB_Name'] = db_name
        # DB['DB_Port'] = db_port
        DB['DB_User'] = db_user
        DB['DB_Pwd'] = db_pwd
        DB['DB_Charset'] = 'utf8'
    except Exception,e:
        print "Readconfig failed error: %s \n" %e
        return False
    return True

def connectMysqlDB(DB={}):
    try:
        conn = MySQLdb.connect(host = DB['DB_Host'],
            user = DB['DB_User'],
            passwd = DB['DB_Pwd'],
            db = DB['DB_Name'])
        cur = conn.cursor()
        if not conn:
            print "connect mysql failed..."
            sys.exit(1)
        print "connect mysql succeed..."
        return conn, cur
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return None, None

def main():
    ret = readConfig(configPath)
    if not ret:
        print "Read system xmlfile error!!!"
        sys.exit(1)
    print DB

    conn, cur = connectMysqlDB(DB)
    if not conn or not cur:
        print "connectMysqlDB failed..."
        sys.exit(1)

    start_time = time.time()

    # failed_list = []
    lineNum = 0
    fpath = blackip_path
    with open(fpath, 'r') as file:
        print "open file[%s]"%fpath
        print "insert mysql[domain_threats]..."
        lines = file.readlines()
        for item in lines:
            info  = item.split('|')
            try:
                sql = "insert into domain_threats(Id, Domain, Time, Src, Type) values(null, '%s', '%s', '%d','%d')" % (\
                    MySQLdb.escape_string(info[0].strip()), \
                    MySQLdb.escape_string(info[1].strip()), \
                    int(MySQLdb.escape_string(info[2].strip())), \
                    int(MySQLdb.escape_string(info[3].strip())))
                # print sql
                cur.execute(sql)
                conn.commit()
                lineNum += 1
            except MySQLdb.Error, e:
                # print "insert data into Mysql Error %d: %s" % (e.args[0], e.args[1])
                # failed_item = {'Domain':info[0], 'Time':info[1], 'Src':info[2], 'Type':info[3]}
                # failed_list.append(failed_item)
                continue
    cur.close()
    conn.close()
    end_time = time.time()
    # print failed_list
    print "Insert domain_threats time: %d" % (end_time-start_time)


if __name__ == "__main__":
    main()