#!/usr/bin/python
'''
MongoConnector.py

@Created On 2018-02-15
@Updated On 2018-02-15
@Author: tx

'''
# -*- coding: UTF-8 -*-
# from pymongo import MongoClient
# import pymongo, traceback
# import sys
# from xml.etree import ElementTree
# import time
# import cPickle as pickle
# import json
# import StringIO

import pymongo, traceback
from xml.etree import ElementTree
import time
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class MongoConnector(object):
    def __init__(self):
        conffile = './conf/SysSet.xml'
        tree = ElementTree.ElementTree(file = conffile)
        root = tree.getroot()
        node = root.find('database')

        if node is None:
            print 'There is no a node named database in the conf file: %s' % (conffile)
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
        if pwd is None:
            print 'There is no a node named db_address in the conf file: %s' % (conffile)
            sys.exit(1)
        port = node.find('db_port')
        if pwd is None:
            print 'There is no a node named db_port in the conf file: %s' % (conffile)
            sys.exit(1)

        uri = 'mongodb://%s:%s@%s:%s/%s' % (user.text, pwd.text, ip.text, port.text, db.text)
        self.__client = None
        self.__db = None
        try:
            self.__client = pymongo.MongoClient(host = uri, maxPoolSize = 1, socketKeepAlive = True)
            self.__db = self.__client[db.text]
        except Exception, e:
            print traceback.print_exc()
            sys.exit(1)

    def __del__(self):
        if self.__client is not None:
            self.__client.close()
            self.__client = None


    def insert(self, collection_name, doc):
        cursor = {}
        try:
            collection = self.__db[collection_name]
            cursor = collection.insert_one(doc)
        except Exception, e:
            print traceback.print_exc()
        finally:
            return cursor


    def insert_many(self, collection_name, docs):
        results = None
        try:
            collection = self.__db[collection_name]
            results = collection.insert_many(docs, False)
        except Exception, e:
            print traceback.print_exc()
        finally:
            return results


    def find(self, collection_name, query = None, field = None, sort = None, limit = 0):
        cursor = {}
        try:
            collection = self.__db[collection_name]
            cursor = collection.find(query, field, sort = sort, limit = limit)
        except Exception, e:
            print traceback.print_exc()
        finally:
            return cursor

    def find_one(self, collection_name, query, field=None):
        cursor = {}
        try:
            collection = self.__db[collection_name]
            cursor = collection.find_one(query, field)
        except Exception, e:
            print traceback.print_exc()
        finally:
            return cursor


    def update(self, collection_name, query, field, upsert=False):
        res = ''
        try:
            collection = self.__db[collection_name]
            res = collection.update_one(query, field, upsert)
        except Exception, e:
            print traceback.print_exc()
        return res


    def count(self, collection_name, query=None):
        c = 0
        try:
            collection = self.__db[collection_name]
            c = collection.count(query)
        except Exception, e:
            print traceback.print_exc()
        finally:
            return c

    def delete(self, collection_name, query = {}):

        try:
            collection = self.__db[collection_name]
            res =  collection.delete_many(query)
            print res.deleted_count
        except Exception, e:
            print traceback.print_exc()
            return False
        return True

    def drop(self, collection_name):
        try:
            collection = self.__db[collection_name]
            collection.drop()
        except pymongo.errors.PyMongoError,e:
            print str(e)

    def save(self, collection_name, doc):
        try:
            collection = self.__db[collection_name]
            collection.save(doc)
        except Exception, e:
            print traceback.print_exc()


    def aggregate(self, collection_name, pipeline):
        cursor = {}
        try:
            collection = self.__db[collection_name]
            cursor = collection.aggregate(pipeline)
        except Exception, e:
            print traceback.print_exc()
        finally:
            return cursor

def insert_test(mydb, collection_name):
    startTime = int(time.time())

    for i in range(1,10):
        insertInfo = {'Num':i, 'Time':int(time.time())}
        mydb.insert(collection_name, insertInfo)

    endTime = int(time.time())
    print "insert Time: ", endTime-startTime


def update_test(mydb, collection_name):
    insert_query = {'Num': 9}
    insert_value = {'$set':{'Num':1838040, 'Time':444444444}}
    mydb.update(collection_name, insert_query, insert_value)


def findPrint_test(mydb, collection_name):
    results = mydb.find(collection_name)
    for result in results:
        num = result.get('Num')
        Time = result.get('Time')

        print "Num: ", num
        print "Time: ", Time


if __name__ == '__main__':
    Mydb = MongoConnector()

    TestTable = "TestTable"

    findPrint_test(Mydb, TestTable)