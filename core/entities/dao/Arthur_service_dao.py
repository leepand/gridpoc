# -*- coding: utf-8 -*-
# author: leepand
# time: 2018-12-17
# desc: tb_algo_dao


'''
#算法管理表
DROP TABLE IF EXISTS `tb_algo`;
CREATE TABLE `tb_algo` (
`aid` int(10) NOT NULL AUTO_INCREMENT,
`uid` int(10) NOT NULL,
`algoname` varchar(50) NOT NULL,
`algodesc` varchar(50) NOT NULL,
`version` varchar(50) NOT NULL  DEFAULT 'v1.0.0',
`opertype` enum('publish','register')  DEFAULT 'publish',
`token` varchar(50) NOT NULL,
`pyfile` varchar(50) NOT NULL,
`funcslist` text NOT NULL,
`tags` text NOT NULL,
`field` int(10) NOT NULL,
`host` varchar(50) NOT NULL  DEFAULT '0.0.0.0',
`port` int(10) NOT NULL,
`atype` varchar(10) NOT NULL DEFAULT 'REST',
`algo_tm` datetime NOT NULL,
`status` enum('normal','stop','notpublish') DEFAULT 'notpublish',
`is_email` varchar(10) NOT NULL DEFAULT 'no',
`remark` text NOT NULL,
`insert_tm` datetime NOT NULL,
PRIMARY KEY (`aid`),
KEY `uid` (`uid`),
CONSTRAINT `tb_algo_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `tb_user` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''


#update 2019-01-25
from Arthur.core.entities.arthur_web_cfg import *
from Arthur.core.entities.base.bs_util import *
from Arthur.core.entities.base.bs_database_pid import DataBase
from Arthur.core.entities.base.bs_time import get_cur_day,get_cur_time

class ArthurAlgoDao:

    @staticmethod
    def insert_node(uId, algoname,algodesc,opertype,token,pyfile,funcslist,tags,field,host,port,atype, algo_tm, is_email,remark):

        dataBase = DataBase()
        sql = "insert into tb_algo(uid, algoname, algodesc,opertype,token,pyfile,funcslist,tags,field,host,port,atype, algo_tm, is_email,remark, insert_tm) " \
              "values(%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s,%s,%s)"
        param = (uId, algoname,algodesc,opertype,token,pyfile,funcslist,tags,field,host,port,atype, algo_tm,is_email, remark, get_cur_time())

        bRet, sRet = dataBase.insert_data(sql, param)
        return bRet, sRet


    @staticmethod
    def update_node(aId, atype, algo_tm,status, remark):

        dataBase = DataBase()
        sql = "update tb_algo set atype=%s, algo_tm=%s, " \
              "status = %s, remark=%s where aid= %s"
        param = (aotype, algo_tm, status, remark, aId)

        bRet, sRet = dataBase.update_data(sql, param)
        return bRet, sRet


    @staticmethod
    def update_node_status(aId, status):
        dataBase = DataBase()
        updatetime=get_cur_day(0, format="%Y-%m-%d %H:%M:%S")
        #sql = "update tb_order set status = %s where oid = %s"
        #param = (status, oId)
        sql = "update tb_algo set status = %s,insert_tm = %s where aid = %s"
        param = (status,updatetime,aId)
        bRet, sRet = dataBase.update_data(sql, param)
        if not bRet:
            return False, sRet

        return True, sRet


    @staticmethod
    def query_node_list2(offset, limit, status, search):
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
    #update 2019-02-19之前的效率太慢, 主要因为后面需要每个uid都要去查user表，修改成直接关联即可
    @staticmethod
    def query_node_list(status):
        dataBase = DataBase()
        sql = "select * from tb_algo a left join tb_user b on a.uid=b.uid where 1=1 "
        param = []
        if status and status != 'all':
            sql += "and status = %s "
            param.append(status)
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
    #用户的服务list查询
    @staticmethod
    def query_node_list_by_uid2(uId,offset, limit, status, search):
        dataBase = DataBase()
        sql = "select * from tb_algo where uid=%s "
        param = [uId]
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
    #用户的服务list查询 update 2019-02-19/原查询效率太低
    @staticmethod
    def query_node_list_by_uid(uId,status='all'):
        dataBase = DataBase()
        sql = "select * from tb_algo a left join tb_user b on a.uid=b.uid where a.uid=%s "
        param = [uId]
        if status and status != 'all':
            sql += "and status = %s "
            param.append(status)
        param = tuple(param)
        bRet, sRet = dataBase.query_data(sql, param)
        if not bRet:
            return False, sRet

        return True, sRet
    

    #用户的服务list查询
    @staticmethod
    def query_node_count_by_uid(uId,status=None, search=None):
        dataBase = DataBase()
        sql = "select count(*) as cnt from tb_algo where uid=%s "
        param = [uId]

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
    #aid的服务list查询,服务于发布
    @staticmethod
    def query_node_by_aid(aId):
        dataBase = DataBase()
        sql = "select * from tb_algo where aid = %s"
        param = (aId, )

        bRet, sRet = dataBase.query_data(sql, param)
        if (not bRet) or (len(sRet) != 1):
            return False, sRet
        
        return True, sRet[0]
    #aid的服务info查询,服务于服务详情页
    @staticmethod
    def query_node_by_proj_uid(uId,AlgoName):
        dataBase = DataBase()
        sql = "select * from tb_algo where uid = %s and algoname = %s"
        param = (uId, AlgoName)

        bRet, sRet = dataBase.query_data(sql, param)
        if (not bRet) or (len(sRet) != 1):
            return False, sRet
        
        return True, sRet[0]
    #aid的服务info查询,服务于rest api proxy loadbalancer
    @staticmethod
    def query_node_by_proj(AlgoName):
        dataBase = DataBase()
        sql = "select * from tb_algo where algoname = %s"
        param = (AlgoName,)

        bRet, sRet = dataBase.query_data(sql, param)
        if (not bRet) or (len(sRet) != 1):
            return False, sRet
        
        return True, sRet[0]
    @staticmethod
    def query_node_by_status(status):
        dataBase = DataBase()
        sql = "select count(*) as cnt from tb_order where 1=1 "
        param = []

        if status == 'all':
            pass
        else:
            sql += 'and status = %s'
            param.append(status)
        
        param = tuple(param)
        bRet, sRet = dataBase.query_data(sql, param)
        if not bRet:
            return False, sRet
        if len(sRet) != 1:
            return True, 0
        
        return True, sRet[0]['cnt']

        
    @staticmethod
    def query_node_by_days(days):
        dataBase = DataBase()
        sql = "select oid, cid, name, date_format(order_tm, '%%Y-%%m-%%d') as end_tm from tb_order " \
              "where order_tm >= curdate() and order_tm < curdate() + %s"
        param = (days, )

        bRet, sRet = dataBase.query_data(sql, param)
        if not bRet:
            return False, sRet
        
        return True, sRet

    
    @staticmethod
    def query_node_by_date(status, tg_date):
        dataBase = DataBase()
        #sql = "select * from tb_algo where status = %s and algo_tm <= %s and algo_tm >= %s"
        sql = "select * from tb_algo where status = %s and insert_tm <= %s and insert_tm >= %s"
        sql_stop = "select * from tb_algo where status = %s and insert_tm <= %s and insert_tm >= %s"
        param = (status,tg_date,get_cur_day(0, format="%Y-%m-%d"))
        if status=='normal':
            bRet, sRet = dataBase.query_data(sql, param)
        else:
            bRet, sRet = dataBase.query_data(sql_stop, param)
        if not bRet:
            return False, sRet

        return True, sRet

    @staticmethod
    def query_node_cnt_by_date(status, tg_date):
        dataBase = DataBase()
        sql = "select count(*) as cnt from tb_algo where status = %s and algo_tm <= %s and algo_tm >= %s"
        sql_stop = "select count(*) as cnt from tb_algo where status = %s and insert_tm <= %s and insert_tm >= %s"
        param = (status, tg_date,get_cur_day(0, format="%Y-%m-%d"))

        if status=='normal':
            bRet, sRet = dataBase.query_data(sql, param)
        elif status=='stop':
            bRet, sRet = dataBase.query_data(sql_stop, param)
        else:
            bRet, sRet = dataBase.query_data(sql, param)
        if not bRet:
            return False, sRet
        if len(sRet) != 1:
            return True, 0
        
        return True, sRet[0]['cnt']

if __name__ == "__main__":
    #print HjsOrderDao.query_node_by_status('stop')
    import datetime
    today = datetime.date.today()
    date_t=today.isoformat()
    uId=41
    algoname='leepand'
    pyfile='./predict.py'
    funcslist='predict,pre2'
    algodesc='text mining'
    tags='nlp'
    token='sdksadfksdf'
    field=41
    atype='recom'
    host='0.0.0.0'
    is_email='no'
    port=9000
    algo_tm= "2018-03-12 12:23:11"
    #order_tm=date_t
    
    remark='just test'
    ArthurAlgoDao.update_node_status(1,'normal')
    #print HjsOrderDao.insert_node(cId, name, otype, order_tm, remark)
    #print HjsOrderDao.query_node_by_date2('normal', '2019-01-02')
    #ArthurAlgoDao.insert_node(uId, algoname,algodesc,token,pyfile,funcslist,tags,field,host,port,atype, algo_tm, is_email,remark)

#uId, algoname,algodesc,token,pyfile,funcslist,tags,field,host,port,atype, algo_tm, is_email,remark

#uId, algoname,algodesc,token,pyfile,funcslist,tags,host,port,atype, algo_tm, is_email,remark