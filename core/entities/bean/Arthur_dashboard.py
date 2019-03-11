# -*- coding: UTF-8 -*-
# author: leepand
# time: 2019-01-07
# desc: Dashboard 数据展示

#update 2019-01-25
from Arthur.core.entities.base.bs_time import get_cur_day
from Arthur.core.entities.dao.hjs_user_dao import HjsUserDao
from Arthur.core.entities.bean.hjs_user import HjsUser
from Arthur.core.entities.dao.Arthur_service_dao import *
import datetime


class ArthurDashboard:

    @staticmethod
    def _get_user_data():
        bRet, user_cnt = HjsUserDao.query_user_count()
        if not bRet: user_cnt = 0


        return  {
            "user_cnt": user_cnt
        }

    @staticmethod
    def _get_algo_data(userName):
        my_priv2=''
        u_status,uId = HjsUser.get_user_uid(userName)
        bRet1, all_algo_cnt=ArthurAlgoDao.query_node_count(status=None, search=None)
        bRet2, online_algo_cnt = ArthurAlgoDao.query_node_count(status='normal', search=None)
        bRet3, online_today_algo_cnt = ArthurAlgoDao.query_node_cnt_by_date(status='normal', tg_date=get_cur_day(0, format="%Y-%m-%d %H:%M:%S"))
        bRet4, offline_today_algo_cnt = ArthurAlgoDao.query_node_cnt_by_date(status='stop', tg_date=get_cur_day(0, format="%Y-%m-%d %H:%M:%S"))
        bRet5, my_algo_cnt = ArthurAlgoDao.query_node_count_by_uid(uId,status=None, search=None)
        bRet7, my_online_algo_cnt = ArthurAlgoDao.query_node_count_by_uid(uId,status='normal', search=None)
        bRet6, my_priv = HjsUser.user_info(uId)
        if not bRet1: all_algo_cnt = 0
        if not bRet2: online_algo_cnt = 0
        if not bRet3: online_today_algo_cnt = 0
        if not bRet4: offline_today_algo_cnt = 0 
        if not bRet5: my_algo_cnt = 0
        if not bRet6: my_priv.priv = 1

        return  {
            "all_algo_cnt": all_algo_cnt,
            "online_algo_cnt" : online_algo_cnt,
            "online_today_algo_cnt":online_today_algo_cnt,
            "offline_today_algo_cnt":offline_today_algo_cnt,
            "my_algo_cnt":my_algo_cnt,
            "my_online_algo_cnt":my_online_algo_cnt,
            "my_priv":my_priv.priv
        }


    @staticmethod
    def data_show(userName):
        datas = {
            "dt_user": ArthurDashboard._get_user_data(),  
            "dt_algo_ser":ArthurDashboard._get_algo_data(userName)
        }
        
        return True, datas

if __name__ == "__main__":
    print ArthurDashboard.data_show('leepand6')
    #bRet, sRet = HjsIndex.data_show('admin')

    #print '>>>> ', sRet

    #print HjsIndex._get_expire_order()