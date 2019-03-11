# -*- coding: UTF-8 -*-

# author: leepand
# time: 2018-12-01/update 2019-01-16
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
        #abort(400, jsonify(err))
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
from Arthur_Abtesting_dao import ArthurAbTestingDao

class ViewApiAbtestAdd(ViewBase):
    def __init__(self):
        self._rDict = {
            "expid": {'n': 'expId', 't': str, 'v': None},
            "explist": {'n': 'expList', 't': str, 'v': None},
            "clientid": {'n': 'clientId', 't': str, 'v': None},
            "expdesc": {'n': 'expDesc', 't': str, 'v': None},
        }

    def _check_param(self):
        bRet, sRet = super(ViewApiAbtestAdd, self)._check_param()
        if not bRet:
            return bRet, sRet
        
        return True, None

    def _deal_abtest_add(self):
        bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        if not bRet:
            return False, sRet
        #if not is_admin:
        #    return False, 'No permission do abtest experiment add'
        bRet, user_id =  HjsUser.get_user_uid(self.get_user_name())
        if not bRet:
            return False, user_id  
        
        bRet,is_ab_exsit = ArthurAbTestingDao.query_node_by_abname(self.expId)
        if len(is_ab_exsit)>1:
            return False, 'Experiment Name you create is exist!'
        abname=self.expId
        bRet,insert_ab = ArthurAbTestingDao.insert_node(user_id,abname)
     

        self.expList=[str(i) for i in self.expList.split(',')]
        #status=abtest_add(self.expId, self.expList, self.clientId)
        exp=Experiment.find_or_create(self.expId,self.expList,redis=db.REDIS)
        exp.update_description(self.expDesc)
        return True,exp

    def POST(self):
        if not self.check_login():
            return self.make_error("user not login")

        bRet, sRet = self.process(self._deal_abtest_add)
        if not bRet:
            Log.err("add abtset error: %s" % (str(sRet)))
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
    
def find_or_404(experiment_name,kpi=None):
    try:
        experiment_name = experiment_name
        exp = Experiment.find(experiment_name, db.REDIS)
        if kpi:#设置kpi，用于页面查询，需要kpis列表非空否则出错，server端调用时也需要有kpi的参数输入
            exp.set_kpi(kpi)
        #if request.args.get('kpi'):
        #   exp.set_kpi(request.args.get('kpi'))
        return True,exp
    except ValueError:
        return False,'None'
#我的实验页面
class ViewApiMyAbList(ViewBase):
    def _deal_my_ab_list(self):
        bRet, user_id =  HjsUser.get_user_uid(self.get_user_name())
        if not bRet:
            return False, user_id  
        bRet, my_ab_list = ArthurAbTestingDao.query_node_ab_list_by_uid(user_id)
        my_ab_list_all=[]
        my_ab_list_win=[]
        my_ab_list_paused=[]
        my_ab_list_archived=[]
        my_ab_list_running = []
        if len(my_ab_list)>0:
            for ab_dict in my_ab_list:
                ab_info={}
                abName = ab_dict['abname']
                bRet,experiment= find_or_404(abName)
                if bRet:
                    period = determine_period()
                    obj = simple_markdown(experiment.objectify_by_period(period))
                    ab_info['created_at']=experiment.created_at
                    description = obj['description']
                    if description and description != '':
                        ab_info['description']=description
                    else:
                        ab_info['description']='目前还没有实验描述，赶紧在详情页添加吧'
                    ab_info['abname'] = abName
                    if obj['kpis']:
                        ab_info['kpis'] = obj['kpis']
                    else:
                        ab_info['kpis'] = []
                    ab_info['has_winner']=obj['has_winner']
                    ab_info['is_archived']=obj['is_archived']
                    ab_info['is_paused']=obj['is_paused']
                    if obj['has_winner']:
                        my_ab_list_win.append(ab_info)
                    if  obj['is_archived']:
                        my_ab_list_archived.append(ab_info)
                    if  obj['is_paused']:
                        my_ab_list_paused.append(ab_info)
                    if not obj['is_paused'] and not obj['is_archived']:
                        if not obj['has_winner']:
                            my_ab_list_running.append(ab_info)
                    my_ab_list_all.append(ab_info)
                else:
                    return False,'%s is not found!'%abName
 
        return True,{'my_ab_list_all':my_ab_list_all,'my_ab_list_win':my_ab_list_win,'my_ab_list_archived':my_ab_list_archived,
                    'my_ab_list_paused':my_ab_list_paused,'my_ab_list_running':my_ab_list_running}

    def GET(self):
        if not self.check_login():
            return self.make_error("user not login")

        bRet, sRet = self.process(self._deal_my_ab_list)
        if not bRet:
            Log.err("deal_my_ab_list: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(sRet)     
    
    
class ViewApiMyAbDetails(ViewBase):
    def __init__(self):
        self._rDict = {
            "abname": {'n': "abName", 't': str, 'v': None}
        }

    def _check_param(self):
        bRet, sRet = super(ViewApiMyAbDetails, self)._check_param()
        if not bRet:
            return False, sRet
        return True, None

    def _deal_Myab_details(self):
        #bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        #if not bRet:
        #    return False, sRet
        #if not is_admin:
        #    return False, 'No permission to do this'
        bRet,experiment= find_or_404(self.abName)
        exp_compute_info={}
        if experiment:
            period = determine_period()
            obj = simple_markdown(experiment.objectify_by_period(period))
            exp_out=obj['alternatives']#实验各组详情数据
            if not obj['description']:
                description=u'目前还没有实验描述，赶紧添加吧'
            else:
                description=obj['description']
            if len(obj['kpis'])>0:
                kpis=obj['kpis']
            else:
                kpis='defalut'
            exp_compute_info={'description':description,'kpis':kpis,\
                      'total_conversions':obj['total_conversions'],\
                      'total_participants':obj['total_participants'],\
                      'total_coversion_rate':100*round(obj['total_conversions']/(obj['total_participants']+0.000001),2),\
                      'created_at':obj['created_at']
                     }          
        else:
            return False,'No experiment found!'
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

        return True,{"exp_info_list":exp_info_list,"exp_daily_details":exp_out,\
                    "exp_name_list4Echart":exp_name_list,"exp_info_list4Echart":exp_info_list,\
                    "data_date4Echart":data_date,'obj':obj,'exp_compute_info':exp_compute_info}

    def GET(self):
        bRet, sRet = self.check_login()
        if not bRet:
            return web.seeother("/login")
        bRet, sRet = self.process(self._deal_Myab_details)
        if not bRet:
            Log.err("deal_Myab_details: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(sRet)
