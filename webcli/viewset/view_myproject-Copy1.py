# -*- coding: UTF-8 -*-

# author: leepand
# time: 2018-12-08
# desc: index view

from view_base import ViewBase,render,render_without_base
from Arthur.core.entities.bean.hjs_user import HjsUser
#from hjs_index import *
from Arthur.core.entities.base.bs_log import Log

from Arthur.core.entities.bean.Arthur_service import ArthurService
from Arthur.core.entities.base.bs_util import get_myip
from Arthur.core.entities.bean.Arthur_algolist import ArthurAlgoList
from Arthur.core.entities.dao.Arthur_AlgoStar_dao import ArthurAlgoStarDao 

class ViewMyProject(ViewBase):
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
        return render.my_project_main(uname,serviceList,user_info)

    def POST(self):
        return self.GET()
class ViewOtherProject(ViewBase):
    def _deal_service_list(self):
        _bRet,uId=HjsUser.get_user_uid(self.uName)
        if not _bRet:
            return False, uId
        return ArthurService.service_user_list(uId,page=1,length=1000, status='normal', search=None)
    def GET(self,username):
        bRet, sRet = self.check_login()
        if not bRet:
            Log.err("user not login!")
            return web.seeother("/login")        
        self.uName=username
        #_deal_service_list= ArthurService.service_user_list(uId,page=1,length=1000, status=None, search=None)
        bRet, algoList = self.process(self._deal_service_list)
        if not bRet:
            Log.err("deal_service_list: %s" % (str(algoList)))
            self.make_error(algoList)
        if algoList is not None:
            serviceList=algoList['service_list']
        else:
            serviceList=[]
        
        bRet, user_id =  HjsUser.get_user_uid(username)
        if not bRet:
            return False, user_id

        bRet, user_info = HjsUser.user_info(user_id)
        if not bRet:
            return False, 'something is wrong about users info' 
        return render.other_project_main(username,serviceList,user_info)

    def POST(self):
        return self.GET(username)



#客户端生成
SCORE_SRC = '''
# coding:utf-8
"""
Compatible for python2.x and python3.x
requirement: pip install requests Arthur
"""
from __future__ import print_function
from Arthur.api_server.client import Client
client =Client('{ip}:{port}',auth_token='该项目的token信息')
input = {data}
# 结果 
print(client.{function_name}(**input))
'''
BASE_INFO = '''
# coding:utf-8
"""
Compatible for python2.x and python3.x
requirement: pip install requests Arthur
"""
from __future__ import print_function
from Arthur.api_server.client import Client
client =Client('{ip}:{port}',auth_token='该项目的apikey')
'''
INFER_INFO = '''
input = {data}
# 结果 
print(client.{function_name}(**input))
'''
def load_function(function_spec, path=None, name=None):
    if "." not in function_spec:
        raise Exception("Invalid function: {}, please specify it as module.function".format(function_spec))

    mod_name, func_name = function_spec.rsplit(".", 1)
    path = path or "/"+func_name
    name = name or func_name
    return name

def load_functions(function_specs):
    return [load_function(function_spec) for function_spec in function_specs]


class ViewAlgoDetails(ViewBase):
    def GET(self,username,projectname):
        bRet, sRet = self.check_login()
        if not bRet:
            Log.err("user not login!")
            return web.seeother("/login")  
        _bRet, uId = HjsUser.get_user_uid(username)
        if not _bRet:
            return False,uId
        _bRet_,algo_detail_info=ArthurService.algo_proj_info(uId,projectname)
        host=algo_detail_info['host']
        port = algo_detail_info['port']
        data=algo_detail_info['remark']
        tags=algo_detail_info['tags']
        funcslist_str=algo_detail_info['funcslist']
        algodesc=algo_detail_info['algodesc']
        
        base_algo_info=BASE_INFO.format(ip=get_myip(), port=port)
        
        if '|' in data:
            datalist=data.split("|")
        else:
            datalist=[data]

        infer_info_list=[]
        funcs_info=load_functions(funcslist_str.split(","))
        for inter in range(len(funcs_info)):
            try:
                datainfo=datalist[inter]
                if len(datainfo)<1:
                    datainfo=None
            except:
                datainfo=None
            infer=INFER_INFO.format(data=datainfo,function_name=funcs_info[inter])
            infer_info_list.append(infer)
        infer_algo_info='\n'.join(infer_info_list)
        python_client_info=base_algo_info+infer_algo_info
        
        tag_ul_list="-".join(tags.split()).split(',')
        taglist=tags.split(',')
        tags_info=(dict(zip(tag_ul_list,taglist)))
        details_info={'infer_algo_info':python_client_info,'tags_info':tags_info,'datainfo':"|".join(datalist),'algodesc':algodesc}
        return render.project_profile(username,projectname,details_info)

    def POST(self):
        return self.GET(username,projectname)



"""class ViewAbtest(ViewBase):
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

        return render.abtest(exp_list)

    def POST(self):
        return self.GET()"""


class ViewApiServList(ViewBase):
    def __init__(self):
        self._rDict = {
            "UName": {'n': "UName", 't': str, 'v': None}#
        }

    def _check_param(self):
        bRet, sRet = super(ViewApiServList, self)._check_param()
        if not bRet:
            return False, sRet
        return True, None
    
    def _deal_serv_user_list(self):
        #algo_from = get_req_all_param()
        #print algo_from,'dddd'
        algo_Uname= self.get_user_name()
        if self.UName=='myself':
            algo_Uname= self.get_user_name()   
        else:
            algo_Uname = self.UName
        _bRet,uId=HjsUser.get_user_uid(self.get_user_name())
        if not _bRet:
            return False, uId
        if algo_Uname=='zoo':
             _bRet,algo_uId=True,'all_algo_lists'#改变量将不起作用
        else:
            _bRet,algo_uId=HjsUser.get_user_uid(algo_Uname)
        
        if self.UName=='zoo':
            bRet,algo_list =ArthurAlgoList.data_show(algo_uId,'zoo')
        else:
            bRet,algo_list =ArthurAlgoList.data_show(algo_uId,'user')
        algo_list_info={}
        algo_star_info={}
        algo_User_star_all=0
        _algo_list=algo_list['dt_algo_list']['algo_list']
        algo_User_algocnt=len(_algo_list)
        if len(_algo_list)<1:
            algo_list = _algo_list
            algo_User_star_all=0
            #star_list = []
        else:
            algo_list = _algo_list
            for _inter in range(len(_algo_list)):
                algouId=_algo_list[_inter]['uid']
                algoname= _algo_list[_inter]['algoname']
                _br, algo_star_info_cnt = ArthurAlgoStarDao.query_status_cnt_by_algo(algouId,algoname)
                if algo_star_info_cnt[0]['star_cnt_algo'] is None:
                    star_cnt=0
                else:
                    star_cnt = int(algo_star_info_cnt[0]['star_cnt_algo'])
                algo_User_star_all+=star_cnt
                _br, algo_star_info_list=ArthurAlgoStarDao.query_node_by_uid_algo_algouid(uId,algouId, algoname)
                if len(algo_star_info_list)<1:
                    star_status='nostar'
                    algo_star_info[algoname]={'star_status':star_status,'star_cnt':star_cnt}
                    
                else:
                    status= algo_star_info_list[0]['star_status']
                    algo_star_info[algoname]={'star_status':status,'star_cnt':star_cnt}
                    
        
        algo_list_info = {"user":self.get_user_name(),"algolist":algo_list,'star_info':algo_star_info,\
                          'algo_User_star_all':algo_User_star_all,'algo_User_algocnt':algo_User_algocnt}
        
        #if not bRet:
        #    return False, algo_list_info
   
        return True, algo_list_info
    def GET(self):
        if not self.check_login():
            return self.make_error("user not login")

        bRet, sRet = self.process(self._deal_serv_user_list)
        if not bRet:
            Log.err("deal_serv_user_list: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(sRet) 