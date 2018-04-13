# -*- encoding: utf-8-*-
'''
    @File    test  pylib.file_tools
    @Author
    @Created On 2018-04-13
    @Updated On 2018-04-13
'''
# py3 = True if sys.version > '3' else False

import os
import sys
import time
from bson.objectid import ObjectId
pwd = os.path.dirname(os.path.realpath(__file__))       #pwd2 = sys.path[0]
pardir = os.path.abspath(os.path.join(pwd, os.pardir))
sys.path.append(pardir)
from pylib.file_tools import *

reload(sys)
sys.setdefaultencoding('utf8')

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

class FiletoolsTest(object):
    def __init__(self, path, debug=1):
        global g_iDEBUG
        g_iDEBUG = debug

        filerealpath = os.path.realpath(__file__)
        filepath     = os.path.dirname(filerealpath)
        self.path    = os.path.abspath(os.path.join(filepath, path))


    def test_get_files(self, tail=None):
        files = get_files(self.path, tail)
        if not isinstance(files, list):
            DEBUG("Path[{}] Not Exsit!".format(self.path))
        try:
            for item in files:
                DEBUG("file: ", item)
        except Exception as e:
            DEBUG("test_get_files failed!!!")
        finally:
            DEBUG("test_get_files end.\n")


    def test_rmfile(self, fname):
        counter = 5
        while isExsit(self.path, fname):
            counter -= 1
            if counter < 0:
                break
            ret = rmfile(self.path, fname)
            if not ret:
                DEBUG("File: [{}] rm  failed! ".format(os.path.join(self.path, fname)))
                continue
        DEBUG("test_rmfile end.\n")


    def test_cpfile(self, srcfpath, tarfpath):
        # srcfpath1 = os.path.abspath(os.path.join(__file__, srcfpath))
        ret = cpfile(srcfpath, tarfpath)
        if not ret:
            DEBUG("File: [{}] cp to [] failed! ".format(srcfpath, tarfpath))
        DEBUG("test_cpfile end.\n")


    # test: get_file_data, get_file_md5, write_date_2file
    def test_some_fun(self, fname, mode='rb'):
        try:
            buf = get_file_data(self.path, fname, mode)
            if not buf:
                DEBUG("get_file_data failed! File: [{}] ".format(os.path.join(self.path, fname)))

            md5 = get_file_md5(self.path, fname)
            if not md5:
                DEBUG("test get_file_md5 failed!!")
            else:
                DEBUG("md5: {}  \tfile[{}] ".format(md5, os.path.join(self.path, fname)))

            ret = write_date_2file(self.path, fname+"_bak", buf)
            if not ret:
                DEBUG("test write_date_2file failed!!")
        except Exception as e:
            DEBUG(e)
        finally:
            DEBUG("test_some_fun ['get_file_data', 'get_file_md5', 'write_date_2file'] end.\n")


    def test_get_file_size(self, fname, unit='B'):
        fsize = get_file_size(self.path, fname, unit)
        if not fsize:
            DEBUG("test get_file_size failed!!")
        DEBUG("fsize: {} Bit.".format(fsize))
        DEBUG("test_get_file_size end.\n")


    def test_get_file_time(self, fname, tattr='C'):
        ftime = get_file_time(self.path, fname, tattr)
        if not ftime:
            DEBUG("test get_file_time failed!!")
        try:
            timeStruct = time.localtime(ftime)
            timeformat = time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)

            DEBUG("ftime[{}]: {}".format(tattr, timeformat))
        except Exception as e:
            DEBUG(e)
        finally:
            DEBUG("test get_file_time end.\n")


def main():
    start_time = time.time()

    test_path = './test_data/'
    test_file = '2222test.txt'

    testObj = FiletoolsTest(test_path, debug=1)

    testObj.test_get_files()

    testObj.test_cpfile(srcfpath='../pylib/file_tools.py', tarfpath='./test_data/')

    # get_file_data, get_file_md5, write_date_2file
    testObj.test_some_fun(fname="2222test.txt")

    testObj.test_get_file_size(fname="2222test.txt", unit='B')

    testObj.test_get_file_time(fname="2222test.txt", tattr='C')

    testObj.test_rmfile(fname="file_tools.py")
    testObj.test_rmfile(fname="2222test.txt_bak")

    end_time = time.time()
    DEBUG("Test last time: ", (end_time-start_time))


if __name__ == "__main__":
    main()