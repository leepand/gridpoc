# -*- coding: UTF-8 -*-

# author: s0nnet
# time: 2016-11-08
# desc: index view

from view_base import ViewBase,render,render_without_base
from Arthur.core.entities.bean.hjs_user import HjsUser
import Arthur.core.abtesting.utils.db as db
from Arthur.core.entities.base.bs_log import Log
import web




class ViewTagService(ViewBase):
    def GET(self,tag):
        bRet, sRet = self.check_login()
        if not bRet:
            Log.err("user not login!")
            return web.seeother("/login")
             
        return render.service_zoo_list_tags(tag)

    def POST(self):
        return self.GET(tag)
    


