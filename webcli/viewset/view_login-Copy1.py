# -*- coding: UTF-8 -*-

# author: s0nnet
# time: 2016-11-08
# desc: login view


import web
from view_base import *
from hjs_user_dao import *

from Arthur.ABtesting.utils.models import Experiment
import Arthur.ABtesting.utils.db as db
from markdown import markdown
import datetime
def determine_period():
    per={'period':'day'}
    period = per.get('period', 'day')
    if period not in ['day', 'week', 'month', 'year']:
        err = {'error': 'invalid argument: {0}'.format(period), 'status': 400}
        abort(400, jsonify(err))
    return period
def simple_markdown(experiment):
    description = experiment['description']
    if description and description != '':
        experiment['pretty_description'] = markdown(description)
    return experiment
def experiment_list():
    experiments = Experiment.all(redis=db.REDIS)
    period = determine_period()
    experiments = [simple_markdown(exp.objectify_by_period(period)) for exp in experiments]
    return experiments
def archived():
    experiments = Experiment.archived(redis=db.REDIS)
    period = determine_period()
    experiments = [simple_markdown(exp.objectify_by_period(period)) for exp in experiments]
    return experiments

def paused():
    experiments = Experiment.paused(redis=db.REDIS)
    period = determine_period()
    experiments = [simple_markdown(exp.objectify_by_period(period)) for exp in experiments]#[exp.name for exp in experiments]
    return experiments

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
        
        return True, None

    def POST(self):

        bRet, sRet = self.process(self._deal_login)
        if not bRet:
            Log.err("deal_login: %s" % (str(sRet)))
            return self.make_error(sRet)
        exp_list=experiment_list()+archived()+paused()
        if len(exp_list)>0:
            for exp_num in range(len(exp_list)):
                exp_list[exp_num]['id']=exp_num
                if exp_list[exp_num]['is_paused']:#如果实验结束，但未决胜负，则状态黑色2，否则绿色1
                    if exp_list[exp_num]['has_winner']:
                        exp_list[exp_num]['is_paused']={'result':u'已结束','status':'label-default'}
                        #exp_list[exp_num]['has_winner']={'result':u'已决','status':1}
                    else:
                        exp_list[exp_num]['is_paused']={'result':u'已结束','status':'label-default'}
                        #exp_list[exp_num]['has_winner']={'result':u'决战中','status':0}
                else:
                    exp_list[exp_num]['is_paused']={'result':u'进行中','status':'label-primary'}
                if exp_list[exp_num]['has_winner']:
                    exp_list[exp_num]['has_winner']={'result':u'已决','status':'label-default'}
                else:
                    exp_list[exp_num]['has_winner']={'result':u'决战中','status':'label-primary'}
                if len(exp_list[exp_num]['winner'])<1:
                    exp_list[exp_num]['winner']=u'暂无'           
        return self.make_response(ViewBase.RetMsg.MSG_SUCCESS)#render.index(exp_list)
class ViewApiLogin(ViewBase):
    def __init__(self):
        self._rDict = {
            "username": {'n': 'userName', 't': str, 'v': None},
            "password": {'n': 'passWord', 't': str, 'v': None}
        }

    def _check_param(self):

        if not self.userName: return False, "param(username) is None!"
        if not self.passWord: return False, "param(password) is NOne!"

        return True, None



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
        
        return True, None

    def POST(self):

        bRet, sRet = self.process(self._deal_login)
        if not bRet:
            Log.err("deal_login: %s" % (str(sRet)))
            return self.make_error(sRet)
        exp_list=experiment_list()+archived()+paused()
        if len(exp_list)>0:
            for exp_num in range(len(exp_list)):
                exp_list[exp_num]['id']=exp_num
                if exp_list[exp_num]['is_paused']:#如果实验结束，但未决胜负，则状态黑色2，否则绿色1
                    if exp_list[exp_num]['has_winner']:
                        exp_list[exp_num]['is_paused']={'result':u'已结束','status':'label-default'}
                        #exp_list[exp_num]['has_winner']={'result':u'已决','status':1}
                    else:
                        exp_list[exp_num]['is_paused']={'result':u'已结束','status':'label-default'}
                        #exp_list[exp_num]['has_winner']={'result':u'决战中','status':0}
                else:
                    exp_list[exp_num]['is_paused']={'result':u'进行中','status':'label-primary'}
                if exp_list[exp_num]['has_winner']:
                    exp_list[exp_num]['has_winner']={'result':u'已决','status':'label-default'}
                else:
                    exp_list[exp_num]['has_winner']={'result':u'决战中','status':'label-primary'}
                if len(exp_list[exp_num]['winner'])<1:
                    exp_list[exp_num]['winner']=u'暂无'           
        return render.index(exp_list)

class ViewLogout(ViewBase):
    def GET(self):
        Session.set_val("username", None)
        web.setcookie("username", None)
        return web.seeother("/login")

    def POST(self):
        return self.GET()


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
