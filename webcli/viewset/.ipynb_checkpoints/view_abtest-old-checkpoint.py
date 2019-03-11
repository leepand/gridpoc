# -*- coding: UTF-8 -*-

# author: leepand
# time: 2018-12-01
# desc: abtesting view and api
from view_base import *
from hjs_user_dao import *
from hjs_user import *
import os,sys
from Arthur.ABtesting.utils.models import Experiment
import Arthur.ABtesting.utils.db as db
from Arthur.common.rpc import thrifty
from Arthur.ABtesting.diversion.abtesting_thrift import Abtesting_thrift
from markdown import markdown
from Arthur_algolist import ArthurAlgoList


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
class ViewMyAbExp(ViewBase):
    def GET(self):
        bRet, sRet = self.check_login()
        if not bRet:
            Log.err("user not login!")
            return web.seeother("/login")
        return render.my_abexp()

    def POST(self):
        return self.GET()
class viewMyAbexpAdd(ViewBase):
    def GET(self):
        if not self.check_login():
            Log.err("user not login");
            return web.seeother("/login")
        #此处用layer自己的模版框架
        return render_without_base.my_abexpAdd()  
    
from operator import itemgetter 
class ViewAbtest(ViewBase):
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
        serviceList_bytime = sorted(exp_list,key = itemgetter('created_at'),reverse = True)
        exp_list = serviceList_bytime
        return render.abtest(exp_list)

    def POST(self):
        return self.GET()
class ViewExpdetails(ViewBase):
    def GET(self,name):
        bRet, sRet = self.check_login()
        if not bRet:
            Log.err("user not login!")
            return web.seeother("/login")
        exp_list=experiment_list()+archived()+paused()
        #设置abtest详情信息
        if len(exp_list)>0:
            for exp_num in range(len(exp_list)):
                if exp_list[exp_num]['name']==name:
                    exp_out=exp_list[exp_num]['alternatives']
                    if not exp_list[exp_num]['description']:
                        description=u'主人很懒没有设置'
                    else:
                        description=exp_list[exp_num]['description']
                    if not exp_list[exp_num]['kpi']:
                        kpi='defalut'
                    if len(exp_list[exp_num]['kpis'])<1:
                        kpis='default'
                    if exp_list[exp_num]['has_winner']:
                        label='label-default'
                        desc=u'已结束'
                    else:
                        label='label-primary'
                        desc=u'进行中'
                    lab_status={'label':label,'desc':desc,'description':description,\
                               'kpi':kpi,'kpis':kpis,\
                               'total_conversions':exp_list[exp_num]['total_conversions'],\
                               'total_participants':exp_list[exp_num]['total_participants'],\
                                'total_coversion_rate':100*round(exp_list[exp_num]['total_conversions']/(exp_list[exp_num]['total_participants']+0.000001),2),\
                               'created_at':exp_list[exp_num]['created_at']}
        #判断实验是否为control
        for _i in range(len(exp_out)):
            exp_out[_i]['confidence_interval']=round(exp_out[_i]['confidence_interval'],2)
            if exp_out[_i]['is_winner']:
                exp_out[_i]['is_winner_check']='fa fa-check'
                exp_out[_i]['is_winner_class']='label label-primary'
                exp_out[_i]['is_winner_result']=u'胜出'
            else:
                exp_out[_i]['is_winner_check']=''
                exp_out[_i]['is_winner_class']='label label-default'
                exp_out[_i]['is_winner_result']=u'暂未胜出'
            if exp_out[_i]['is_control']:
                exp_out[_i]['is_control_label']='label label-warning'
                exp_out[_i]['is_control_is']=u'控制组'
            else:
                exp_out[_i]['is_control_label']=''
                exp_out[_i]['is_control_is']=u''
        #abtest详情曲线图
        date_all=[]#每个实验的所有实验日期列表
        for j in exp_out:
            for k in j['data']:     
                date_all.append(k['date'])
        _m=max(date_all)
        new_list=[]
        str2date=datetime.datetime.strptime(_m,"%Y-%m-%d")
        for _i in range(5):
            d_j=str2date+datetime.timedelta(days=-_i)
            new_list.append(d_j.strftime("%Y-%m-%d"))
        data_date=sorted(new_list)
        #组合E chart所需要的信息
        exp_name_list=[]
        exp_info_list=[]

        exp_series=[]
        for _j_ in exp_out:
            exp_info={}
            exp_name_list.append(_j_['name'])
            exp_data=[0.0,0.0,0.0,0.0,0.0]
            for _iter in range(len(data_date)):
                for kk in _j_['data']:
                    if kk['date'] == data_date[_iter]:
                        exp_data[_iter]=kk['conversions']/(kk['participants']+0.001)
                        #exp_data.append(kk['conversions']/(kk['participants']+0.00001))
                    #else:
                    #    exp_data.append(0.00)
            exp_info['name']=_j_['name']
            exp_info['type']='line'
            exp_info['data']=exp_data
            exp_info_list.append(exp_info)
        return render.expdetails(exp_out,name,lab_status,exp_info_list,exp_name_list,data_date)

    def POST(self):
        return self.GET(name)  
    
class indexeeee:
    def GET(self):
        conn = sqlite3.connect(db.DB)
        cur = conn.cursor()
        cur.execute(db.SELECT_JOB)
        jobs = []
        for job in cur:
            state = job[0]
            state_text = setting.STATUS[int(job[0])]
            name = job[1]
            url = job[2]
            exe_time = job[3]
            id = job[4]
            dic_job = {'state': state, 'state_text': state_text, 'name': name, 'url': url,
                       'exe_time': exe_time, 'id': id}
            jobs.append(dic_job)
        return render.index(jobs)
    
    
class ViewAbtestCreate(ViewBase):
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
 
        return render.abtest_create(exp_list)
    
class ViewApiAbtestAdd(ViewBase):
    def __init__(self):
        self._rDict = {
            "expid": {'n': 'expId', 't': str, 'v': None},
            "explist": {'n': 'expList', 't': str, 'v': None},
            "clientid": {'n': 'clientId', 't': str, 'v': None},
        }

    def _check_param(self):
        bRet, sRet = super(ViewApiAbtestAdd, self)._check_param()
        if not bRet:
            return bRet, sRet
        
        return True, None

    def _deal_user_add(self):
        bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        if not bRet:
            return False, sRet
        if not is_admin:
            return False, 'No permission do abtest experiment add'
        self.expList=[str(i) for i in self.expList.split(',')]
        status=abtest_add(self.expId, self.expList, self.clientId)
        return True,status

    def POST(self):
        if not self.check_login():
            return self.make_error("user not login")

        bRet, sRet = self.process(self._deal_user_add)
        if not bRet:
            Log.err("add user error: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(ViewBase.RetMsg.MSG_SUCCESS)


def abtest_add(exp_id,alt,client_id):
    try:
        with thrifty.Client(Abtesting_thrift) as c:
            return c.diversion(exp_id,alt,client_id)
    except:
        print 'wrong exp create'
        
    
class ViewApiAbServList(ViewBase):
    #def _check_param(self):
    #    bRet, sRet = super(ViewApiServMsgUser, self)._check_param()
    #   if not bRet:
    #        return False, sRet
    #    
    #    return True, None
    
    def _deal_ab_serv_list(self):
        #msg_info = get_req_all_param()
        #userName=msg_info.get('userName','')
        #projectName = msg_info.get('projectName','')
        #bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        #if not bRet:
        #    return False, sRet
        #if not is_admin:
        #    return False, 'No permission do user info'
        #bRet, user_id =  HjsUser.get_user_uid(self.get_user_name())
        #if not bRet:
        #    return False, user_id
        #_bRet, msg_user_list=ArthurMsg.query_node_msg_list_by_usrproj(userName,projectName)
        #_bRet, msg_user_list =HjsUserDao.query_node_msg_user_list(user_id,"../static/images/user-icon.png")
        #if not _bRet:
        #    return False, msg_user_list
        #print 'msg_info = get_req_all_param()',msg_info 
        #print 'comments;;;;;;;',msg_user_list
        exp_list=experiment_list()+archived()+paused()
        is_win_list=[]
        is_pause_list=[]
        is_end_list = []
        ab_info_dict={}
        if len(exp_list)>0:
            for exp_num in range(len(exp_list)):
                exp_list[exp_num]['id']=exp_num
                if exp_list[exp_num]['is_paused']:#如果实验结束，但未决胜负，则状态黑色2，否则绿色1
                    is_pause_list.append(exp_list[exp_num])
                if exp_list[exp_num]['is_paused'] or exp_list[exp_num]['has_winner']:
                    is_end_list.append(exp_list[exp_num])
                if exp_list[exp_num]['has_winner']:
                    is_win_list.append(exp_list[exp_num])
        bRet, sRet =ArthurAlgoList.algo_list_forautocomplete()
        abservlist= sRet
        ab_info_dict['abservlist']=abservlist
        ab_info_dict['is_pause_list']=is_pause_list
        ab_info_dict['is_win_list']=is_win_list
        ab_info_dict['is_end_list']=is_end_list
        ab_info_dict['all_exp_cnt']=len(exp_list)
        ab_info_dict['is_win_ratio']="width: {data}%;".format(data=int(round((len(is_win_list)/(len(exp_list)+0.0000001)),2)*100))
        ab_info_dict['is_pause_ratio']="width: {data}%;".format(data=int(round((len(is_pause_list)/(len(exp_list)+0.0000001)),2)*100))
        ab_info_dict['is_end_ratio']="width: {data}%;".format(data=int(round((len(is_end_list)/(len(exp_list)+0.0000001)),2)*100))
        return True,ab_info_dict

    def GET(self):
        if not self.check_login():
            return self.make_error("user not login")

        bRet, sRet = self.process(self._deal_ab_serv_list)
        if not bRet:
            Log.err("deal_ab_serv_list: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(sRet) 