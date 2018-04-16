# -*- encoding: utf-8-*-
#  __title__ = 'rmove_file'
#  __author__ = 'tx'
#  __mtime__ = '2018-04-16'

import os
import sys
import time
sys.path.append("./pylib/")
from get_file_config import get_config_value
from file_tools import get_files, get_file_size, get_file_time
from time_tools import TimeStampToTime
reload(sys)
sys.setdefaultencoding('utf-8')


g_iDEBUG = 0
def DEBUG(*value):
    if g_iDEBUG == 1:
        t = time.strftime("%Y-%m-%d %H:%M:%S")
        filename = sys.argv[0][sys.argv[0].rfind(os.sep)+1:]
        print "[python][%s,%s]:" % (filename, t),
        for i in value:
            print i,
        print ""


class RemoveFile(object):
    def __init__(self, fpath, debug=0):
        self.fpath = fpath
        self.total_num  = 0
        self.osize_num  = 0
        self.otime_num  = 0
        self.size_faild = 0
        self.time_faild = 0

    def __del__(self, path='./', tail='.pyc'):
        files = get_files(path, tail)
        if not files:
            print("No file")
            return
        for file in files:
            print("File: {}".format(file))
            try:
                os.remove(file)
            except Exception as e:
                print(e)

    def rm_over_size(self, rmSize, tail='.txt'):
        files = get_files(self.fpath, tail)
        if not files or isinstance(files, list) is False:
            print("no file in the path: {}".format(self.fpath))
            return None

        self.total_num = len(files)
        for file in files:
            size = get_file_size(file, unit='MB')
            DEBUG("File: {}, Size: {}".format(file, size))

            if float(size) > float(rmSize):
                self.osize_num += 1
                try:
                    os.remove(file)
                except Exception as e:
                    self.size_faild += 1
                    print("Error: {} \nFile:{}\nRemove failed!".format(e, file))


    def rm_over_time(self, rmTime, tail='.txt'):
        files = get_files(self.fpath, tail)
        if not files or isinstance(files, list) is False:
            print("no file in the path: {}".format(self.fpath))
            return None

        self.total_num = len(files)
        ntime = time.time()
        for file in files:
            ctime = get_file_time(file, tattr='M')
            DEBUG("File: {}, ctime: {}".format(file, TimeStampToTime(ctime)))

            if (float(ntime) - float(ctime))/(24*60*60) > rmTime:   # compare by day
                self.otime_num += 1
                try:
                    os.remove(file)
                except Exception as e:
                    self.time_faild += 1
                    print("Error: {} \nFile:{}\nRemove failed!".format(e, file))


def main():
    confPath = "./conf/fileConfig.xml"
    myNode = "rmConfig"

    fsize, ftime = get_config_value(confPath, myNode, debug=0)
    print("fsize value: {} MB".format(fsize))
    print("ftime value: {} D ".format(ftime))
    print('\n')

    rm_SFlag = 1
    rm_TFlag = 1
    test_file = "./test/test_data/"
    rmObj = RemoveFile(test_file)
    # while True:
    if rm_SFlag:
        rmObj.rm_over_size(fsize, tail='.log')

        print("at present, total_num : ", rmObj.total_num)
        print("at present, osize_num : ", rmObj.osize_num)
        print("at present, size_faild: ", rmObj.size_faild)
    print("~~"*20)

    if rm_TFlag:
        rmObj.rm_over_time(ftime, tail='.log')
        print("at present, total_num : ", rmObj.total_num)
        print("at present, otime_num : ", rmObj.otime_num)
        print("at present, time_faild: ", rmObj.time_faild)
    print("handle over!\n")


if __name__ == "__main__":
    main()