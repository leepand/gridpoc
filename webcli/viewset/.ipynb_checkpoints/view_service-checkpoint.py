# -*- coding: UTF-8 -*-

# author: leepand
# time: 2018-11-30
# desc: model deploy

from view_base import ViewBase,render,render_without_base
from Arthur.core.entities.bean.hjs_user import HjsUser
from Arthur.core.entities.dao.hjs_user_dao import HjsUserDao

from Arthur.core.entities.bean.Arthur_service import ArthurService
from Arthur.core.utils.token_util import Connector
from Arthur.core.entities.base.bs_log import Log
from Arthur.core.controller.deploy.driver.arthur_microservice import ArthurMicroserviceDeployDriver

import web
from web_util import get_req_all_param
#from Arthur.core.entities.dao.hjs_user_dao import *
#参见view_myproject.py
from Arthur.core.apiserver.client import Client
import json
from Arthur.core.entities.base.bs_util import get_myip
#客户端生成

from arthur_utils.file_process import FileStore
from arthur_utils.algo_publish import model_publish 
from arthur_utils.file_utils import list_subdirs
import os,sys
import time
#重构于2019-01-21
class ViewAlgoAdd(ViewBase):
    def GET(self):
        if not self.check_login():
            Log.err("user not login");
            return web.seeother("/login")
        return render_without_base.service_add()#render.service_add()  

class ViewAlgoList(ViewBase):
    def GET(self):
        if not self.check_login():
            Log.err("user not login");
            return web.seeother("/login")
        return render.service_list()    

from operator import itemgetter 
class ViewAlgoZooList (ViewBase):
    def _deal_service_list(self):
        return ArthurService.service_zoo_list(page=1,length=1000, status='normal', search=None)
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
        #print 'algoList',algoList
        if  algoList is not None and "service_list" in algoList:
            serviceList=algoList['service_list']
            serviceList_bytime = sorted(serviceList,key = itemgetter('insert_tm'),reverse = True)
        else:
            serviceList=[]
            serviceList_bytime=[]
        
        
        #uname=self.get_user_name()
        return render.service_zoo_list(serviceList,serviceList_bytime)

    def POST(self):
        return self.GET()    
#用于遍历项目的子目录
def list_all_filepaths(absolute_dirpath):
    """Returns all filepaths within dir relative to dir root"""
    return [
        os.path.relpath(os.path.join(dirpath, file), absolute_dirpath)
        for (dirpath, dirnames, filenames) in os.walk(absolute_dirpath)
        for file in filenames
    ]
#2018-12-29 update    
class ViewApiAlgoPublish(ViewBase):
    def __init__(self):
        self.deploy_info_publish = ArthurMicroserviceDeployDriver('remote')
        self._rDict = {
            "aid": {'n': "aId", 't': int, 'v': None}
        }

    def _check_param(self):
        bRet, sRet = super(ViewApiAlgoPublish, self)._check_param()
        if not bRet:
            return False, sRet
        return True, None

    def _deploy_algo_publish(self):
        bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        if not bRet:
            return False, sRet
        if not is_admin:
            return False, 'No permission to do this'
        #_bRet , algo_info = ArthurService.algo_info(self.aId)
        #if not _bRet:
        #    return False, algo_info
        #project_name=algo_info['algoname']     
        userName = self.get_user_name()
        bRet,msg = self.deploy_info_publish.algoDeployUI(self.aId,userName)
        if bRet:
            return True,'algo publish success!'
        else:
            return False,' algo publish failed!'


    def POST(self):
        bRet, sRet = self.check_login()
        if not bRet:
            return web.seeother("/login")
        bRet, sRet = self.process(self._deploy_algo_publish)
        if not bRet:
            Log.err("deploy_algo_publish: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(ViewBase.RetMsg.MSG_SUCCESS)
    
#2019-01-05 add 
def kill9_byname(strname):
    """
    kill -9 process by name
    """
    fd_pid = os.popen("ps -ef | grep -v grep |grep %s \
            |awk '{print $2}'" % (strname))
    pids = fd_pid.read().strip().split('\n')
    fd_pid.close()
    for pid in pids:
        #print pid
        os.system("kill -9 %s" % (pid))
    return True

class ViewApiAlgoUnpublish(ViewBase):
    def __init__(self):
        self._rDict = {
            "aid": {'n': "aId", 't': int, 'v': None}
        }

    def _check_param(self):
        bRet, sRet = super(ViewApiAlgoUnpublish, self)._check_param()
        if not bRet:
            return False, sRet
        return True, None

    def _deploy_algo_unpublish(self):
        bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        if not bRet:
            return False, sRet
        if not is_admin:
            return False, 'No permission to do this'
        _bRet , algo_info = ArthurService.algo_info(self.aId)
        if not _bRet:
            return False, algo_info
        project_name=algo_info['algoname']
        funcslist=algo_info['funcslist']
        port=algo_info['port']
        token=algo_info['token']
        undeploy=kill9_byname(str(port))
        time.sleep(5)
        if undeploy:
            ArthurService.algo_publish_status_update(self.aId,'stop')
            return True,'algo unpublish success!'
        else:
            return False,' algo unpublish failed!'
        return True,"Unpublished Service"#_run_server(self.func, self.token, self.host, self.port)

    def POST(self):
        bRet, sRet = self.check_login()
        if not bRet:
            return web.seeother("/login")
        bRet, sRet = self.process(self._deploy_algo_unpublish)
        if not bRet:
            Log.err("deploy_algo_unpublish: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(ViewBase.RetMsg.MSG_SUCCESS)
    


    
class ViewApiServUserList(ViewBase):
    def __init__(self):
        self._rDict = {
            "page": {'n': "page", 't': int, 'v': 1},
            "length": {'n': "length", 't': int, 'v': 20},
            "status": {'n': "status", 't': str, 'v': 'all'},
            "search": {'n': "search", 't': str, 'v': ''}
        }
    
    def _check_param(self):
        bRet, sRet = super(ViewApiServUserList, self)._check_param()
        if not bRet:
            return False, sRet
        return True, None

    def _deal_service_list(self):
        _bRet,uId=HjsUser.get_user_uid(self.get_user_name())
        if not _bRet:
            return False, uId
        return ArthurService.service_user_list(uId,self.page, self.length, self.status, self.search)

    # get all service list
    def GET(self):
        bRet, sRet = self.check_login()
        if not bRet:
            return web.seeother("/login")
        bRet, algoList = self.process(self._deal_service_list)
        if not bRet:
            Log.err("deal_service_list: %s" % (str(algoList)))
            return self.make_error(algoList)

        return self.make_response(algoList)

    # do search the service list
    def POST(self):
        bRet, sRet = self.check_login()
        if not bRet:
            return web.seeother("/login")
        bRet, algoList = self.process(self._deal_service_list)
        if not bRet:
            Log.err("deal_search_service_list: %s" % (str(algoList)))
            return self.make_error(algoList)

        return self.make_response(algoList)
    
    
class ViewApiServUserAdd(ViewBase):
    def __init__(self):
        self.deploy_info_add = ArthurMicroserviceDeployDriver('remote')
        self._rDict = {
            "projectname": {'n': "projectname", 't': str, 'v': None},
            "projectdesc": {'n': "projectdesc", 't': str, 'v': None},
            "tags": {'n': "tags", 't': str, 'v': None},
            "funcspath": {'n': "funcspath", 't': str, 'v': None},
            "funclist": {'n': "funclist", 't': str, 'v': None},
            "host": {'n': "host", 't': str, 'v': None},
            #"port": {'n': "port", 't': int, 'v': None},
            "algo_field": {'n': "algo_field", 't': int, 'v': None},
            "opertype": {'n': "opertype", 't': str, 'v': None},
            "projecttm": {'n': "projecttm", 't': str, 'v': None},
            "emailmsg": {'n': "emailmsg", 't': str, 'v': None},
            "remark": {'n': "remark", 't': str, 'v': None}
        }

    def _check_param(self):
        bRet, sRet = super(ViewApiServUserAdd, self)._check_param()
        if not bRet:
            return False, sRet
        return True, None

    def _deal_service_add(self):
        
        bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        if not bRet:
            return False, sRet
        #if not is_admin:
        #    return False, 'No permission to do this'
        _bRet,uId=HjsUser.get_user_uid(self.get_user_name())
        if not _bRet:
            return False, uId       
        rel_path='arthur_runs/'+self.get_user_name()
        port=None#不需要用户指定port
        return self.deploy_info_add.algoInfoAdd(self.get_user_name(),self.projectname,self.funcspath,self.funclist,self.algo_field,port,\
                   self.projecttm,str(self.remark),self.emailmsg,self.opertype,self.projectdesc,self.tags)
     
        #return ArthurService.service_add(uId,self.projectname, self.projectdesc,self.opertype,rel_path,#self.funcspath
        #                         self.funclist,self.tags,self.algo_field,self.host,self.port,self.projecttm,
        #                         self.emailmsg,str(self.remark))

    def POST(self):
        bRet, sRet = self.check_login()
        if not bRet:
            return web.seeother("/login")
        bRet, sRet = self.process(self._deal_service_add)
        if not bRet:
            Log.err("deal_service_add: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(ViewBase.RetMsg.MSG_SUCCESS)
    

BASE_INFO = '''
# coding:utf-8
"""
Compatible for python2.x and python3.x
requirement: pip install requests Arthur
"""
from Arthur.api_server.client import Client
client =Client('{ip}',auth_token={token})
'''
INFER_INFO = '''client.{function_name}(**input_data)'''
def load_function(function_spec, path=None, name=None):
    if "." not in function_spec:
        raise Exception("Invalid function: {}, please specify it as module.function".format(function_spec))

    mod_name, func_name = function_spec.rsplit(".", 1)
    path = path or "/"+func_name
    name = name or func_name
    return name

def load_functions(function_specs):
    return [load_function(function_spec) for function_spec in function_specs]


class ViewApiRunApi22(ViewBase):
    #def _check_param(self):
    #    bRet, sRet = super(ViewApiServMsgUser, self)._check_param()
    #   if not bRet:
    #        return False, sRet
        
    #    return True, None
    
    def _deal_run_api_example(self):
        msg_info = get_req_all_param()
        #获取api信息
        model_info=eval(msg_info['algoinfo'])
        username= model_info['username']
        proJectname= model_info['algoname']
        _bRet, uId = HjsUser.get_user_uid(username)
        if not _bRet:
            return False,uId
        _bRet_,algo_detail_info= ArthurService.algo_proj_info(uId,proJectname)
        host=algo_detail_info['host']
        port = algo_detail_info['port']
        data=algo_detail_info['remark']
        tags=algo_detail_info['tags']
        token=algo_detail_info['token']
        funcslist_str=algo_detail_info['funcslist']
        bind_address2 = "http://%s:%s" % ('0.0.0.0', int(port))#get_myip()
        client = Client(bind_address2,auth_token=token)
        data=msg_info['data']
        #print input_data,type(input_data),'input_data'
        #base_algo_info=BASE_INFO.format(ip=bind_address2, token=token)
        #eval(base_algo_info)
        if '|' in data:
            datalist=data.split("|")
        else:
            datalist=[data]

        infer_info_dict={}
        funcs_info=load_functions(funcslist_str.split(","))
        for inter in range(len(funcs_info)):
            try:
                datainfo=datalist[inter]
                if len(datainfo)<1:
                    datainfo=None
            except:
                datainfo=None
            #print 'datainfo',datainfo,type(datainfo)
            input_data = eval(datainfo)
      
            result= eval(INFER_INFO.format(function_name=funcs_info[inter]))
            infer_info_dict[funcs_info[inter].strip()]=result
        #infer_algo_info='\n'.join(infer_info_list)
        #python_client_info=base_algo_info+infer_algo_info
        
        
        infer=INFER_INFO.format(data=datainfo,function_name=funcs_info[inter])
        #result=client.pred(**input_data)
        #print 'result',result
        bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        if not bRet:
            return False, sRet
        #if not is_admin:
        #    return False, 'No permission do run example'
        bRet, user_id =  HjsUser.get_user_uid(self.get_user_name())
        if not bRet:
            return False, user_id
        #print 'msg_info = get_req_all_param()',msg_info 
        #print 'comments;;;;;;;',msg_user_list
        return True,infer_info_dict#json.dumps(infer_info_dict)

    def GET(self):
        if not self.check_login():
            return self.make_error("user not login")

        bRet, sRet = self.process(self._deal_run_api_example)
        if not bRet:
            Log.err("deal_run_api_example: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(sRet)  

import yaml
from Arthur.core.utils.misc_functions import Commands
class ViewApiRunApi(ViewBase):
    def __init__(self):
        self.commands=Commands()
        self._rDict = {
            "modelInfo": {'n': "modelInfo", 't': str, 'v': None},
            "dataInfo": {'n': "dataInfo", 't': str, 'v': None},
        }

    def _check_param(self):
        bRet, sRet = super(ViewApiRunApi, self)._check_param()
        if not bRet:
            return False, sRet
        return True, None

    def _deal_run_api_example(self):
        
        bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        if not bRet:
            return False, sRet
        if not is_admin:
            return False, 'No permission to do this'
        _bRet,uId=HjsUser.get_user_uid(self.get_user_name())
        if not _bRet:
            return False, uId       

        #获取api信息
        #print type(self.modelInfo), self.modelInfo,self.dataInfo,'infoooooo'
        modelInfo=yaml.safe_load(self.modelInfo)
        dataInfo=yaml.safe_load(self.dataInfo)
        #dataInfo=json.loads(dataInfo)
        #print type(modelInfo),modelInfo,'modelInfo'
        modelInfo=json.loads(modelInfo)
        username= modelInfo['username']
        proJectname= modelInfo['algoname']
        _bRet, uId = HjsUser.get_user_uid(username)
        if not _bRet:
            return False,uId
        _bRet_,algo_detail_info= ArthurService.algo_proj_info(uId,proJectname)
        host=algo_detail_info['host']
        port = algo_detail_info['port']
        data=algo_detail_info['remark']
        tags=algo_detail_info['tags']
        token=algo_detail_info['token']
        funcslist_str=algo_detail_info['funcslist']
        bind_address2 = "http://%s:%s" % ('0.0.0.0', int(port))#get_myip()
        client = Client(bind_address2,auth_token=token)
        data=self.dataInfo#['data']
        #print input_data,type(input_data),'input_data'
        #base_algo_info=BASE_INFO.format(ip=bind_address2, token=token)
        #eval(base_algo_info)
        if '|' in data:
            datalist=data.split("|")
        else:
            datalist=[data]

        infer_info_dict={}
        funcs_info=load_functions(funcslist_str.split(","))
        for inter in range(len(funcs_info)):
            try:
                datainfo=datalist[inter]
                if len(datainfo)<1:
                    datainfo=None
            except:
                datainfo=None
            input_data = eval(datainfo)
            input_data=json.loads(input_data)
            print input_data,type(input_data)
            result= eval(INFER_INFO.format(function_name=funcs_info[inter]))
            infer_info_dict[funcs_info[inter].strip()]=result
            
            #end_point=bind_address2+'/%s'%funcInfo
            #shell_cmd = ['curl', '-H', "Authorization: Token %s"%token,'-d','%s'%json.dumps(datainfo),end_point]
            #command_run = self.commands.run_cmd(shell_cmd)
            #result= eval(INFER_INFO.format(function_name=funcs_info[inter]))
            #if command_run['status']:
            #    print 'fffffff',command_run['output']
            ##    infer_info_dict[funcs_info[inter].strip()]=command_run['output']
            #else:
            #    return False,'run api wrong!'

        
        #infer=INFER_INFO.format(data=datainfo,function_name=funcs_info[inter])
    
        bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        if not bRet:
            return False, sRet
        #if not is_admin:
        #    return False, 'No permission do run example'
        bRet, user_id =  HjsUser.get_user_uid(self.get_user_name())
        if not bRet:
            return False, user_id
 
        return True,infer_info_dict#json.dumps(infer_info_dict)


    def POST(self):
        bRet, sRet = self.check_login()
        if not bRet:
            return web.seeother("/login")
        bRet, sRet = self.process(self._deal_run_api_example)
        if not bRet:
            Log.err("deal_run_api_example: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(sRet)