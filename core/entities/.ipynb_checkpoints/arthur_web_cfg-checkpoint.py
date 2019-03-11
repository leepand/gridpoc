# -*- coding: UTF-8 -*-

# author: Leepand
# time: 2019-01-25
# desc: Arthur后台配置

import os
from Arthur.core.entities.base.bs_base_cfg import BaseConf

class EnvEnum:
    T_DEV       =   "dev"
    T_ONLINE    =   "online"
    
CUR_ENV         =   EnvEnum.T_DEV

if CUR_ENV ==  EnvEnum.T_DEV:
    
    BaseConf.IS_CTR_LOG     =   True
    BaseConf.LOG_LEVEL      =   1
    BaseConf.SQL_HOST       =   "127.0.0.1"
    BaseConf.SQL_PORT       =   3306
    BaseConf.SQL_USER       =   "root"
    BaseConf.SQL_PASSWD     =   ""
    BaseConf.SQL_DB         =   "Arthur_manage"
    

else:
    BaseConf.IS_CTR_LOG     =   False
    BaseConf.LOG_LEVEL      =   2
    BaseConf.SQL_HOST       =   "127.0.0.1"
    BaseConf.SQL_PORT       =   3306
    BaseConf.SQL_USER       =   "root"
    BaseConf.SQL_PASSWD     =   ""
    BaseConf.SQL_DB         =   "Arthur_manage"



# with local cfg, so do not modify the file when test in the local env.
#if os.path.exists(os.path.join(os.path.dirname(__file__), 'hjs_local_cfg.py')):
#    from hjs_local_cfg import *



