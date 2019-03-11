# -*- coding: utf-8 -*-

# author: leepand
# time: 2019-01-15
# desc: AB Testing信息持久化

'''
# 用户操作
DROP TABLE IF EXISTS `tb_user_abtesting`;
CREATE TABLE `tb_user_abtesting` (
`abid` int(10) NOT NULL AUTO_INCREMENT,
`uid` int(10) NOT NULL,
`abname` varchar(50) NOT NULL,
PRIMARY KEY (`abid`),
KEY `uid` (`uid`),
CONSTRAINT `tb_abtesting_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `tb_user` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''
#update 2019-01-25
from Arthur.core.entities.arthur_web_cfg import *
from Arthur.core.entities.base.bs_util import *
from Arthur.core.entities.base.bs_database_pid import DataBase

class ArthurAbTestingDao:
    @staticmethod
    def insert_node(uId, abname):

        dataBase = DataBase()
        sql = "insert into tb_user_abtesting(uid, abname) values(%s, %s)"
        param = (uId, abname)

        bRet, sRet = dataBase.insert_data(sql, param)
        return bRet, sRet
    @staticmethod
    def delete_node_user_ab(abid):
        dataBase = DataBase()
        sql = "delete from tb_user_abtesting where abid = %s"
        param = (abid, )

        bRet, sRet = dataBase.delete_data(sql, param)
        if not bRet:
            return False, sRet
        
        return True, sRet
    @staticmethod
    def query_node_ab_list_by_uid(uid):
        dataBase = DataBase()
        sql = "select * from tb_user_abtesting where uid = %s"
        param = (uid, )

        bRet, sRet = dataBase.query_data(sql, param)
        if not bRet:
            return False, sRet

        return True, sRet
    
    @staticmethod
    def query_node_ab_list():
        dataBase = DataBase()
        sql = "select * from tb_user_abtesting"

        bRet, sRet = dataBase.query_data(sql, None)
        if not bRet:
            return False, sRet
        
        return True, sRet
    @staticmethod
    def query_node_by_abname(abName):
        dataBase = DataBase()
        sql = "select * from tb_user_abtesting where abname = %s"
        param = (abName, )

        bRet, sRet = dataBase.query_data(sql, param)
        if not bRet:
            return False, sRet
        if len(sRet)>0:
            return True, sRet[0]
        else:
            return True, {}
    

if __name__ == "__main__":
    uId=1
    abname='layerui2'
    ArthurAbTestingDao.insert_node(uId,abname)
    ArthurAbTestingDao.query_node_ab_list_by_uid(1)
    print ArthurAbTestingDao.query_node_by_abname('layui')