# -*- coding: UTF-8 -*-

# author: s0nnet
# time: 2016-11-08
# desc: base conf


import os
import sys

'''
LOG_LEVEL
    DEBUG   =   1
    INFO    =   2
    WARINING =  3
    ERR     =   4
    ALERT   =   5
    CLOSE   =   10
'''
class BaseConf:

    LOG_LEVEL       =   2
    LOG_DIR         =   "../../log/"
    LOG_PREFIX      =   ""
    IS_CTR_LOG      =   True

    SQL_HOST        =   "127.0.0.1"
    SQL_PORT        =   3306
    SQL_USER        =   "root"
    SQL_PASSWD      =   ""
    SQL_DB          =   "Arthur_manage"
