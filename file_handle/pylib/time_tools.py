# -*- encoding: utf-8-*-
'''
    @File    test  pylib.time_tools
    @Author
    @Created On 2017-12-08
    @Updated On 2018-04-13
'''
# py3 = True if sys.version > '3' else False

import os
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')

g_iDEBUG = 1
def DEBUG(*value):
    if g_iDEBUG == 1:
        t = time.strftime("%Y-%m-%d %H:%M:%S")
        # filename = sys.argv[0][sys.argv[0].rfind(os.sep)+1:]
        filename = os.path.splitext(os.path.basename(__file__))[0]
        print "[python2.7][%s,%s]:" % (filename, t),
        for i in value:
            print i,
        print ""


def TimeStampToTime(timebuf):
    '''把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12.'''
    if timebuf:
        if isinstance(timebuf, str) is True:
            timebuf = timebuf.strip()[:11]
            timestamp = int(timebuf)
        elif isinstance(timebuf, (int, float))is True:
            timestamp = timebuf
        else:
            return None
        timeStruct = time.localtime(int(timestamp))                 # step1: timestamp  to timeStruct
        return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)       # step2: timeStruct to format_time
    else:
        return None


def format_date(value):
    if not value:
        return None
    time_value = value.strip()
    try:
        #根据指定的格式把一个时间字符串解析为时间元组
        timeStruct = time.strptime(time_value, "%m %d, %Y")           # eg: "1 06, 2018"
        # timeStruct = time.strptime(time_value, "%m %d, %y")         # eg: "1 06, 18"
        # timeStruct = time.strptime(time_value, "%B %d, %Y")         # eg: "January 06, 2018"
        # print timeStruct
        timesf = time.strftime("%Y-%m-%d", timeStruct)
        return timesf
    except:
        timesf = time.strftime("%Y-%m-%d", time.localtime())
        return timesf


def get_nowtime(tStamp=1):
    '''tStamp is 1, return now time by timeStamp.'''
    if tStamp == 1:
        timeStamp = time.time()             #返回当前时间的时间戳
        return timeStamp
    else:
        time_local  = time.localtime()      #类似gmtime()，作用是格式化时间戳为本地的时间。 如果sec参数未输入，则以当前时间为转换标准
        YMD = time.strftime("%Y-%m-%d", time_local)
        return YMD

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


def tets_TimeStampToTime():
    nowtime = time.time()
    timep = TimeStampToTime(int(nowtime))
    DEBUG("TimeStamp : ", nowtime)
    DEBUG("PrettyTime: ", timep)


def test_format_date():
    timestr = "1 06, 2018"
    timep   = format_date(timestr)
    DEBUG("str    data: ", timestr)
    DEBUG("format date: ", timep)


def main():
    # test TimeStampToTime
    tets_TimeStampToTime()

    # test format_date
    test_format_date()


if __name__ == '__main__':
    main()