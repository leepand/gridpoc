# -*- coding: UTF-8 -*-

# author: leepand
# time: 2018-11-27
# desc: service处理逻辑 


#update 2019-01-25
from web.utils import storage
from Arthur.core.entities.base.bs_time import get_cur_day
from Arthur.core.entities.bean.hjs_user import HjsUser
from Arthur.core.entities.dao.hjs_user_dao import HjsUserDao
from Arthur.core.entities.dao.Arthur_service_dao import ArthurAlgoDao
from Arthur.core.entities.dao.Arthur_ps_service_dao import ArthurServicePauseDao
from Arthur.core.utils.token_util import Connector
from Arthur.core.entities.base.bs_util import Page
from Arthur.core.entities.dao.Arthur_serviceTags_dao import ArthurServTagsDao
from Arthur.core.entities.base.bs_log import Log



class ServiceStatus:
    ALL    = 'all'
    STOP   = 'stop'
    NORMAL = 'normal'
    DELETE = 'delete'
    NOTPUBLISH = 'notpublish'


class ArthurService:

    @staticmethod
    def _page_data2(data_list, status, search, page):
        if not isinstance(page, Page):
            return data_list
        return {
            "page_count": page.page_count,
            "current": page.page_index,
            "service_list": data_list,
            "service_query": {"status": status, "search": search}
        }
    #update 2019-02-19
    @staticmethod
    def _page_data(data_list, status, search):
        #if not isinstance(page, Page):
        #    return data_list
        return {
            "page_count": 1,
            "current": 1,
            "service_list": data_list,
            "service_query": {"status": status, "search": search}
        }
    @staticmethod
    def service_zoo_list(page=1, length=1, status=None, search=None):
        allow_status = [ServiceStatus.ALL, ServiceStatus.NORMAL, ServiceStatus.STOP, ServiceStatus.DELETE,ServiceStatus.NOTPUBLISH]
        if status and (status not in allow_status):
            return False, 'param(status) not define'

        #bRet, count = ArthurAlgoDao.query_node_count(status, search)
        #if not bRet:
        #    return False, count

        #pg = Page(count, page, length)
        #bRet, sRet = ArthurAlgoDao.query_node_list(pg.offset, pg.limit, status, search)
        bRet, sRet = ArthurAlgoDao.query_node_list(status)
        if not bRet:
            Log.err('list algo fail: %s' % str(sRet))
            return False, sRet
        if len(sRet) == 0:
            return True, None
        
        algoList = list()
        for item in sRet:
            #_bRet,uName=HjsUser.user_info(item['uid'])效率太低 要每个uid都去查一遍
            #if not _bRet:
            #    uName=''
            #user_name= uName.username
            algo_info = storage()
            algo_info.aid = int(item['aid'])
            algo_info.uid = int(item['uid'])
            algo_info.user_name =str(item['username'])
            algo_info.algoname = item['algoname']
            algo_info.algodesc = item['algodesc']
            algo_info.atype = item['atype'];
            algo_info.algo_tm = str(item['algo_tm'])[:10]
            algo_info.token = item['token']
            algo_info.host = item['host']
            algo_info.port = item['port']
            algo_info.field = item['field']
            #order_info.start_tm = str(item['start_tm'])
            #order_info.end_tm = str(item['end_tm'])
            #order_info.amount = item['amount']
            #order_info.cash = item['cash']
            algo_info.status = item['status']
            algo_info.remark = item['remark']
            algo_info.insert_tm = str(item['insert_tm'])#[2:16]
            algoList.append(algo_info)
        return True, ArthurService._page_data(algoList, status, search)
    @staticmethod
    def service_user_list(uid,page=None, length=None, status=None, search=None):
        allow_status = [ServiceStatus.ALL, ServiceStatus.NORMAL, ServiceStatus.STOP, ServiceStatus.DELETE,ServiceStatus.NOTPUBLISH]
        if status and (status not in allow_status):
            return False, 'param(status) not define'

        #bRet, count = ArthurAlgoDao.query_node_count_by_uid(uid,status, search)
        #if not bRet:
        #    return False, count

        #pg = Page(count, page, length)
        #bRet, sRet = ArthurAlgoDao.query_node_list_by_uid(uid,pg.offset, pg.limit, status, search)
        bRet, sRet = ArthurAlgoDao.query_node_list_by_uid(uid, status)
        if not bRet:
            Log.err('list algo fail: %s' % str(sRet))
            return False, sRet
        if len(sRet) == 0:
            return True, None
        
        algoList = list()
        
        for item in sRet:
            #_bRet,uName=HjsUser.user_info(item['uid'])#太耗时
            #if not _bRet:
            #     uName=''
            #user_name= uName.username
            algo_info = storage()
            algo_info.aid = int(item['aid'])
            algo_info.uid = int(item['uid'])
            algo_info.user_name =str(item['username'])
            algo_info.algoname = item['algoname']
            algo_info.algodesc = item['algodesc']
            algo_info.atype = item['atype'];
            algo_info.algo_tm = str(item['algo_tm'])[:10]
            algo_info.token = item['token']
            algo_info.host = item['host']
            algo_info.port = item['port']
            algo_info.field = item['field']
            #order_info.start_tm = str(item['start_tm'])
            #order_info.end_tm = str(item['end_tm'])
            #order_info.amount = item['amount']
            #order_info.cash = item['cash']
            algo_info.status = item['status']
            algo_info.remark = item['remark']
            algo_info.insert_tm = str(item['insert_tm'])#[2:16]
            algoList.append(algo_info)
        return True, ArthurService._page_data(algoList, status, search)
    #增加 2019-01-31: 用于获取某tag下的service list/TODO:标签聚类
    @staticmethod
    def service_tag_list(search=None):
        bRet, tag_services_list = ArthurServTagsDao.query_node_list_by_tag(search=search)
        if not bRet:
            Log.err('Tag algo list fail: %s' % str(sRet))
            return False, tag_services_list
        if len(tag_services_list) == 0:
            return True, None
        
        algoList = list()
        
        for item in tag_services_list:
            #_bRet,uName=HjsUser.user_info(item['uid'])
            #if not _bRet:
            #     uName=''
            #user_name= uName.username
            algo_info = storage()
            algo_info.aid = int(item['aid'])
            algo_info.uid = int(item['uid'])
            algo_info.user_name =str(item['username'])
            algo_info.algoname = item['algoname']
            algo_info.algodesc = item['algodesc']
            algo_info.atype = item['atype'];
            algo_info.algo_tm = str(item['algo_tm'])[:10]
            algo_info.token = item['token']
            algo_info.host = item['host']
            algo_info.port = item['port']
            algo_info.field = item['field']
            #order_info.start_tm = str(item['start_tm'])
            #order_info.end_tm = str(item['end_tm'])
            #order_info.amount = item['amount']
            #order_info.cash = item['cash']
            algo_info.status = item['status']
            algo_info.remark = item['remark']
            algo_info.insert_tm = str(item['insert_tm'])#[2:16]
            algoList.append(algo_info)
        return True, algoList
    
    #增加2019-01-10:获取用户收藏算法服务
    @staticmethod
    def service_user_list_filter(uid,algoname,page=1, length=None, status=None, search=None):
        allow_status = [ServiceStatus.ALL, ServiceStatus.NORMAL, ServiceStatus.STOP, ServiceStatus.DELETE,ServiceStatus.NOTPUBLISH]
        if status and (status not in allow_status):
            return False, 'param(status) not define'

        #bRet, count = ArthurAlgoDao.query_node_count_by_uid(uid,status, search)
        #if not bRet:
        #    return False, count

        #pg = Page(count, page, length)
        #bRet, sRet = ArthurAlgoDao.query_node_list_by_uid(uid,pg.offset, pg.limit, status, search)
        bRet, sRet = ArthurAlgoDao.query_node_list_by_uid(uid, status)
        if not bRet:
            Log.err('list algo fail: %s' % str(sRet))
            return False, sRet
        if len(sRet) == 0:
            return True, None
        
        algoList = list()
        
        for item in sRet:
            if algoname==item['algoname'] and item['status']=='normal': 
                #_bRet,uName=HjsUser.user_info(item['uid'])
                #if not _bRet:
                #     uName=''
                #user_name= uName.username
                algo_info = storage()
                algo_info.aid = int(item['aid'])
                algo_info.uid = int(item['uid'])
                #algo_info.user_name =str(user_name)
                algo_info.user_name =str(item['username'])
                algo_info.algoname = item['algoname']
                algo_info.algodesc = item['algodesc']
                algo_info.atype = item['atype'];
                algo_info.algo_tm = str(item['algo_tm'])[:10]
                algo_info.token = item['token']
                algo_info.host = item['host']
                algo_info.port = item['port']
                algo_info.field = item['field']
                algo_info.status = item['status']
                algo_info.remark = item['remark']
                algo_info.insert_tm = str(item['insert_tm'])#[2:16]
                algoList.append(algo_info)
        return True, ArthurService._page_data(algoList, status, search)

    @staticmethod
    def service_today(status='normal', days=0):
        tg_date = get_cur_day(days, format="%Y-%m-%d %H:%M:%S")#"%Y-%m-%d %H:%M:%S" %Y-%m-%d
        bRet, algoList_tmp = ArthurAlgoDao.query_node_by_date(status, tg_date)
        if not bRet:
            return False, algoList
        
        bRet, sRet = ArthurServicePauseDao.query_node_by_date(tg_date)
        if not bRet:
            return False, sRet
        
        pauseList = list()
        for item in sRet:
            if item.has_key('aid'):
                pauseList.append(item['aid'])

        algoList = list()
        for item in algoList_tmp:
            if item['aid'] in pauseList: continue
            
            algo_info = storage()
            algo_info.aid = int(item['aid'])
            algo_info.uid = int(item['uid'])
            algo_info.algoname = item['algoname']
            algo_info.algodesc = item['algodesc']
            algo_info.atype = item['atype']
            algo_info.algo_tm = str(item['algo_tm'])
            algo_info.status = item['status']
            algo_info.remark = item['remark']
            algo_info.token = item['token']
            algo_info.host = item['host']
            algo_info.port = item['port']
            algo_info.field = item['field']
            #bRet, custom_info = HjsCustomDao.query_node_by_cid(order_info.cid)
            #order_info.address = custom_info['address'] if bRet else '--'
            #order_info.phone = custom_info['phone'] if bRet else '--'
            #order_info.ctype = custom_info['ctype'] if bRet else '--'

            algoList.append(algo_info)

        return True, algoList



    #(uId, algoname,algodesc,token,pyfile,funcslist,tags,field,host,port,atype, algo_tm,is_email, remark, get_cur_time())
    @staticmethod
    def service_add(uId, algoname, algodesc,opertype, pyfile,funcslist,tags,field,host,port,
                   algo_tm,is_email, remark):
        atype='REST'
        Token_gen=Connector.encrypt_token( 1, str(uId), 'session_token')
        Token_info=Token_gen['token']
        return ArthurAlgoDao.insert_node(uId, algoname, algodesc,opertype,Token_info, pyfile,funcslist,tags,field,host,port,atype,
                   algo_tm,is_email, remark)


    #@staticmethod
    #def order_update(oId, otype, order_tm, start_tm, end_tm, amount, cash, status, remark):
    #    return HjsOrderDao.update_node(oId, otype, order_tm, start_tm, end_tm, amount, cash, status, remark)
    #add 2018-12-29增加对服务状态的更新（发布时）
    @staticmethod
    def algo_publish_status_update(aId, status):
        return ArthurAlgoDao.update_node_status(aId, status)
    @staticmethod
    def order_update(oId, otype, order_tm, status,remark):
        return HjsOrderDao.update_node(oId, otype, order_tm, status,remark)

    @staticmethod
    def order_del(oId):
        return HjsOrderDao.update_node_status(oId, 'stop')

    #add 2018-12-29
    @staticmethod
    def algo_info(aId):
        bRet, sRet = ArthurAlgoDao.query_node_by_aid(aId)
        if not bRet:
            return False, sRet
        
        algo_info = storage()
        algo_info.aid = int(sRet['aid'])
        algo_info.uid = int(sRet['uid'])
        algo_info.algoname = sRet['algoname']
        algo_info.status = sRet['status']
        algo_info.port = str(sRet['port'])[:10]
        #order_info.start_tm = str(sRet['start_tm'])
        #order_info.end_tm = str(sRet['end_tm'])
        #order_info.amount = sRet['amount']
        #order_info.cash = sRet['cash']
        algo_info.host = sRet['host']
        algo_info.token = sRet['token']
        algo_info.funcslist = sRet['funcslist']
        return True, algo_info
    #add 2019-01-03
    @staticmethod
    def algo_proj_info(uId,AlgoName):
        bRet, sRet = ArthurAlgoDao.query_node_by_proj_uid(uId,AlgoName)
        if not bRet:
            return False, sRet
        
        algo_info = storage()
        algo_info.aid = int(sRet['aid'])
        algo_info.uid = int(sRet['uid'])
        algo_info.algoname = sRet['algoname']
        algo_info.algodesc = sRet['algodesc']
        algo_info.status = sRet['status']
        algo_info.tags = sRet['tags']
        algo_info.field = sRet['field']
        algo_info.port = str(sRet['port'])
        #order_info.start_tm = str(sRet['start_tm'])
        #order_info.end_tm = str(sRet['end_tm'])
        #order_info.amount = sRet['amount']
        #order_info.cash = sRet['cash']
        algo_info.algo_tm = str(sRet['algo_tm'])
        algo_info.host = sRet['host']
        algo_info.token = sRet['token']
        algo_info.funcslist = sRet['funcslist']
        algo_info.remark = sRet['remark']
        return True, algo_info
    #add 2019-02-21
    @staticmethod
    def algo_proj_info_noid(AlgoName):
        bRet, sRet = ArthurAlgoDao.query_node_by_proj(AlgoName)
        if not bRet:
            return False, sRet
        
        algo_info = storage()
        algo_info.aid = int(sRet['aid'])
        algo_info.uid = int(sRet['uid'])
        algo_info.algoname = sRet['algoname']
        algo_info.algodesc = sRet['algodesc']
        algo_info.status = sRet['status']
        algo_info.tags = sRet['tags']
        algo_info.field = sRet['field']
        algo_info.port = str(sRet['port'])
        #order_info.start_tm = str(sRet['start_tm'])
        #order_info.end_tm = str(sRet['end_tm'])
        #order_info.amount = sRet['amount']
        #order_info.cash = sRet['cash']
        algo_info.algo_tm = str(sRet['algo_tm'])
        algo_info.host = sRet['host']
        algo_info.token = sRet['token']
        algo_info.funcslist = sRet['funcslist']
        algo_info.remark = sRet['remark']
        return True, algo_info

if __name__ == "__main__":
    
    #print ArthurService.service_today() 
    #print ArthurService.service_zoo_list(1, 20, status=None, search=None) 
    #print ArthurService.service_user_list(35,1, 20, status=None, search=None)
    print ArthurService.algo_info(1)
    #print HjsOrder.order_info(2003)
    #cId, otype, order_tm, start_tm, end_tm, amount, cash, remark
    #orfa={"cId": 1,"otype": "A", "order_tm": "2018-03-12 12:23:11","remark":"need 20"}
    #print HjsOrder.order_add(**orfa)
   # print HjsOrder.order_today()
    #print ArthurService.service_user_list(page, length, status=None, search=None)

    #订单需要与客户绑定才能插入
    pass
