#coding=utf-8
'''
mysql_test.py
@Created On 2018-02-15
@Updated On 2018-02-15
@Author: tx
'''

from mysqldb import mysqldb
import MySQLdb
import sys
import time


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


def main():
    xmlpath = './conf/SysSet.xml'

    Mysql = mysqldb.SqlConnector(xmlpath)

    TestTable = "TestTable"

    start_time = time.time()

    for i in range(1, 10):
        insertInfo = {'Num':str(i), 'Time':int(time.time())}
        insert_test(Mysql.cursor, Mysql.conn, TestTable, insertInfo)

    end_time = time.time()
    print "Insert  time: %d" % (end_time-start_time)



    result = Mysql.find_one(TestTable, 'Num', '5')
    print result

    print "find all: "
    result2 = Mysql.find_many(TestTable, limit=100)
    for i in result2:
        print i



if __name__ == "__main__":
    main()