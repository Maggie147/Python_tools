# -*- encoding: utf-8-*-
#================================================
#  __title__ = 'time_fun'
#  __author__ = 'tx'
#  __mtime__ = '2017-12-08'
#=================================================
import os
import sys
import time
import shutil

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

def TimeStampToTime(inTime):
    '''把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12.'''
    if inTime:
        if isinstance(inTime, str) is True:
            inTime = inTime.strip()[:11]
            timestamp = int(inTime)
        elif isinstance(inTime, (int, float))is True:
            timestamp = inTime
        else:
            return None
        timeStruct = time.localtime(int(timestamp))
        return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)
    else:
        return None

def get_nowtime(tStamp=1):
    '''tStamp is 1, return now time by timeStamp.'''
    if tStamp == 1:
        timeStamp = time.time()             #返回当前时间的时间戳
        return timeStamp
    else:
        time_local  = time.localtime()      #类似gmtime()，作用是格式化时间戳为本地的时间。 如果sec参数未输入，则以当前时间为转换标准
        YMD = time.strftime("%Y-%m-%d", time_local)
        return YMD

def format_date(value):
    if not value:
        return None
    time_value = value.strip()
    try:
        # timesp = time.strptime(time_value, "%m/%d/%y")
        # timesp = time.strptime(time_value, "%B %d, %Y")     #根据指定的格式把一个时间字符串解析为时间元组
        timesp = time.strptime(time_value, "%B %d, %Y")
        print timesp
        timesf = time.strftime("%Y-%m-%d", timesp)
        print timesf
        return timesf
    except:
        timesf = time.strftime("%Y-%m-%d", time.localtime())
        return timesf

def get_fileTime(fpath, fAttr='C', tStamp=1):
    '''
get file time, param 'about' is 'C', return file create time;
param 'about' is 'M', return file modify time;
param 'about' is 'A', return file access time;
if tStamp is 1, return timeStamp; else return formatDate.
    '''
    try:
        # fpath = unicode(fpath,'utf8')
        fAttr = fAttr.upper()
        if fAttr == 'C':
            t = os.path.getctime(fpath)
        elif fAttr == 'M':
            t = os.path.getmtime(fpath)
        elif fAttr == 'A':
            t = os.path.getatime(fpath)
        else:
            print "please input file time of fAttr: c, m , a"
            return None
        if int(tStamp) == 1:
            return t
        else:
            return TimeStampToTime(t)
    except Exception as e:
        print e
        return None

def test_get_fileCMAtime(fpath):
    fileCTime = get_fileTime(fpath, fAttr='C')
    fileMTime = get_fileTime(fpath, fAttr='M')
    fileATime = get_fileTime(fpath, fAttr='A')
    print "fileCTime: ", fileCTime, TimeStampToTime(fileCTime)
    print "fileMTime: ", fileMTime, TimeStampToTime(fileMTime)
    print "fileATime: ", fileATime, TimeStampToTime(fileATime)

def test():
    fpath = "../test_file/2222test.txt"
    test_get_fileCMAtime(fpath)

if __name__ == '__main__':
    test()