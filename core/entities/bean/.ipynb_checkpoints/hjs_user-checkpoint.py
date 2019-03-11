# -*- coding: UTF-8 -*-

# author: leepand
# time: 2018-12-16
# desc: user处理逻辑



#update 2019-01-25
from web.utils import storage
from Arthur.core.entities.arthur_web_cfg import *
from Arthur.core.entities.base.bs_util import *
from Arthur.core.entities.dao.hjs_user_dao import *


class UserPriv:
    VIEW = 1
    USER = 2
    ADMIN = 3


class HjsUser:
    
    @staticmethod
    def user_list(userName):
        bRet, sRet = HjsUserDao.query_node_user_list()
        if not bRet:
            return False, sRet
        userList = list()
        for item in sRet:
            user_info = storage()
            user_info.uid = int(item['uid'])
            user_info.username = item['username']
            user_info.nickname = item['nickname']
            user_info.password = item['password']
            user_info.phone = item['phone']
            user_info.email = item['email']
            user_info.priv = int(item['privilege'])
            user_info.lastlogin = str(item['lastlogin'])
            userList.append(user_info)

        return True, userList


    @staticmethod
    def user_add(nickName, userName, passWord, Phone, Email, Priv,Remark):
        bRet, sRet = HjsUserDao.insert_node_user(nickName, userName, passWord, Phone, Email, Priv,Remark)
        if not bRet:
            return False, sRet
        
        return True, sRet

    #效率低
    @staticmethod
    def user_info(uId):
        bRet, uInfo = HjsUserDao.query_node_by_uid(uId)

        if not bRet:
            return False, uInfo
        
        user_info = storage()
        user_info.uid = uInfo['uid']
        user_info.username = uInfo['username']
        user_info.nickname = uInfo['nickname']
        user_info.password = uInfo['password']
        user_info.phone = uInfo['phone']
        user_info.email = uInfo['email'];
        user_info.priv = uInfo['privilege']
        user_info.remark = uInfo['remark']
        return True, user_info


    @staticmethod
    def user_update(uId, nickName, userName, passWord, Phone, Email, Priv):
        bRet, sRet = HjsUserDao.update_node_user(uId, nickName, userName, passWord, Phone, Email, Priv)
        if not bRet:
            return False, sRet
        
        return True, sRet


    @staticmethod
    def user_del(uId):
        bRet, sRet = HjsUserDao.delete_node_user(uId)
        if not bRet:
            return False, sRet
        
        return True, sRet


    @staticmethod
    def get_user_uid(userName):
        bRet, sRet = HjsUserDao.query_node_by_username(userName)
        if not bRet:
            return False, sRet
        uid = int(sRet['uid'])
        
        return True, uid


    @staticmethod
    def is_admin(userName):
        bRet, sRet = HjsUserDao.query_node_by_username(userName)
        if not bRet:
            return False, sRet
        if not sRet['privilege']:
            return False, 'get user priv error'
        if sRet['privilege'] != UserPriv.ADMIN: # is_admin user
            return True, False
        
        return True, True

    @staticmethod
    def is_zuanshi(userName):
        bRet, sRet = HjsUserDao.query_node_by_username(userName)
        if not bRet:
            return False, sRet
        if not sRet['privilege']:
            return False, 'get user priv error'
        if sRet['privilege'] != UserPriv.ADMIN: # is_admin user
            if sRet['privilege'] != UserPriv.USER:#某些操作钻石也可以，比如添加服务
                return True, False
        
        return True, True






if __name__ == "__main__":
    #print HjsUser.user_list('admin')


    print HjsUser.user_info(105)


