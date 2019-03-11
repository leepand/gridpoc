# -*- coding: utf-8 -*-

# author: leepand
# time: 2018-12-21
# desc: tb_comments_dao

'''
# 用户操作
DROP TABLE IF EXISTS `tb_user`;
CREATE TABLE `tb_user` (
`uid` int(10) NOT NULL AUTO_INCREMENT,
`username` varchar(50) NOT NULL,
`nickname` varchar(50) NOT NULL,
`password` varchar(50) NOT NULL,
`phone` varchar(50) DEFAULT NULL,
`email` varchar(50) DEFAULT NULL,
`privilege` int(1) NOT NULL DEFAULT '1',
`remark` text,
`lastlogin` datetime DEFAULT NULL,
PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''

#update 2019-01-25
from Arthur.core.entities.arthur_web_cfg import *
from Arthur.core.entities.base.bs_util import *
from Arthur.core.entities.base.bs_database_pid import DataBase
from Arthur.core.entities.base.bs_time import get_cur_time

class HjsUserDao:
    
    @staticmethod
    def query_node_by_username(userName):
        dataBase = DataBase()
        sql = "select * from tb_user where username = %s"
        param = (userName, )

        bRet, sRet = dataBase.query_data(sql, param)
        if not bRet:
            return False, sRet
        
        return True, sRet[0]


    @staticmethod
    def query_node_by_uid(uid):
        dataBase = DataBase()
        sql = "select * from tb_user where uid = %s"
        param = (uid, )

        bRet, sRet = dataBase.query_data(sql, param)
        if not bRet:
            return False, sRet
        
        return True, sRet[0]

    
    @staticmethod
    def query_node_user_list():
        dataBase = DataBase()
        sql = "select * from tb_user"

        bRet, sRet = dataBase.query_data(sql, None)
        if not bRet:
            return False, sRet
        
        return True, sRet
    @staticmethod
    def query_user_count():
        dataBase = DataBase()
        sql = "select count(*) as cnt from tb_user where 1=1 "
        param = []

        param = tuple(param)
        bRet, sRet = dataBase.query_data(sql, param)
        if not bRet:
            return False, sRet
        if len(sRet) !=1:
            return True, 0

        return True, sRet[0]['cnt']

    @staticmethod
    def insert_node_user(nickName, userName, passWord, Phone, Email, Priv,Remark):
        dataBase = DataBase()
        sql = "insert into tb_user(nickname, username, password, phone, email, privilege, remark,lastlogin) values(%s, %s, %s, %s, %s, %s, %s, %s)"
        param = (nickName, userName, passWord, Phone, Email, Priv, Remark,get_cur_time())

        bRet, sRet = dataBase.insert_data(sql, param)
        if not bRet:
            return False, sRet
        
        return True, sRet


    @staticmethod
    def update_node_user(uId, nickName, userName, passWord, Phone, Email, Priv):
        dataBase = DataBase()
        sql = "update tb_user set nickname = %s, username = %s, password = %s, phone = %s, email = %s, privilege= %s where uid = %s"
        param = (nickName, userName, passWord, Phone, Email, Priv, uId)

        bRet, sRet = dataBase.update_data(sql, param)
        if not bRet:
            return False, sRet
        
        return True, sRet
    @staticmethod
    def query_node_msg_user_list(uId,profile_picture_url):
        dataBase = DataBase()
        sql = "select * from tb_user"

        bRet, sRet = dataBase.query_data(sql, None)
        if not bRet:
            return False, sRet
        msg_user_list=[]
        for usr in sRet:#HjsUser.user_info(35)
            usr_info={}
            if int(usr['uid'])==int(uId):
                fullname="Current User"
            else:
                fullname= usr['username']
            email= usr['email']
            usr_info['id']=int(usr['uid'])
            usr_info['fullname']=fullname
            usr_info['email']=email
            usr_info['profile_picture_url']=profile_picture_url
            msg_user_list.append(usr_info)
        return True,msg_user_list
    @staticmethod
    def delete_node_user(uId):
        dataBase = DataBase()
        sql = "delete from tb_user where uid = %s"
        param = (uId, )

        bRet, sRet = dataBase.delete_data(sql, param)
        if not bRet:
            return False, sRet
        
        return True, sRet

    @staticmethod
    def update_lastlogin(uId):
        dataBase = DataBase()
        sql = "update tb_user set lastlogin = %s where uid = %s"
        param = (get_cur_time(), uId)
        
        return dataBase.update_data(sql, param)





if __name__ == "__main__":
    #print HjsUserDao.query_node_by_username('admin')
    print HjsUserDao.query_node_user_list()

    pass
