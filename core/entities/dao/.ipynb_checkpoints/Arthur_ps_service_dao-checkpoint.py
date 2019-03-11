# -*- coding: utf-8 -*-

# author: leepand
# time: 2018-12-16
# desc: tb_service_dao


'''
# 暂取消服务表
CREATE TABLE `tb_ps_algo` (
`pid` int(11) NOT NULL AUTO_INCREMENT,
`aid` int(10) NOT NULL,
`uid` int(10) NOT NULL,
`algoname` varchar(50) NOT NULL,
`pause_tm` date NOT NULL,
`remark` text NOT NULL,
`insert_tm` datetime NOT NULL,
PRIMARY KEY (`pid`),
KEY `aid` (`aid`),
KEY `uid` (`uid`),
CONSTRAINT `tb_ps_algo_ibfk_1` FOREIGN KEY (`aid`) REFERENCES `tb_algo` (`aid`),
CONSTRAINT `tb_ps_algo_ibfk_2` FOREIGN KEY (`uid`) REFERENCES `tb_user` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''


#update 2019-01-25
from Arthur.core.entities.arthur_web_cfg import *
from Arthur.core.entities.base.bs_util import *
from Arthur.core.entities.base.bs_database_pid import DataBase
from Arthur.core.entities.base.bs_time import get_cur_time

class ArthurServicePauseDao:

    @staticmethod
    def insert_node(aid, uid, algoname, pause_tm, remark):

        dataBase = DataBase()
        sql = "insert into tb_ps_algo(aid, uid, algoname, pause_tm, remark, insert_tm) " \
              "values(%s, %s, %s, %s, %s, %s)"
        param = (aid, uid, algoname, pause_tm, remark, get_cur_time())

        bRet, sRet = dataBase.insert_data(sql, param)
        return bRet, sRet

    @staticmethod
    def query_node_list(offset, limit, status, search):
        dataBase = DataBase()
        sql = "select * from tb_algo where 1=1 "
        param = []
        if status and status != 'all':
            sql += "and status = %s "
            param.append(status)
        if search:
            search = "%%%s%%" % (search)
            sql += "and (uid like %s or algoname like %s)"
            param.append(search)
            param.append(search)

        sql += "order by aid desc limit %s, %s"
        param.append(offset)
        param.append(limit)

        param = tuple(param)
        bRet, sRet = dataBase.query_data(sql, param)
        if not bRet:
            return False, sRet

        return True, sRet


    @staticmethod
    def query_node_count(status=None, search=None):
        dataBase = DataBase()
        sql = "select count(*) as cnt from tb_algo where 1=1 "
        param = []

        if status and status != 'all':
            sql += "and status = %s"
            param.append(status)
        if search:
            search = "%%%s%%" % (search)
            sql += "and (uid like %s or algoname like %s)"
            param.append(search)
            param.append(search)

        param = tuple(param)
        bRet, sRet = dataBase.query_data(sql, param)
        if not bRet:
            return False, sRet
        if len(sRet) !=1:
            return True, 0

        return True, sRet[0]['cnt']


    @staticmethod
    def delete_node_by_pid(pId):
        dataBase = DataBase()
        sql = "delete from tb_ps_algo where pid = %s"
        param = (pId, )

        bRet, sRet = dataBase.delete_data(sql, param)
        if not bRet:
            return False, sRet
        
        return True, sRet


    @staticmethod
    def query_node_by_date(tg_date):
        dataBase = DataBase()
        sql = "select * from tb_ps_algo where pause_tm = %s"
        param = (tg_date, )

        bRet, sRet = dataBase.query_data(sql, param)
        if not bRet:
            return False, sRet
    
        return True, sRet



if __name__ == "__main__":
    #print HjsOrderDao.query_node_by_status('stop')

    #print HjsOrderDao.query_node_by_date(3)
    print ArthurServicePauseDao.delete_node_by_pid(3)




