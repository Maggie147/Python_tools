#!/usr/bin/env python
#coding=utf-8
'''
mongo_test.py

@Created On 2018-02-15
@Updated On 2018-02-15
@Author: tx

'''
from mongodb import mongodb
import pymongo, traceback
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def insert_test(mydb, collection_name):
    startTime = int(time.time())

    for i in range(10, 20):
        insertInfo = {'Num':i, 'Time':int(time.time())}
        mydb.insert(collection_name, insertInfo)

    endTime = int(time.time())
    print "insert Time: ", endTime-startTime


def update_test(mydb, collection_name):
    insert_query = {'Num': 15}
    insert_value = {'$set':{'Num':6666666, 'Time':444444444}}
    mydb.update(collection_name, insert_query, insert_value)


def findPrint_test(mydb, collection_name):
    results = mydb.find(collection_name)
    for result in results:
        num = result.get('Num')
        Time = result.get('Time')

        print "Num: ", num
        print "Time: ", Time


if __name__ == '__main__':
    conffile = './conf/SysSet.xml'

    Mydb = mongodb.MongoConnector(conffile)

    TestTable = "TestTable"

    insert_test(Mydb, TestTable)

    update_test(Mydb, TestTable)

    findPrint_test(Mydb, TestTable)