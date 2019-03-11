# -*- coding: utf-8 -*-
# author: leepand
# time: 2019-01-09
# desc: 点赞、收藏等信息持久化


'''
#点赞、收藏等信息持久化
DROP TABLE IF EXISTS `tb_algo_star_thumb`;
CREATE TABLE `tb_algo_star_thumb` (
`sid` int(10) NOT NULL AUTO_INCREMENT,
`algouid` int(10) NOT NULL,
`uid` int(10) NOT NULL,
`algoname` varchar(50) NOT NULL,
`star_cnt` int(30) DEFAULT 1,
`thumb_cnt` int(30) DEFAULT 1,
`star_status` enum('star','nostar') DEFAULT 'nostar',
`thumb_status` enum('thumb','nothumb') DEFAULT 'nothumb',
`insert_tm` datetime NOT NULL,
PRIMARY KEY (`sid`),
KEY `uid` (`uid`),
CONSTRAINT `tb_star_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `tb_user` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''
#update 2019-01-25

from Arthur.core.entities.arthur_web_cfg import *
from Arthur.core.entities.base.bs_util import *
from Arthur.core.entities.base.bs_database_pid import DataBase
from Arthur.core.entities.base.bs_time import get_cur_day,get_cur_time

class ArthurAlgoStarDao:

    @staticmethod
    def insert_node(algouid, uid,algoname,star_status,thumb_status):

        dataBase = DataBase()
        sql = "insert into tb_algo_star_thumb(algouid, uid,algoname,star_status,thumb_status,insert_tm) " \
              "values(%s, %s, %s, %s, %s, %s)"
        param = (algouid, uid,algoname,star_status,thumb_status, get_cur_time())

        bRet, sRet = dataBase.insert_data(sql, param)
        return bRet, sRet


    @staticmethod
    def update_node_status(algouid, uid,algoname,star_status,thumb_status):
        dataBase = DataBase()
        updatetime=get_cur_day(0, format="%Y-%m-%d %H:%M:%S")
        #_bRet,status_cnt_list = ArthurAlgoStarDao.query_status_cnt_by_algo(algouid,algoname)
        #star_cnt_old = status_cnt_list[0]['star_cnt_algo']
        #thumb_cnt_old = status_cnt_list[0]['thumb_cnt_algo']
        #每个使用者ID+算法开发者ID共同唯一表示一个starID，并只有1和0，前端展示的star数则是以algoID和algoname确定的记录和
        if thumb_status=='nothumb':
            #thumb_cnt_new=thumb_cnt_old-1
            thumb_cnt_new=0
        elif thumb_status=='thumb':
            #thumb_cnt_new=thumb_cnt_old+1
            thumb_cnt_new=1
        else:
            #thumb_cnt_new=thumb_cnt_old
            thumb_cnt_new=0

        if star_status=='nostar':
            #star_cnt_new=star_cnt_old-1
            star_cnt_new=0
        elif star_status=='star':
            #star_cnt_new=star_cnt_old+1
            star_cnt_new=1
        else:
            #star_cnt_new=star_cnt_old
            star_cnt_new=0
        sql = "update tb_algo_star_thumb set star_cnt = %s ,thumb_cnt = %s,star_status = %s, thumb_status = %s, insert_tm = %s" \
              " where algouid = %s and uid = %s and algoname = %s"
        param = (star_cnt_new,thumb_cnt_new,star_status,thumb_status,updatetime,algouid,uid,algoname)
        bRet, sRet = dataBase.update_data(sql, param)
        if not bRet:
            return False, sRet

        return True, sRet
    @staticmethod
    def query_status_cnt_by_algo(algouid,algoname):
        dataBase = DataBase()
        sql = "select sum(star_cnt) as star_cnt_algo,sum(thumb_cnt) as thumb_cnt_algo from tb_algo_star_thumb where algouid =%s and algoname =%s"
        param = [algouid,algoname]
        param = tuple(param)
        bRet, sRet = dataBase.query_data(sql, param)
        if not bRet:
            return False, sRet

        return True, sRet
    #搜索服务被哪些人点来赞（收藏/星星）从第offset+1开始读取limit条信息
    @staticmethod
    def query_star_list_by_algo(algouid,algoname,offset=1, limit=1000):
        dataBase = DataBase()
        sql = "select * from tb_algo_star_thumb where algouid =%s and algoname =%s and star_cnt>0 "
        param = [algouid,algoname]
        sql += "order by insert_tm desc limit %s, %s"
        param.append(offset)
        param.append(limit)

        param = tuple(param)
        bRet, sRet = dataBase.query_data(sql, param)
        if not bRet:
            return False, sRet

        return True, sRet

    @staticmethod
    def query_node_by_uid_algo_algouid(uid,algouid, algoname):
        dataBase = DataBase()
        sql = "select * from tb_algo_star_thumb where uid=%s and algouid = %s and algoname = %s"
        param = [uid,algouid, algoname]

        param = tuple(param)
        bRet, sRet = dataBase.query_data(sql, param)
        if not bRet:
            return False, sRet

        return True, sRet
    @staticmethod
    def query_algouid_by_uidstar(uid):
        dataBase = DataBase()
        star_status='star'
        sql = "select * from tb_algo_star_thumb where uid=%s and star_status = %s"
        param = [uid,star_status]

        param = tuple(param)
        bRet, sRet = dataBase.query_data(sql, param)
        if not bRet:
            return False, sRet

        return True, sRet

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
    #用户的服务list查询
    @staticmethod
    def query_node_list_by_uid(uId,offset, limit, status, search):
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
    algouid=1
    uid=2
    algoname='test_algo'
    star_status='star'
    thumb_status='nothumb'
    #ArthurAlgoStarDao.insert_node(algouid, uid,algoname,star_status,thumb_status)
    ArthurAlgoStarDao.query_node_by_aid(1)
    ArthurAlgoStarDao.query_node_count()
    #print HjsOrderDao.insert_node(cId, name, otype, order_tm, remark)
    #print HjsOrderDao.query_node_by_date2('normal', '2019-01-02')
    #ArthurAlgoDao.insert_node(uId, algoname,algodesc,token,pyfile,funcslist,tags,field,host,port,atype, algo_tm, is_email,remark)

#uId, algoname,algodesc,token,pyfile,funcslist,tags,field,host,port,atype, algo_tm, is_email,remark

#uId, algoname,algodesc,token,pyfile,funcslist,tags,host,port,atype, algo_tm, is_email,remark