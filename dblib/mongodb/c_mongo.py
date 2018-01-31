# -*- coding: utf-8 -*-
#  __title__ = ' '
#  __author__ = ''
#  __mtime__ = '2018-01-23'
import os
import sys
import time
import string
import pprint
import re
import json
from ctypes import *
import cPickle as pickle
import traceback
# from bson import ObjectId
sys.path.append('/home/pylib/')
# from storage import storage
# from storage import datastruct
reload(sys)
sys.setdefaultencoding('utf8')


def usage():
    print """-d , no option"""

def get_sysArgv():
    global g_iDEBUG

    if len(sys.argv) == 1:
        usage()
    else:
        if sys.argv[1].startswith('-'):
            option = sys.argv[1][1:]
        if sys.argv[1].startswith('--'):
            option = sys.argv[1][2:]
        else:
            usage()
            sys.exit()

        option_tmp = option.lower()     #lower(); upper()

        if option_tmp == 'version':
            print "Version 1.0"
        elif option_tmp  == 'help':
            usage()
        elif option_tmp  == 'd':
            g_iDEBUG = 1
        else:
            print "Unknown option."
        sys.exit()
    # return inputSting


class RecordID(object):
    def __init__(self):
        self.datfile = '/home/idata/getPostId'
        # self.datfile = '/home/idata/GetId.txt'
        # self.datfile = '/home/idata/PostId.txt'

    def read_id(self):
        count_dict = {'TGetAction': '000000000000000000000000', 'TPostAction': '000000000000000000000000'}
        if os.path.exists(self.datfile) is False:
            return count_dict

        myfile = open(self.datfile, 'rb')
        try:
            count_dict = pickle.load(myfile)
        except Exception, e:
            print e
        myfile.close()
        os.remove(self.datfile)
        return count_dict

    def write_id(self, count_dict):
        myfile = open(self.datfile, 'wb')
        pickle.dump(count_dict, myfile)
        myfile.close()


class MongoCtrl(object):
    def __init__(self):
        self.db = self._connect_mongo()

    def _connect_mongo(self):
        mongo_client = None
        try:
            mongo_client = cdll.LoadLibrary("/home/solib/system/libeasymongo.so")
        except Exception, e:
            traceback.print_exc()
            sys.exit(1)

        return mongo_client

    def find_mongo(self, query, field, collection, limit, docs):
        count = 0
        try:
            count = self.db._find(query, field, collection, limit, byref(docs))
        except Exception, e:
            print e
        finally:
            return count, docs

    def insert_mongo(self, query, field, collection):
        count = 0
        try:
            count = self.db._replace(query, field, collection)
        except Exception, e:
            print e
        finally:
            return count

    def freeMery(self, type, size):
        self.db._free(type, size)


class DealWithTableData(object):
    def __init__(self):
        c_str = {}
        # c_str['_id'] = 1
        c_str['H010042'] = 1
        c_str['G010002'] = 1
        c_str['G010003'] = 1
        c_str['C110008'] = 1            # get NickName, Uid
        c_str['B040022'] = 1
        c_str['F020004'] = 1
        c_str['F020005'] = 1
        c_str['C040002'] = 1
        c_str['H010014'] = 1
        c_str['F020006'] = 1
        c_str['F020007'] = 1
        c_str['F010008'] = 1
        self.LIMIT = 100
        self.c_limit = c_int32(self.LIMIT)
        self.c_docs = (c_char_p * self.LIMIT)()
        self.c_field = json.JSONEncoder().encode(c_str)

        self.regulr = re.compile(r'(?<= uin=o)[1-9]{1}\d{5,}?(?=;)|(?<= uin=o)[1-9]{1}\d{5,}?$', re.VERBOSE | re.IGNORECASE)

    def searchData(self, mydb, id1, id2, data=[], index=[]):
        getData = []
        postData = []
        ret = self._searchData(mydb, 'TGetAction', id1, data)
        if not ret:
            print "no more data"
        index1 = self.index
        ret = self._searchData(mydb, 'TPostAction', id2, data)
        if not ret:
            print "no more data"
        index2 = self.index
        index.append(index1)
        index.append(index2)


    def _searchData(self, mydb, tablename, index, data=[]):
        c_collection = c_char_p(tablename)

        query_info = '{"$query": {"_id": {"$gt": {"$oid": "%s"}}}, "$orderby": {"_id": 1}}' % (index)
        # query_info = '{"_id": {"$gt": {"$oid": "%s"}}}' % (index)

        c_query = c_char_p('{"_id":{"$gt":{"$oid":"%s"}}}' % index)

        count, docs = mydb.find_mongo(c_query, self.c_field, c_collection, self.c_limit, self.c_docs)
        if count:
            for i in range(count):
                try:
                    temp = json.loads(docs[i])
                except Exception, e:
                    try:
                        temp = eval(docs[i])
                    except Exception as e:
                        print e
                        continue

                index = temp['_id']['$oid']

                # print "tablename: %s"%tablename, index

                c_str = {}
                try:
                    c_str['C110008'] = temp['C110008']
                except Exception, e:
                    #print e
                    continue

                try:
                    c_str['H010014'] = temp['H010014']
                except Exception, e:
                    pass
                try:
                    c_str['F020004'] = temp['F020004']
                except Exception, e:
                    pass
                try:
                    c_str['F020005'] = temp['F020005']
                except Exception, e:
                    pass
                try:
                    c_str['F020006'] = temp['F020006']
                except Exception, e:
                    pass
                try:
                    c_str['F020007'] = temp['F020007']
                except Exception, e:
                    pass
                try:
                    c_str['B040022'] = temp['B040022']
                except Exception, e:
                    pass
                try:
                    c_str['C040002'] = temp['C040002']
                except Exception, e:
                    pass
                try:
                    c_str['F010008'] = temp['F010008']
                except Exception, e:
                    pass

                data.append(c_str)
                # print "tablename[%s] len data: "%tablename, len(data)

        # print "tablename[%s] len data: "%tablename, len(data)

        print "tablename[%s] count: "%tablename, count
        print "LIMIT: ", self.LIMIT

        self.index = index
        mydb.freeMery(byref(docs), count)

        if count < self.LIMIT:
            return 0
        else:
            return 1

    def print_data(self):
        pprint.pprint(c_str)

    def insertData(self, mydb, data=[]):
        for oneData in data:
            info = oneData['C110008']

            QQ = self._getQQNumberInfo(info)
            if QQ == None:
                continue

            try:
                sip = oneData['F020004']
            except Exception, e:
                sip = None
            try:
                dip = oneData['F020005']
            except Exception, e:
                dip = None
            try:
                sport = oneData['F020006']
            except Exception, e:
                sport = None
            try:
                dport = oneData['F020007']
            except Exception, e:
                dport = None
            try:
                mac = oneData['C040002']
            except Exception, e:
                mac = None
            try:
                account = oneData['B040022']
            except Exception, e:
                account = None
            try:
                itime = oneData['H010014']
            except Exception, e:
                itime = None
            try:
                collectaddr = oneData['F010008']
            except Exception, e:
                collectaddr = None

            self._insertData(mydb, mac, account, sip, dip, sport, dport, itime, collectaddr, QQ)

    def _insertData(self, mydb, mac, account, sip, dip, sport, dport, itime, collectaddr, QQ):
        c_str = {}

        if mac:
            c_str['C040002'] = mac
        if account:
            c_str['B040022'] = account
        if sip:
            c_str['F020004'] = sip
        if dip:
            c_str['F020005'] = dip
        if sport:
            c_str['F020006'] = sport
        if dport:
            c_str['F020007'] = dport
        if itime:
            c_str['H010014'] = itime
        if collectaddr:
            c_str['F010008'] = collectaddr

        c_str['B040002'] = QQ
        c_str['H010003'] = '30'
        c_str['C020017'] = '01'

        c_query = json.JSONEncoder().encode(c_str)
        c_field = json.JSONEncoder().encode(c_str)
        c_collection = c_char_p('TQQIndividual')

        mydb.insert_mongo(c_query, c_field, c_collection)

    def _getQQNumberInfo(self, data):

        ret = self.regulr.search(data)
        if ret:
            return ret.group()
        return None

def test():
    mydb = MongoCtrl()
    myid = RecordID()
    myData = DealWithTableData()

    while True:
        count_dict = myid.read_id()
        index1 = count_dict['TGetAction']
        index2 = count_dict['TPostAction']

        print "TGetAction  id: ", index1
        print "TPostAction id: ",index2

        index = []
        data = []
        myData.searchData(mydb, index1, index2, data, index)

        # myData.insertData(mydb, data)

        index1 = index[0]
        index2 = index[1]

        count_dict['TGetAction'] = index1
        count_dict['TPostAction'] = index2

        print "TGetAction  id: ", index1
        print "TPostAction id: ",index2

        myid.write_id(count_dict)
        print "sleep 10s , waitting next times"
        time.sleep(10)


if __name__ == "__main__":
    test()