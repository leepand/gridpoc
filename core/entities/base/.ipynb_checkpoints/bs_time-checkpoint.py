# -*- coding: UTF-8 -*-

# author: Leepand
# time: 2019-01-25
# desc: 时间处理类封装


from Arthur.core.entities.base.bs_log import Log
import datetime
import time


def get_cur_dtime():
    return int(time.time())


def get_cur_time(tmFormat=None):
    if tmFormat == None: tmFormat = "%Y-%m-%d %H:%M:%S"
    return (datetime.datetime.now()).strftime(tmFormat)

"""import datetime
now_time = datetime.datetime.now()
yes_time = now_time + datetime.timedelta(days=-1)
yes_time_nyr = yes_time.strftime("%Y-%m-%d %H:%M:%S")
yes_time_nyr
"""

def yg_tm_str_int(strTm, format="%Y-%m-%d %H:%M:%S"):
    if type(strTm) == datetime.datetime:
        strTm = strTm.strftime(format)
    tmTuple = time.strptime(strTm, format)
    return time.mktime(tmTuple)


def yg_tm_int_str(tm, format="%Y-%m-%d %H:%M:%S"):
    # tmObj = time.localtime(tm)
    tmObj = time.localtime(tm)
    return time.strftime(format, tmObj)


def get_cur_day(days=0, format="%Y%m%d"):
    return (datetime.datetime.now() - datetime.timedelta(days)).strftime(format)


def get_cur_time_2(days=0, format="%Y-%m-%d %H:%M:%S"):
    return (datetime.datetime.now() - datetime.timedelta(days)).strftime(format)




if __name__ == "__main__":
    def test1():
        print get_cur_time_2(1, "%Y-%m-%d 00:00:00")


    print get_cur_day(0,format="%Y-%m-%d")
