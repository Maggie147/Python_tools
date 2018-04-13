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
from pylib.time_tools import *

reload(sys)
sys.setdefaultencoding('utf8')

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
    start_time = time.time()

    # test TimeStampToTime
    tets_TimeStampToTime()


    # test format_date
    test_format_date()

    end_time = time.time()
    DEBUG("Test last time: ", (end_time-start_time))


if __name__ == "__main__":
    main()