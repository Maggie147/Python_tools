# -*- encoding: utf-8-*-
#================================================
#  __title__ = 'file_fun'
#  __author__ = 'tx'
#  __mtime__ = '2017-12-08'
#=================================================
import os
import sys
import time
import hashlib
import shutil
sys.path.append("./")
from time_tools import TimeStampToTime

reload(sys)
sys.setdefaultencoding('utf-8')

g_iDEBUG = 1
def DEBUG(*value):
    if g_iDEBUG == 1:
        t = time.strftime("%Y-%m-%d %H:%M:%S")
        filename = sys.argv[0][sys.argv[0].rfind(os.sep)+1:]
        print "[python][%s,%s]:" % (filename, t),
        for i in value:
            print i,
        print ""

def get_file_md5(fpath):
    '''以文件路径作为参数，返回对文件md5后的值
    '''
    try:
        # 需要使用二进制格式读取文件内容
        fp = open(fpath, 'rb')
        data = fp.read()
        fp.close()
    except:
        return None
    hashObj = hashlib.md5()
    hashObj.update(data)
    return hashObj.hexdigest()


def cpfile(srcfpath, tarfpath):
    try:
        shutil.copy(srcfpath, tarfpath)
        return True
    except:
        return False


def rmfile(fpath, flag=1):
    if flag:
        try:
            if fpath != "NULL":
                os.remove(fpath)
        except:
            return False
        return True
    else:
        return False


def get_fileList(file_dir, tail='.txt'):
    file_path=[]
    # file_name=[]
    fpath = file_dir.strip()
    ftail = tail.strip()

    if not os.path.exists(fpath):
        return None
    for value1, value2, value3 in os.walk(fpath):
        # print "value1: ", value1
        # print "value2: ", value2
        # print "value3: ", value3
        if len(value3)==0:
            continue
        for filename in value3:
            if ftail != os.path.splitext(filename)[1]:
                continue
            # file_path.append(value1)
            # file_name.append(i)
            file_path.append(value1+'/'+filename)
    # return file_path, file_name
    return file_path


def write_date_2file(path, fname, data,):
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        with open(path+fname, "wb") as f:
            fp.write(data)
    except:
        return False
    return True


def get_fileSize(fpath, unit='KB'):
    '''
get file szie, return default szie unit is KB, rounded to 3 decimal places.
    '''
    try:
        # fpath = unicode(fpath, 'utf8')
        unit = unit.upper()
        fsize = os.path.getsize(fpath)      # get file size, unit is B
        if unit == 'B':
            return fsize
        elif unit == 'KB':
            fsize = fsize/float(1024)
        elif unit == 'MB':
            fsize = fsize/float(1024*1024)
        elif unit == 'G':
            fsize = fsize/float(1024*1024*1024)
        else:
            print "please input Correct [unit of measure]!!!!!!!"
            return None
        return round(fsize, 3)
    except Exception as e:
        print e
        return None

def test_get_fileSize(fpath):
    fileSize = get_fileSize(fpath, unit='kB')
    if fileSize:
        print "fileSize:  %.3f KB"%fileSize


def test():
    fpath = "../test_file/2222test.txt"
    test_get_fileSize(fpath)

    fileList = get_fileList("../test_file", '.txt')
    for file in fileList:
        print "file path: ", file


if __name__ == '__main__':
    test()