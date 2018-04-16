# -*- encoding: utf-8-*-
#  __title__ = '[ get_config_value ]'
#  __author__ = 'tx'
#  __mtime__ = '2018-04-16'

import io
import sys
import os
import time
import pprint
from xml.dom import minidom
reload(sys)
sys.setdefaultencoding('utf-8')


g_iDEBUG = 0
def DEBUG(*value):
    if g_iDEBUG == 1:
        t = time.strftime("%Y-%m-%d %H:%M:%S")
        # filename = sys.argv[0][sys.argv[0].rfind(os.sep)+1:]
        filename = os.path.splitext(os.path.basename(__file__))[0]
        print "[python2.7][%s,%s]:" % (filename, t),
        for i in value:
            print i,
        print ""


def get_config(xmlpath, Node='rmConfig'):
    import xml.etree.ElementTree as ET
    try:
        tree = ET.parse(xmlpath)
        root = tree.getroot()                       # get root Node, <fileConfig>
        rmNode = root.find(Node)                    # get <rmConfig>
        result = {}
        for child in rmNode:
            tmp_dic = child.attrib
            tmp_dic['value'] = child.text
            result[child.tag] = tmp_dic
        return result
    except Exception as e:
        print("{} \nGetXmlData failed!".format(e))
        return None


def get_config2(xmlpath, Node='rmConfig'):
    try:
        doc = minidom.parse(xmlpath)
        root = doc.documentElement                   # get root Node, <fileConfig>
        rmNode = _get_xmlnode(root, Node)            # get <rmConfig>
        result = {}

        size = {}
        fsize = _get_xmlnode(rmNode[0], 'fsize')
        size['enable'] = _get_attrvalue(fsize[0], "enable")
        size['unit']   = _get_attrvalue(fsize[0], "unit")
        size['value']  = _get_nodevalue(fsize[0])

        time = {}
        ftime = _get_xmlnode(rmNode[0], 'ftime')
        time['enable'] = _get_attrvalue(ftime[0], "enable")
        time['unit']   = _get_attrvalue(ftime[0], "unit")
        time['value']  = _get_nodevalue(ftime[0])

        result['fsize'] = size
        result['ftime'] = time
        return result
    except Exception as e:
        print("{} \nGetXmlData failed!".format(e))
        return None

def _get_attrvalue(node, attrname):
     return node.getAttribute(attrname) if node else ''
def _get_nodevalue(node, index = 0):
    return node.childNodes[index].nodeValue if node else ''
def _get_xmlnode(node,name):
    return node.getElementsByTagName(name) if node else []



def analyse_config(param):
    '''
return FSize default unit M; return FTime default unit D(day).
    '''
    fsize = ftime = 0
    try:
        OverSize = param.get('fsize')
        OverTime = param.get('ftime')

        if OverSize['enable'] != '0':
            unit = OverSize['unit'].strip().upper()
            if "M" in unit:
                fsize = float(OverSize['value'])
            elif 'G' in unit:
                fsize = float(OverSize['value'].strip())*1024
            elif 'KB' in unit:
                fsize = float(OverSize['value'].strip())/1024

        if OverTime['enable'] != '0':
            unit = OverTime['unit'].strip().upper()
            if "D" in unit:
                ftime = float(OverTime['value'])
            elif 'M' in unit:
                ftime = float(OverTime['value'].strip())*30
            elif 'Y' in unit:
                ftime = float(OverTime['value'].strip())*365
    except Exception as e:
        print(e)
    finally:
        return (fsize, ftime)


def get_config_value(xmlpath, Node, debug=0):
    global g_iDEBUG
    g_iDEBUG = debug
    try:
        # Step1: read xml values
        values = get_config(xmlpath, Node)
        DEBUG(values)

        # Step2: Analyse xml values
        fsize, ftime = analyse_config(values)
        DEBUG("fsize value: {} MB".format(fsize))
        DEBUG("ftime value: {} D ".format(ftime))

    except Exception as e:
        print(e)
    finally:
        return (fsize, ftime)


def test():
    confPath = "./conf/fileConfig.xml"
    myNode = "rmConfig"
    get_config_value(confPath, myNode, debug=1)



if __name__ == "__main__":
    test()