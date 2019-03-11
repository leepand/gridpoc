# -*- coding: UTF-8 -*-
# author: leepand
# time: 2019-02-27
# desc: abtesting dispatcher
from Arthur.core.controller.abtesting.driver.abtesting_client import SessionDriver

class ABexpDispatcher(object):
    def __init__(self, client_id=None,options=None):
        self.options = options
        self.session = SessionDriver(client_id=client_id, options=self.options)

    def get_model(self,exp_name, model_list,force=None, traffic_fraction=1, prefetch=False):
        return self.session.participate(exp_name, model_list)#["alternative"]

    def model_convert(self, exp_name, kpi=None):
        return self.session.convert(exp_name,kpi)

"""
options ={'host': 'http://0.0.0.0:8002'}

recom=ABexpDispatcher(options=options)
recom.get_model("ab_recom_join", ["alternative-2", "alternative-1"])
recom.model_convert('ab_recom_join',kpi='cvt')
"""