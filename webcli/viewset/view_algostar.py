# -*- coding: UTF-8 -*-

# author: leepand
# time: 2019-01-09
# desc: star and thumb

from view_base import ViewBase,render,render_without_base
from Arthur.core.entities.bean.hjs_user import HjsUser
from Arthur.core.entities.bean.Arthur_service import ArthurService
from Arthur.core.entities.dao.Arthur_msg_dao import ArthurMsg
from Arthur.core.utils.token_util import Connector
from Arthur.core.entities.dao.hjs_user_dao import HjsUserDao
from arthur_utils.file_process import FileStore
from arthur_utils.file_utils import list_subdirs
from Arthur.core.entities.base.bs_log import Log

from Arthur.core.entities.dao.Arthur_AlgoStar_dao import ArthurAlgoStarDao 
from Arthur.core.entities.bean.Arthur_Service_Stared import ArthurServiceStared
import os,sys
import time
#迁移至ViewApiServList类中，将数据整合到algo_list_info
"""class ViewApiAlgoStarGet(ViewBase):
    def __init__(self):
        self._rDict = { 
            "viewdUser": {'n': "viewdUser", 't': str, 'v': None},
            "algoname": {'n': "algoname", 't': str, 'v': None},
            "algoUser": {'n': "algoUser", 't': str, 'v': None}
        }
    
    def _check_param(self):
        bRet, sRet = super(ViewApiAlgoStarGet, self)._check_param()
        if not bRet:
            return False, sRet
        return True, None

    def _deal_algo_star_get(self):   
        if self.viewdUser=='myself':
            uName= self.get_user_name()   
        else:
            uName = self.viewdUser
        _bRet,uId=HjsUser.get_user_uid(uName)
        if not _bRet:
            return False, uId
        _bRet,algouId=HjsUser.get_user_uid(self.algoUser)
        if not _bRet:
            return False, algouId
        _br, algo_star_info_list = ArthurAlgoStarDao.query_node_by_uid_algo_algouid(uId,algouId, self.algoname)
        
        if len(algo_star_info_list)<1:
            print 'ddddd',True,{'star_status':'nostar','star_cnt':0}
            return True,{'star_status':'nostar','star_cnt':0}
        else:
            status= algo_star_info_list[0]['star_status']
            cnt= algo_star_info_list[0]['star_cnt']
            return True,{'star_status':status,'star_cnt':cnt}

    def POST(self):
        bRet, sRet = self.check_login()
        if not bRet:
            return web.seeother("/login")
        bRet, sRet = self.process(self._deal_algo_star_get)
        if not bRet:
            Log.err("deal_algo_star_get: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(sRet)
"""    
class ViewApiAlgoStarUpdate(ViewBase):
    def __init__(self):
        self._rDict = { 
            "viewdUser": {'n': "viewdUser", 't': str, 'v': None},
            "algoname": {'n': "algoname", 't': str, 'v': None},
            "algoUser": {'n': "algoUser", 't': str, 'v': None},
            "star_status": {'n': "star_status", 't': str, 'v': None},
            "star_cnt": {'n': "star_cnt", 't': int, 'v': None}          
        }
    
    def _check_param(self):
        bRet, sRet = super(ViewApiAlgoStarUpdate, self)._check_param()
        if not bRet:
            return False, sRet
        return True, None

    def _deal_algo_star_update(self):     
        if self.algoUser=='myself':
            algoName= self.get_user_name()   
        else:
            algoName = self.algoUser
        #获取登陆者id
        _bRet,uId=HjsUser.get_user_uid(self.viewdUser)
        if not _bRet:
            return False, uId
        #print self.algoUser,'self.algoUser'
        #获取算法发布者ID
        _bRet,algouId=HjsUser.get_user_uid(algoName)
        if not _bRet:
            return False, algouId
        _br, algo_star_info_list = ArthurAlgoStarDao.query_node_by_uid_algo_algouid(uId,algouId, self.algoname)
        print 'algo_star_info_list',algo_star_info_list
        if len(algo_star_info_list)<1:
            bRet, sRet = ArthurAlgoStarDao.insert_node(algouId, uId,self.algoname,self.star_status,thumb_status=None)
        else:
            bRet, sRet = ArthurAlgoStarDao.update_node_status(algouId, uId,self.algoname,self.star_status,thumb_status=None)
        return True,True

    def POST(self):
        bRet, sRet = self.check_login()
        if not bRet:
            return web.seeother("/login")
        bRet, sRet = self.process(self._deal_algo_star_update)
        if not bRet:
            Log.err("deal_algo_star_update: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(ViewBase.RetMsg.MSG_SUCCESS)
    

from Arthur.core.controller.apimanager.apiproxy import RemoteAPIController
    
class ViewApiStaredInfo(ViewBase):
    def __init__(self):
        self._rDict = { 
            "username": {'n': "username", 't': str, 'v': None},
            "algoname": {'n': "algoname", 't': str, 'v': None},      
        }
    
    def _check_param(self):
        bRet, sRet = super(ViewApiStaredInfo, self)._check_param()
        if not bRet:
            return False, sRet
        return True, None

    def _deal_stared_info(self):   
        _bRet,algouId=HjsUser.get_user_uid(self.username)
        _bRet,stared_info = ArthurServiceStared.serviceStaredInfo(algouId,self.algoname)
        if not _bRet:
            return False,'wrong stared info get'
        #begin of new add(request-cnt)
        response = {"status_code": 200}
        projectName = self.algoname
        if self.username:

            _bRet_,algo_detail_info= ArthurService.algo_proj_info(algouId,projectName)
        else:
            _bRet_,algo_detail_info= ArthurService.algo_proj_info_noid(projectName)

        host=algo_detail_info['host']
        port = algo_detail_info['port']
        funcName2 =algo_detail_info['funcslist']
        funcName=funcName2.split(',')[0].split('.')[1]
        bind_address = "%s:%s" % ('0.0.0.0', str(port))#get_myip()
        fn = RemoteAPIController()
        response = fn.get_completed_requests(funcName,bind_address)
        #print (response,type(response))
        #end of new add(request-cnt)
        if "body" not in response:
            response["body"]=0
        return True,{"stared_info":stared_info,"request_cnt":response}

    def POST(self):
        bRet, sRet = self.check_login()
        if not bRet:
            return web.seeother("/login")
        bRet, sRet = self.process(self._deal_stared_info)
        if not bRet:
            Log.err("deal_stared_info: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(sRet)