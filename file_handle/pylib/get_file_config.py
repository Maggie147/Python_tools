# -*- encoding: utf-8-*-
#================================================
#  __title__ = 'Get file config'
#  __author__ = 'tx'
#  __mtime__ = '2017-12-08'
#=================================================
import io
import sys
import os
import time
import pprint
from xml.dom import minidom

reload(sys)
sys.setdefaultencoding('utf-8')

def get_attrvalue(node, attrname):
     return node.getAttribute(attrname) if node else ''
def get_nodevalue(node, index = 0):
    return node.childNodes[index].nodeValue if node else ''
def get_xmlnode(node,name):
    return node.getElementsByTagName(name) if node else []


def get_fileConfig(filename, module='RmFConfig'):
    '''
    read fileConfig['RmFConfig'] about remove file setting,
return dic named fileSet.
    '''
    try:
        doc = minidom.parse(filename)
        root = doc.documentElement          # get root Node, APT_FilePathConfig
        modulePer = get_xmlnode(root, module)
        fileSet = {}

        fSize = {}
        fileSizes = get_xmlnode(modulePer[0], 'FileSize')
        fSize['enable'] = get_attrvalue(fileSizes[0], "enable")
        fSize['unit'] = get_attrvalue(fileSizes[0], "unit")
        fSize['value'] = get_nodevalue(fileSizes[0])

        fTime = {}
        fileTimes = get_xmlnode(modulePer[0], 'FileTime')
        fTime['enable'] = get_attrvalue(fileTimes[0], "enable")
        fTime['unit'] = get_attrvalue(fileTimes[0], "unit")
        fTime['value'] = get_nodevalue(fileTimes[0])

        fileSet['FSize'] = fSize
        fileSet['FTime'] = fTime
        return fileSet
    except:
        print "GetXmlData failed"
        return None


def analyse_fileConfig(fileSet):
    '''
    analyse rmfile setting in 'fileConfig['RmFConfig'],
return FSize info unit is M; return FTime info unit is D(day).
    '''
    FSize = 0
    FTime = 0
    try:
        fileSize = fileSet['FSize']
        fileTime = fileSet['FTime']

        if fileSize['enable'] != '0':
            unitSize = fileSize['unit'].strip().upper()
            if "M" in unitSize:
                FSize = float(fileSize['value'])
            elif 'G' in unitSize:
                FSize = float(fileSize['value'].strip())*1024
            elif 'KB' in unitSize:
                FSize = float(fileSize['value'].strip())/1024

        if fileTime['enable'] != '0':
            unitTime = fileTime['unit'].strip().upper()
            if "D" in unitTime:
                FTime = float(fileTime['value'])
            elif 'M' in unitTime:
                FTime = float(fileTime['value'].strip())*30
            elif 'Y' in unitTime:
                FTime = float(fileTime['value'].strip())*365
    except Exception as e:
        print e
    return (FSize, FTime)


def test():
    module = "RmFConfig"
    confPath = "../conf/fileConfig.xml"
    fConf = get_fileConfig(confPath, module)

    # pprint.pprint(fConf)
    # pprint.pprint(fConf['FSize'])
    # pprint.pprint(fConf['FTime'])

    # get fszie unit is M, ftime unit is D(day)
    fszie, ftime = analyse_fileConfig(fConf)
    print "Config Setting [fszie: %.3f MB]" % fszie
    print "Config Setting [ftime: %.3f D]" % ftime


if __name__ == "__main__":
    test()



# def get_fileConfig222_testing(xmlfile, module='RmFConfig'):
#     import xml.etree.ElementTree as ET
#     try:
#         tree = ET.parse(xmlfile)
#         root = tree.getroot()
#         data = root.find(module)
#         module = {}
#         FSize = {}
#         FTime = {}
#         sizeValue = data.find('FileSize').text
#         timeValue = data.find('FileTime').text
#         return module
#     except:
#         print "read config file error!!!"
#         return None