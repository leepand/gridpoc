# -*- coding: UTF-8 -*-
# author: leepand
# time: 2019-01-08
# desc: Algo 数据展示(my/other/zoo)

#update 2019-01-25

import datetime
from operator import itemgetter 
from Arthur.core.entities.bean.Arthur_service import ArthurService
from Arthur.core.entities.dao.Arthur_AlgoStar_dao import ArthurAlgoStarDao
#from Arthut.core.entities.dao.Arthur_serviceTags_dao import ArthurServTagsDao

class ArthurAlgoList:

    @staticmethod
    def _get_algolist_byuid(uId,service_status):
        #增加收藏的算法服务
        bRet,uid_algouid_list = ArthurAlgoStarDao.query_algouid_by_uidstar(uId)
        my_star_algo_list_all=[]
        my_star_algo_list=[]
        my_star_algo_list_dict=None
        if len(uid_algouid_list)>0:
            for algouid_algoname_dict in uid_algouid_list:
                algouid=algouid_algoname_dict['algouid']
                algoname = algouid_algoname_dict['algoname']
                #过滤掉自己收藏自己的算法，避免重复
                if int(algouid)-int(uId)==0:
                    continue
                bRet, my_star_algo_list_dict = ArthurService.service_user_list_filter(algouid,algoname,page=1,length=1000, status='normal', search=None)
                #print 'my_star_algo_list_dict',my_star_algo_list_dict
                if not bRet: my_star_algo_list = []
                if my_star_algo_list_dict is not None and "service_list" in my_star_algo_list_dict:
                    my_star_algo_list= my_star_algo_list_dict['service_list']
                else:
                    my_star_algo_list=[]
                my_star_algo_list_all.extend(my_star_algo_list)
    
        bRet, my_algo_list_dict = ArthurService.service_user_list(uId,page=1,length=1000, status=service_status, search=None)
        if not bRet: my_algo_list = []
        if my_algo_list_dict is not None and "service_list" in my_algo_list_dict:
            my_algo_list= my_algo_list_dict['service_list']
        else:
            my_algo_list=[]
        my_algo_list.extend(my_star_algo_list_all)
        my_algo_list_new=my_algo_list
        return  {
            "algo_list": my_algo_list_new
        }
    
    @staticmethod
    def _get_algolist_zoo():
        bRet, algo_list_zoo = ArthurService.service_zoo_list(page=1,length=1000, status='normal', search=None)
        if not bRet: algo_list_zoo = []
        if  algo_list_zoo is not None and "service_list" in algo_list_zoo:
            serviceList=algo_list_zoo['service_list']
            #serviceList_bystar = sorted(serviceList,key = itemgetter('star_cnt'),reverse = True)
            serviceList_bytime = sorted(serviceList,key = itemgetter('insert_tm'),reverse = True)

        else:
            serviceList=[]
            serviceList_bystar=[]
            serviceList_bytime=[]
        return {
                "algo_list": serviceList,#serviceList
                "algo_list_bytime":serviceList_bytime}
    @staticmethod
    def _get_tag_services(tag):
        bRet, tag_services_list = ArthurService.service_tag_list(search=tag)
        if not bRet: tag_services_list = []
        if  len(tag_services_list)>0:
            serviceList_bytime = sorted(tag_services_list,key = itemgetter('insert_tm'),reverse = True)

        else:
            tag_services_list=[]
            serviceList_bytime=[]
        return {
                "algo_list": tag_services_list,#serviceList
                "algo_list_bytime":serviceList_bytime}


    @staticmethod
    def data_show(uId,query_type,tag,service_status='normal'):
        if query_type=='zoo':
            if tag=="NonetagQuery":#myservice_layerui
                datas = {
                    "dt_algo_list":ArthurAlgoList._get_algolist_zoo()
                }
            else:
                datas = {
                    "dt_algo_list":ArthurAlgoList._get_tag_services(tag)
                }
        else:
            datas = {
                "dt_algo_list":ArthurAlgoList._get_algolist_byuid(uId,service_status)
            }
        return True, datas
    @staticmethod
    def algo_list_forautocomplete():
        bRet, sRet = ArthurAlgoList.data_show(1,'zoo')
        new_serv_list=[]
        try:
            for _inter in sRet['dt_algo_list']['algo_list']:
                new_serv_list.append(_inter['algoname'])
        except:
            pass
        return True,new_serv_list

if __name__ == "__main__":

    bRet, sRet = ArthurAlgoList.data_show(1,'zoo')

    print '>>>> ', sRet

    #print HjsIndex._get_expire_order()
