# -*- coding: UTF-8 -*-

# author: leepand
# time: 2018-11-30
# desc: model deploy
import web
from web_util import get_req_all_param
from view_base import ViewBase,render,render_without_base
from Arthur.core.entities.bean.hjs_user import HjsUser
from Arthur.core.entities.dao.hjs_user_dao import HjsUserDao
from Arthur.core.entities.dao.Arthur_msg_dao import ArthurMsg
from Arthur.core.entities.base.bs_log import Log

    
    
class ViewApiQAMsgSave(ViewBase):  
    def _deal_service_msg(self):
        bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        if not bRet:
            return False, sRet
      
        _bRet,uId=HjsUser.get_user_uid(self.get_user_name())
        if not _bRet:
            return False, uId   
        self.msg_info = get_req_all_param()
        id=self.msg_info['id'] 
        username=self.msg_info['username']
        projectname=self.msg_info['projectname']
        creator=self.msg_info.get('creator','')
        created= self.msg_info['created']
        modified = self.msg_info['modified']
        parent = self.msg_info.get('parent','')
        #if parent=='':
        #    parent='null'
        content=self.msg_info.get('content','')
      
        pings=self.msg_info.get('pings[]','')
        fullname=self.get_user_name()#self.msg_info.get('fullname','')
        profile_picture_url=self.msg_info['profile_picture_url']
        created_by_admin = self.msg_info.get('created_by_admin','false')
        created_by_current_user=self.msg_info.get('created_by_current_user','false')
        user_has_upvoted=self.msg_info.get('user_has_upvoted','false')
        is_new= self.msg_info.get('is_new','false')
        upvote_count= self.msg_info.get('upvote_count',0)
        _bRet_, msginfo = ArthurMsg.query_node_by_id(id,username,projectname)
        if len(msginfo)>0:
            ArthurMsg.update_node_user_msg(id,content,modified,user_has_upvoted,int(upvote_count))
        else:
            ArthurMsg.insert_node_user_msg(id, username,projectname,creator,created, modified, parent, content, pings,fullname,profile_picture_url,\
                                       created_by_admin,created_by_current_user,user_has_upvoted,is_new,upvote_count)
        #yy=ArthurMsg.query_node_by_id('c13')
        #zz=ArthurMsg.query_node_msg_list()
        #ArthurMsg.update_node_user_msg('c12','hahhhhha','2018-12-29')
        #print ('self.suggest',self.modified,type(self.modified))
        return True,True

    def POST(self):
        bRet, sRet = self.check_login()
        if not bRet:
            return web.seeother("/login")
        bRet, sRet = self.process(self._deal_service_msg)
        if not bRet:
            Log.err("deal_service_add: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(ViewBase.RetMsg.MSG_SUCCESS)
class ViewApiQAdata(ViewBase):
    def __init__(self):
        self._rDict = {
            "userName": {'n': "userName", 'str': int, 'v': None},
            "projectName": {'n': "projectName", 'str': int, 'v': None}
        }

    def _check_param(self):
        bRet, sRet = super(ViewApiQAdata, self)._check_param()
        if not bRet:
            return False, sRet
        return True, None

    def _deal_msg_info(self):
        bRet, user_id =  HjsUser.get_user_uid(self.get_user_name())
        if not bRet:
            return False, user_id
        _bRet, QAuser_list =HjsUserDao.query_node_msg_user_list(user_id,"../static/images/user-icon.png")
        
        if not _bRet:
            return False, QAuser_list
  
        _bRet, QAmsg_list=ArthurMsg.query_node_msg_list_by_usrproj(self.userName,self.projectName)
    
        if not _bRet:
            return False, QAmsg_list

        return True,{"QAmsg_list":QAmsg_list,"QAuser_list":QAuser_list,"loginUser":self.get_user_name()}

    def GET(self):
        if not self.check_login():
            return self.make_error("user not login")

        bRet, sRet = self.process(self._deal_msg_info)
        if not bRet:
            Log.err("deal_msg_info: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(sRet)