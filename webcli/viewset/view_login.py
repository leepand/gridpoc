# -*- coding: UTF-8 -*-

# author: s0nnet
# time: 2016-11-08
# desc: login view


import web
from view_base import ViewBase,render,render_without_base,Session
from Arthur.core.entities.base.bs_log import Log
from Arthur.core.entities.dao.hjs_user_dao import HjsUserDao
from Arthur.core.entities.bean.hjs_user import HjsUser
from Arthur.core.entities.base.bs_time import get_cur_day,get_cur_time

from Arthur.core.entities.bean.Arthur_service import ArthurService
import json
import datetime
 
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)
class UserPriv:
    VIEW = 1
    USER = 2
    ADMIN = 3

class ViewLogin(ViewBase):
    def __init__(self):
        self._rDict = {
            "username": {'n': 'userName', 't': str, 'v': None},
            "password": {'n': 'passWord', 't': str, 'v': None}
        }

    def _check_param(self):

        if not self.userName: return False, "param(username) is None!"
        if not self.passWord: return False, "param(password) is NOne!"

        return True, None

    def GET(self):
        #该部分不需要公共模版，所以采用去掉base部分的
        return render_without_base.login()

    def _deal_login(self):

        bRet, sRet = HjsUserDao.query_node_by_username(self.userName)
        if not bRet:  return False, "username does not exist!"
        
        if sRet['password'] != self.passWord:
        #if record['passwd'] != comput_md5_text(salt + self.passWord):
            return False, u"用户名或密码错误"
        print 'usename',self.userName
        Session.set_val("username", self.userName)
        web.setcookie("username", self.userName)
        HjsUserDao.update_lastlogin(sRet['uid'])
        bRet, sRet = HjsUserDao.query_node_by_username(self.userName)
        if not bRet:
            return False, sRet
        if not sRet['privilege']:
            return False, 'get user priv error'
        if sRet['privilege'] != UserPriv.ADMIN: # is_admin user
            userpriv='普通用户'
        else:
            userpriv='超级管理员'
        
        Session.set_val("userpriv", userpriv)
        web.setcookie("userpriv", userpriv)        
        return True, sRet

    def POST(self):

        bRet, sRet = self.process(self._deal_login)
        if not bRet:
            Log.err("deal_login: %s" % (str(sRet)))
            return self.make_error(sRet)
                 
        return self.make_response(ViewBase.RetMsg.MSG_SUCCESS)#render.index(exp_list)#json.loads(json.dumps(sRet,cls=CJsonEncoder))
    

class ViewApiMeInfo(ViewBase):
    def __init__(self):
        self._rDict = {
            "page": {'n': "page", 't': int, 'v': 1},
            "length": {'n': "length", 't': int, 'v': 20},
            "status": {'n': "status", 't': str, 'v': 'all'},
            "search": {'n': "search", 't': str, 'v': ''}
        }
    
    def _check_param(self):
        bRet, sRet = super(ViewApiMeInfo, self)._check_param()
        if not bRet:
            return False, sRet
        return True, None

    def _deal_userinfo_get(self):
        bRet, sRet = HjsUserDao.query_node_by_username(self.get_user_name())
        if not bRet:
            return False, sRet
        
        return True,sRet

    # get old info
    def GET(self):
        bRet, sRet = self.check_login()
        if not bRet:
            return web.seeother("/login")
        bRet, userInfo = self.process(self._deal_userinfo_get)
        print 'sRetsRet',userInfo
        if not bRet:
            Log.err("deal_userinfo_get: %s" % (str(userInfo)))
            return self.make_error(userInfo)

        return self.make_response(json.loads(json.dumps(userInfo,cls=CJsonEncoder)))

    # do change/update user info TODO
    def POST(self):
        bRet, sRet = self.check_login()
        if not bRet:
            return web.seeother("/login")
        bRet, orderList = self.process(self._deal_order_list)
        if not bRet:
            Log.err("deal_search_order_list: %s" % (str(orderList)))
            return self.make_error(orderList)

        return self.make_response(orderList)

class ViewLogout(ViewBase):
    def GET(self):
        Session.set_val("username", None)
        web.setcookie("username", None)
        return web.seeother("/login")

    def POST(self):
        return self.GET()
class ViewIProfile2(ViewBase):
    def GET(self):
        bRet, sRet = self.check_login()
        if not bRet:
            Log.err("user not login!")
            return web.seeother("/login")
       
        return render.profile()
    
class ViewIProfile(ViewBase):
    def _deal_service_list(self):
        _bRet,uId=HjsUser.get_user_uid(self.get_user_name())
        if not _bRet:
            return False, uId
        return ArthurService.service_user_list(uId,page=1,length=1000, status='normal', search=None)
    def GET(self):
        bRet, sRet = self.check_login()
        if not bRet:
            Log.err("user not login!")
            return web.seeother("/login")        
    
        #_deal_service_list= ArthurService.service_user_list(uId,page=1,length=1000, status=None, search=None)
        bRet, algoList = self.process(self._deal_service_list)
        if not bRet:
            Log.err("deal_service_list: %s" % (str(algoList)))
            self.make_error(algoList)
        if algoList is not None:
            serviceList=algoList['service_list']
        else:
            serviceList=[]
        uname=self.get_user_name()
        bRet, user_id =  HjsUser.get_user_uid(self.get_user_name())
        if not bRet:
            return False, user_id

        bRet, user_info = HjsUser.user_info(user_id)
        if not bRet:
            return False, 'something is wrong about users info' 
        defultTime=get_cur_day(0, format="%Y-%m-%d %H:%M:%S")
        token="部署服务后自动生成"
        if len(serviceList)<1:
            serviceList=[{"insert_tm":defultTime,"token":token}]
        return render.profile(uname,serviceList,user_info)

    def POST(self):
        return self.GET()

class ViewLandingPage(ViewBase):
    def GET(self):       
        return render_without_base.web_app()
if __name__ == "__main__":

    def test_login():
        Session.session = {}
        viewLogin = ViewLogin()
        viewLogin.userName = 'test'
        viewLogin.password = 'test'
        bRet, sRet = viewLogin._deal_login()
        if not bRet:
            Log.err("test_case ERR! %s" % (str(sRet)))
        else:
            Log.info("test_case SUCCESS!")

    test_login()
