# -*- coding: UTF-8 -*-

# author: leepand
# time: 2019-01-31
# desc: service被点赞者信息处理 
from Arthur.core.entities.bean.hjs_user import HjsUser
from Arthur.core.entities.dao.Arthur_AlgoStar_dao import ArthurAlgoStarDao

class ArthurServiceStared:
    @staticmethod
    def serviceStaredInfo(algouid,algoname):
        _bRet,staredServiceList=ArthurAlgoStarDao.query_star_list_by_algo(algouid,algoname,offset=0, limit=1000)
        stared_cnt=len(staredServiceList)
        stared_user_infoList = []
        if stared_cnt>0:
            i=0
            for _iter in staredServiceList:
                if i>10:#只展示10条
                    continue
                uId = _iter['uid']
                _bRet,userInfo=HjsUser.user_info(uId)
                username = userInfo.username
                stared_user_infoList.append({"userName":userInfo.get('username','none'),
                                            "phone":userInfo.get('phone','18888888888'),
                                            "email":userInfo.get('email',str(username)+'@arthur.io')})
                i+=1
        return True,{"stared_cnt":stared_cnt,"stared_user_infoList":stared_user_infoList}
        