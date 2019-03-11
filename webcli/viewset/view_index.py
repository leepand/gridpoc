# -*- coding: UTF-8 -*-

# author: s0nnet
# time: 2016-11-08
# desc: index view

from view_base import ViewBase,render,render_without_base
from Arthur.core.entities.bean.hjs_user import HjsUser
from Arthur.core.abtesting.utils.models import Experiment
import Arthur.core.abtesting.utils.db as db
from Arthur.core.entities.base.bs_log import Log
import web

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

class ViewIndex(ViewBase):
    def GET(self):
        bRet, sRet = self.check_login()
        if not bRet:
            Log.err("user not login!")
            return web.seeother("/login")
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

    def POST(self):
        return self.GET()

class Viewwizard(ViewBase):
    def GET(self):
        bRet, sRet = self.check_login()
        if not bRet:
            Log.err("user not login!")
            return web.seeother("/login")
             
        return render_without_base.wizard_create_profile()

    def POST(self):
        return self.GET()
    


class ViewApiDataCount(ViewBase):
    def _deal_data_show(self):
        return HjsIndex.data_show(self.get_user_name())


    def GET(self):
        if not self.check_login():
            return self.make_error("user not login")

        bRet, sRet = self.process(self._deal_data_show)
        if not bRet:
            Log.err("deal_user_list: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(sRet)



