# -*- coding: UTF-8 -*-

# author: leepand
# time: 2019-01-07
# desc: Arthur Dashboard

from view_base import ViewBase,render,render_without_base
from Arthur.core.entities.bean.Arthur_dashboard import ArthurDashboard
from Arthur.core.entities.base.bs_log import Log

class ViewApiDashboardIndex(ViewBase):
    def _deal_data_show(self):
        return ArthurDashboard.data_show(self.get_user_name())


    def GET(self):
        if not self.check_login():
            return self.make_error("user not login")

        bRet, sRet = self.process(self._deal_data_show)
        if not bRet:
            Log.err("deal_data_show: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(sRet)