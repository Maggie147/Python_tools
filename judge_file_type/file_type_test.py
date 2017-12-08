#!/usr/bin/python
#-*-coding:utf-8-*- 

import os
import struct

# 支持文件类型  
# 用16进制字符串的目的是可以知道文件头是多少字节  
# 各种文件头的长度不一样，少半2字符，长则8字符  
def typeList():  
    return {
        "FFD8FF" :  'EXT_JPEG',
        "89504E47": 'EXT_PNG',
        "47494638": 'EXT_GIF',
        "49492A00": 'EXT_TIF',
        "424D": 'EXT_BMP',
        "3C3F786D6C": 'EXT_XML',
        "68746D6C3E": 'EXT_HTML',
        "44656C69766572792D646174653A": 'EXT_EML',
        "255044462D312E": 'EXT_PDF',
        "52617221": 'EXT_RAR',  
        "504B0304": 'EXT_ZIP'}  
  
# 字节码转16进制字符串  
def bytes2hex(bytes):  
    num = len(bytes)  
    hexstr = u""  
    for i in range(num):  
        t = u"%x" % bytes[i]  
        if len(t) % 2:  
            hexstr += u"0"  
        hexstr += t  
    return hexstr.upper()  
  
# 获取文件类型  
def filetype(filename):  
    binfile = open(filename, 'rb') # 必需二制字读取  
    tl = typeList()  
    ftype = 'unknown'  
    for hcode in tl.keys():  
        numOfBytes = len(hcode) / 2 # 需要读多少字节  
        binfile.seek(0) # 每次读取都要回到文件头，不然会一直往后读取  
        try:
            hbytes = struct.unpack_from("B"*numOfBytes, binfile.read(numOfBytes)) # 一个 "B"表示一个字节
        except Exception as e:
            print e
            continue

        f_hcode = bytes2hex(hbytes)  
        if f_hcode == hcode:  
            ftype = tl[hcode]  
            break  
    binfile.close()  
    return ftype, filename

def getListFiles(path):
    assert os.path.isdir(path), '%s not exist.' % path
    ret = []
    file_path = []
    file_name = []

    for root ,dirs, files in os.walk(path):
        # print '%s, %s, %s' % (root, dirs, files)
        for filespath in files:
            ret.append(os.path.join(root,filespath))

            # file_path.append(root + '/' + filespath)
            file_name.append(filespath)
    return ret
    # return file_name


def test():
    FilePath = './files'
    # print filetype(FilePath)
    ret = getListFiles(FilePath)
    # print ret
    for i in ret:
        print filetype(i)
        
  
if __name__ == '__main__':
    # print filetype('./files/C-coding-rules-simple.pdf')
    test()
