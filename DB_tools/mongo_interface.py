#!/usr/bin/python
# -*- coding: utf-8 -*-  
'''
    @File        mongo_interface.py
    @Author      pengsen cheng
    @Company     bhyc
    @CreatedDate 2015-06-18
'''
import sys, os
dir = os.path.realpath(__file__)
for i in range(3):
    dir = os.path.dirname(dir)
sys.path.append(dir)

from storage import datastruct, opcode
from MongoConnector import MongoConnector
from MongoBuilder import MongoBuilder 
import socket, struct, pymongo, ctypes
from storage.tools.MyLog import MyLog
#from storage.tools.Redis import Redis
from storage.tools.MemCache import MemCache

def insert_into_mongo(data):
    builder = MongoBuilder(data)
    connector = MongoConnector()

    # md5 = {}
    # ttl = builder.get_md5(data, md5)
    # if ttl is not None:
    #     tag, count = connector.count(md5, ttl)
    #     if count > 0:
    #         return opcode.DO_ERROR_RKEY
    #     else:
    #         builder.insert_md5(md5)
    #         connector.insert(md5, ttl)

    md5, seconds = builder.get_md5_str(data)
    if seconds != 0:
#         redis = Redis()
#         if redis.isexist(md5) is True:
#             return opcode.DO_ERROR_RKEY
# 
#         redis.set(md5, seconds)
        mc = MemCache()
        if mc.isexist(md5) is True:
            return opcode.DO_ERROR_RKEY
 
        mc.set(md5, seconds)

    bson = {}
    builder.build_insert_bson(data, bson)
    #print builder.get_collection_name(), bson
    
    now = 0;
    if bson.has_key('H010014') is True:
        now = bson['H010014']
    collection = builder.get_collection_name(now)

    tag = connector.insert(bson, collection)

    value = {}
    bson = {}
    collection = builder.build_replace_bson(data, bson, value)
    if collection is not None:
        connector.replace(bson, value, collection);

    return tag

def replace_of_mongo(data):
    builder = MongoBuilder(data)
    connector = MongoConnector()
    value = {}
    bson = {}
    collection = builder.build_replace_bson(data, bson, value)
    if collection is not None:
        connector.replace(bson, value, collection);
    return tag


def insert_into_mongo_with_collection(bson, collection_name):
    connector = MongoConnector()
    return connector.insert(bson, collection_name)

def bind_account_mongo(ip, port, mac_in_package, auth_type):
    query = {}
    ip = ctypes.c_int32(int(ip)).value
    MongoBuilder.bind_account(ip, port, query)

    Account = None
    Mac = mac_in_package
    if auth_type == 1:
        Account = mac_in_package
    else:
        Account = socket.inet_ntoa(struct.pack("!i", ip))

    connector = MongoConnector()
    tag, cursor = connector.find(query, None, "TAccount_M")
    
    if tag == opcode.DO_OK:
        tag = opcode.DO_UNSUCCESS
        try:
            for doc in cursor:
                Account = doc['B040022']
                Mac = doc['C040002']
                tag = opcode.DO_SUCCESS
        except pymongo.errors.PyMongoError, e:
            log = MyLog()
            log.write('ERROR: %s\n', str(e))
            tag = opcode.DO_ERROR_UN
            
    return tag, Account, Mac 

def bind_address_mongo(Account):
    query = {}
    MongoBuilder.bind_address(Account, query)

    gisinfo = datastruct.GisInfo()
    connector = MongoConnector()
    tag, cursor = connector.find(query, None, "TAddress_M");
    
    if tag == opcode.DO_OK:
        tag = opcode.DO_UNSUCCESS
        try:
            for doc in cursor:
                gisinfo.isNew = 1
                if doc.has_key('F010001'):
                    gisinfo.x = doc['F010001']
                if doc.has_key('F010002'):
                    gisinfo.y = doc['F010002']
                if doc.has_key('G020017'):
                    gisinfo.Street = doc['G020017']
                if doc.has_key('Z118010'):
                    gisinfo.AppName = doc['Z118010']
                tag = opcode.DO_SUCCESS
        except pymongo.errors.PyMongoError, e:
            log = MyLog()
            log.write('ERROR: %s\n', str(e))
            tag = opcode.DO_ERROR_UN
        
    return tag, gisinfo

def bind_ipaddress_mongo(Account):
    query = {}
    MongoBuilder.bind_ipaddress(Account, query)

    ip = None
    bport = None
    eport = None
    connector = MongoConnector()
    tag, cursor = connector.find(query, None, "TAccount_M");
    
    if tag == opcode.DO_OK:
       tag = opcode.DO_UNSUCCESS
       try:
           for doc in cursor:
               ip = doc['F020004']
               bport = doc['Z118001']
               eport = doc['Z118002']
               tag = opcode.DO_SUCCESS
       except pymongo.errors.PyMongoError, e:
           log = MyLog()
           log.write('ERROR: %s\n', str(e))
           tag = opcode.DO_ERROR_UN
    
    return tag, ip, bport, eport 

def find_from_mongo(query, field, collection_name):
    connector = MongoConnector()
    tag, cursor = connector.find(query, field, collection_name)
    
    dataset = []
    if tag == opcode.DO_OK:
        try:
            for doc in cursor:
                dataset.append(doc)
        except pymongo.errors.PyMongoError, e:
            log = MyLog()
            log.write('ERROR: %s\n', str(e))
            tag = opcode.DO_ERROR_UN
            dataset = []
    
    return tag, dataset
