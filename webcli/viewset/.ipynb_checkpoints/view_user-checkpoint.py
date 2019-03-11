# -*- coding: UTF-8 -*-

# author: s0nnet
# time: 2016-11-08
# desc: user view


from view_base import ViewBase,render,render_without_base
from Arthur.core.entities.bean.hjs_user import HjsUser
from Arthur.core.entities.dao.hjs_user_dao import HjsUserDao
from Arthur.core.entities.base.bs_log import Log


class ViewUserList(ViewBase):
    def GET(self):
        if not self.check_login():
            Log.err("user not login")
            return web.seeother("/login")
        
        return render.user_list()


class ViewUserAdd(ViewBase):
    def GET(self):
        if not self.check_login():
            Log.err("user not login")
            return web.seeother("/login")
        
        return render.user_add()
class ViewUserGrade(ViewBase):
    def GET(self):
        if not self.check_login():
            Log.err("user not login")
            return web.seeother("/login")
        
        return render.user_grade()

class ViewUserEdit(ViewBase):
    def GET(self):
        if not self.check_login():
            Log.err("user not login!")
            return web.seeother("/login")
        #该部分不需要公共模版，所以采用去掉base部分的
        #return render_without_base.user_edit()
        return render.user_edit()



class ViewApiUserList(ViewBase):
    def _deal_user_list(self):
        bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        #当前登陆用户self.get_user_name()
        if not bRet:
            return False, sRet
        if not is_admin:
            return False, 'No permission view user list'
        #print 'fffff:',HjsUser.get_user_uid('leepand3')
        #print 'ddd::::',HjsUser.get_user_uid('hahahahahah')
        return HjsUser.user_list(self.get_user_name())

    def GET(self):
        if not self.check_login():
            return self.make_error("user not login")

        bRet, sRet = self.process(self._deal_user_list)
        if not bRet:
            Log.err("deal_user_list: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(sRet)


class ViewApiUserAdd(ViewBase):
    def __init__(self):
        self._rDict = {
            "nickname": {'n': 'nickName', 't': str, 'v': None},
            "username": {'n': 'userName', 't': str, 'v': None},
            "password": {'n': 'passWord', 't': str, 'v': None},
            "phone": {'n': 'Phone', 't': str, 'v': None},
            "email": {'n': 'Email', 't': str, 'v': ''},
            "priv": {'n': 'Priv', 't': int, 'v': 1},
            "remark": {'n': 'Remark', 't': str, 'v': None}
        }

    def _check_param(self):
        bRet, sRet = super(ViewApiUserAdd, self)._check_param()
        if not bRet:
            return bRet, sRet
        
        return True, None

    def _deal_user_add(self):
        bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        try:
            _bRet, is_exist=HjsUser.get_user_uid(self.userName)
            if _bRet:
                return False, 'user already exist! cannot do user add'
        except:
            pass
        if not bRet:
            return False, sRet
        if not is_admin:
            return False, 'No permission do user add'      

        return HjsUser.user_add(self.nickName, self.userName, self.passWord, self.Phone, self.Email, self.Priv,self.Remark)

    def POST(self):
        if not self.check_login():
            return self.make_error("user not login")

        bRet, sRet = self.process(self._deal_user_add)
        if not bRet:
            Log.err("add user error: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(ViewBase.RetMsg.MSG_SUCCESS)


class ViewApiUserInfo(ViewBase):
    def __init__(self):
        self._rDict = {
            "uid": {'n': 'uId', 't': int, 'v': None}
        }
    
    def _check_param(self):
        bRet, sRet = super(ViewApiUserInfo, self)._check_param()
        if not bRet:
            return False, sRet
        
        return True, None

    def _deal_user_info(self):
        bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        if not bRet:
            return False, sRet
        if not is_admin:
            return False, 'No permission do user info'
        bRet, user_id =  HjsUser.get_user_uid(self.get_user_name())
        if not bRet:
            return False, user_id

        return HjsUser.user_info(self.uId)

    def GET(self):
        if not self.check_login():
            return self.make_error("user not login")

        bRet, sRet = self.process(self._deal_user_info)
        if not bRet:
            Log.err("deal_user_info: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(sRet)


class ViewApiUserUpdate(ViewBase):
    def __init__(self):
        self._rDict = {
            "uid": {'n': 'uId', 't': int, 'v': None},
            "nickname": {'n': 'nickName', 't': str, 'v': None},
            "username": {'n': 'userName', 't': str, 'v': None},
            "password": {'n': 'passWord', 't': str, 'v': None},
            "phone": {'n': 'Phone', 't': str, 'v': None},
            "email": {'n': 'Email', 't': str, 'v': ''},
            "priv": {'n': 'Priv', 't': str, 'v':None}
        }

    def _check_param(self):
        bRet, sRet = super(ViewApiUserUpdate, self)._check_param()
        if not bRet:
            return bRet, sRet
        
        return True, None

    def _deal_user_update(self):
        bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        if not bRet:
            return False, sRet
        if not is_admin:
            return False, 'No permission do user update'


        #不允许修改自己的权限和用户名
        bRet, user_id =  HjsUser.get_user_uid(self.get_user_name())
        if not bRet:
            return False, user_id
        bRet2, sRet = HjsUserDao.query_node_by_username(self.get_user_name())
        #不需要修改用户名,uid不变
        status,user_info=HjsUser.user_info(self.uId)
        if not status:
            return False, user_info

        #print 'quanxian',sRet['privilege'],self.Priv
        if user_id == self.uId:
            if self.userName!=self.get_user_name():
                return False, 'do not allow update yourself name!'
            if int(sRet['privilege']) != int(self.Priv): # is_admin user
                return False, 'do not allow update yourself privilege!'
        else:
            if user_info.username!=self.userName:
                return False, 'do not allow update other peoples name!'           
        return HjsUser.user_update(self.uId, self.nickName, self.userName, self.passWord, self.Phone, self.Email, self.Priv)

    def POST(self):
        if not self.check_login():
            return self.make_error("user not login")

        bRet, sRet = self.process(self._deal_user_update)
        if not bRet:
            Log.err("update user error: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(ViewBase.RetMsg.MSG_SUCCESS)


class ViewApiUserDel(ViewBase):
    def __init__(self):
        self._rDict = {
            "uid": {'n': 'uId', 't': int, 'v': None}
        }
    
    def _check_param(self):
        bRet, sRet = super(ViewApiUserDel, self)._check_param()
        if not bRet:
            return bRet, sRet
        
        return True, None

    def _deal_user_del(self):
        bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        if not bRet:
            return False, sRet
        if not is_admin:
            return False, 'No permission do user del'
        bRet, user_id =  HjsUser.get_user_uid(self.get_user_name())
        if not bRet:
            return False, user_id
        if user_id == self.uId:
            return False, 'do not allow delete yourself'

        return HjsUser.user_del(self.uId)

    def POST(self):
        if not self.check_login():
            return self.make_error("user not login")

        bRet, sRet = self.process(self._deal_user_del)
        if not bRet:
            Log.err("deal_user_del: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(ViewBase.RetMsg.MSG_SUCCESS)



