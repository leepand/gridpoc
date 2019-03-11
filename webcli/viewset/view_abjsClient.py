# -*- coding: UTF-8 -*-

# author: leepand
# time: 2019-02-13
# desc: Arthur abtesting js client

from view_base import ViewBase,render,render_without_base
from Arthur.core.entities.base.bs_log import Log

class ViewABjsClient(ViewBase):
    def GET(self):
        bRet, sRet = self.check_login()
        if not bRet:
            Log.err("user not login!")
            return web.seeother("/login")
             
        return render_without_base.indexTest()

    def POST(self):
        return self.GET()
    
    
    