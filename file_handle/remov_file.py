# -*- encoding: utf-8-*-
#================================================
#  __title__ = 'rmove_file'
#  __author__ = 'tx'
#  __mtime__ = '2017-12-08'
#=================================================
import io
import sys
import os
import time
sys.path.append("./pylib/")
from get_file_config import get_fileConfig, analyse_fileConfig
from file_tools import get_fileList, get_fileSize, rmfile
from time_tools import get_fileTime, TimeStampToTime, get_nowtime

reload(sys)
sys.setdefaultencoding('utf-8')


rm_SFlag = 1
rm_TFlag = 1

g_iDEBUG = 1
def DEBUG(*value):
    if g_iDEBUG == 1:
        t = time.strftime("%Y-%m-%d %H:%M:%S")
        filename = sys.argv[0][sys.argv[0].rfind(os.sep)+1:]
        print "[python][%s,%s]:" % (filename, t),
        for i in value:
            print i,
        print ""


def rmFOverTime(rmTime, fpath, tail='.dat'):
    '''
    test remove file overflow Time.
    '''
    # fpath = "/home/tx/Desktop/file_handle/test"
    print "set rmtime: ", rmTime

    fileList = get_fileList(fpath, tail)
    if not fileList or isinstance(fileList, list) is False:
        print "get no file"
        return None

    total_num = len(fileList)
    overTime_num = 0
    succesRm_num = 0

    ntime = get_nowtime()
    for file in fileList:
        ctime = get_fileTime(file, fAttr='C')
        print "file path: ", file
        print "file ctime: ", TimeStampToTime(ctime)

        if (float(ntime) - float(ctime))/(24*60*60) > rmTime:   # compare by day
        # if (float(ntime) - float(ctime))/(60*60) > rmTime:     # compare by hourse, just for test
            overTime_num += 1
            flag = rmfile(file, 1)
            if not flag:
                print "remove file[%s] failed!" % file
            succesRm_num += 1

    print "total file num: ", total_num
    print "overTime_num: ", overTime_num
    print "succesRm_num: ", succesRm_num
    return succesRm_num


def rmFOverSize(rmSize, fpath, tail='.dat'):
    '''
    test remove file overflow Size.
    '''
    print "set rmsize: ", rmSize

    fileList = get_fileList(fpath, tail)
    if not fileList or isinstance(fileList, list) is False:
        print "get no file"
        return None

    total_num = len(fileList)
    overSize_num = 0
    succesRm_num = 0

    for file in fileList:
        size = get_fileSize(file, unit='MB')
        print "file path: ", file
        print "file size: ", size

        if float(size) > float(rmSize):
            overSize_num += 1

            flag = rmfile(file, 1)
            if not flag:
                print "remove file[%s] failed!" % file
            succesRm_num += 1

    print "total file num: ", total_num
    print "overSize_num: ", overSize_num
    print "succesRm_num: ", succesRm_num
    return succesRm_num


def main():
    module = "RmFConfig"
    confPath= "../conf/fileConfig.xml"
    fConf = get_fileConfig(confPath, module)
    RmFSize, RmFTime = analyse_fileConfig(fConf)
    print "Config Setting [fszie: %.3f MB]" % RmFSize
    print "Config Setting [ftime: %.3f Day]" % RmFTime

    test_file = "./test_file"
    while True:
        if rm_SFlag:
            rmFOverSize(RmFSize, test_file, tail='.txt')

        print "~~"*20

        if rm_TFlag:
            rmFOverTime(RmFTime, test_file, tail='.txt')

        time.sleep(60)

if __name__ == "__main__":
    main()