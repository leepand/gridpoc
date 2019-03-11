# -*- coding: UTF-8 -*-

# author: leepand
# time: 2019-01-30
# desc: service Tag list

from Arthur.core.entities.arthur_web_cfg import *
from Arthur.core.entities.base.bs_util import *
from Arthur.core.entities.base.bs_database_pid import DataBase
from Arthur.core.entities.base.bs_time import get_cur_day,get_cur_time
#2019-01-30 add
class ArthurServTagsDao:
    
    #用户的tag service list
    #update 2019-02-19:left Join user表，批量增加username信息
    @staticmethod
    def query_node_list_by_tag(status='normal', search=None):
        dataBase = DataBase()
        sql = "select * from tb_algo a left join tb_user b on a.uid=b.uid where 1=1 "
        param = []
        if status and status != 'all':
            sql += "and status = %s "
            param.append(status)
        if search:
            #search = "%%%s%%" % (search)           
            sql += "and locate(%s,tags)"#tags like %s or algoname like %s
            param.append(search)

        """sql += "order by aid desc limit %s, %s"
        param.append(offset)
        param.append(limit)"""

        param = tuple(param)
        bRet, sRet = dataBase.query_data(sql, param)
        if not bRet:
            return False, sRet

        return True, sRet

if __name__ == "__main__":

    #ArthurAlgoStarDao.insert_node(algouid, uid,algoname,star_status,thumb_status)
    ArthurServTagsDao.query_node_list_by_tag(search='机器')