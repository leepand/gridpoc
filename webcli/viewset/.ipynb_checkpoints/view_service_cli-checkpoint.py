# -*- coding: UTF-8 -*-

# author: leepand
# time: 2019-02-21
# desc: model predict

from Arthur.core.entities.bean.hjs_user import HjsUser
from Arthur.core.entities.dao.hjs_user_dao import HjsUserDao

from Arthur.core.entities.bean.Arthur_service import ArthurService
from view_base import ViewBase
from Arthur.core.entities.base.bs_log import Log
from Arthur.core.controller.apimanager.apiproxy import RemoteAPIController

import yaml
import web
import json

#Add 2019-02-21
class ViewApiServiceCli(ViewBase):
    def __init__(self):
        self._rDict = {
            "servicename": {'n': "servicename", 't': str, 'v': ""},
            "algoname": {'n': "algoname", 't': str, 'v': ""},
            "username": {'n': "username", 't': str, 'v': ""},            
        }

    def _check_param(self):
        bRet, sRet = super(ViewApiServiceCli, self)._check_param()
        if not bRet:
            return False, sRet
        return True, None

    def _deal_run_api_example(self):
        #获取api信息
        response = {"status_code": 200}
        projectName = self.servicename
        token = self.token
        #funcName = self.algoname
        if self.username:
            username= self.username
            _bRet, uId = HjsUser.get_user_uid(username)
            if not _bRet:
                return False,uId
            _bRet_,algo_detail_info= ArthurService.algo_proj_info(uId,projectName)
        else:
            _bRet_,algo_detail_info= ArthurService.algo_proj_info_noid(projectName)

        host=algo_detail_info['host']
        port = algo_detail_info['port']
        funcName2 =algo_detail_info['funcslist']
        funcName=funcName2.split(',')[0].split('.')[1]
        bind_address = "%s:%s" % ('0.0.0.0', str(port))#get_myip()
        fn = RemoteAPIController()
        response = fn.get_completed_requests(funcName,bind_address)
            
        return True,response

    def POST(self):
        bRet, sRet = self.check_login()
        if not bRet:
            return web.seeother("/login")
        bRet, sRet = self.process(self._deal_run_api_example)
        if not bRet:
            Log.err("deal_run_api_example: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(sRet)
    
    
#Add 2019-02-21
class ViewApiServiceCli22(ViewBase):
    def __init__(self):
        self._rDict = {
            #"modelInfo": {'n': "modelInfo", 't': str, 'v': ""},
            #"dataInfo": {'n': "dataInfo", 't': str, 'v': ""},
            "servicename": {'n': "servicename", 't': str, 'v': ""},
            "token": {'n': "token", 't': str, 'v': ""},
            "algoname": {'n': "algoname", 't': str, 'v': ""},
            "req_data": {'n': "req_data", 't': str, 'v': ""},
            "username": {'n': "username", 't': str, 'v': ""},
            "request_type": {'n': "request_type", 't': str, 'v': ""},
            
        }

    def _check_param(self):
        bRet, sRet = super(ViewApiServiceCli, self)._check_param()
        if not bRet:
            return False, sRet
        return True, None

    def _deal_run_api_example(self):
        #获取api信息
        response = {"status_code": 200}
        #modelInfo={"servicename":"new_year_exp","algoname":"fib","token":"20bf7679146eaef99136cde84ccc1eba"}
        #self.modelInfo =modelInfo
        #self.dataInfo={"n":10}
        print self.servicename,type(self.servicename),self.req_data,type(self.req_data)
        projectName = self.servicename
        token = self.token
        funcName = self.algoname
        if self.username:
            username= self.username
            _bRet, uId = HjsUser.get_user_uid(username)
            if not _bRet:
                return False,uId
            _bRet_,algo_detail_info= ArthurService.algo_proj_info(uId,projectName)
        else:
            _bRet_,algo_detail_info= ArthurService.algo_proj_info_noid(projectName)

        host=algo_detail_info['host']
        port = algo_detail_info['port']
        bind_address = "%s:%s" % ('0.0.0.0', int(port))#get_myip()
        fn = RemoteAPIController()
        if self.req_data:
            req_data=json.loads(self.req_data)
            print req_data,type(req_data),'req_data',bind_address,funcName,token
            response = fn.post_data(req_data,bind_address,funcName,token)
        if self.request_type=="cnt":
            response = fn.get_completed_requests(funcName,bind_address)
            
        return True,response

    def POST(self):
        #bRet, sRet = self.check_login()
        #if not bRet:
        #    return web.seeother("/login")
        bRet, sRet = self.process(self._deal_run_api_example)
        if not bRet:
            Log.err("deal_run_api_example: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(sRet)