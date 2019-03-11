# -*- coding: UTF-8 -*-

# author: leepand
# time: 2018-11-30
# desc: model deploy

from view_base import *
from hjs_user import *
from hjs_order import *
from hjs_ps_order import *
from bs_process import *#for service process exce_cmd
__version__ = '0.0.7'
APIFLY_FUNCTIONS="APIFLY_FUNCTIONS"
APIFLY_TOKEN="APIFLY_TOKEN"
def _run_server(apifly_function, apifly_token, host, port, workers=2, is_reg=False,static_prefix=None,
                gunicorn_opts=None):
    """
    Run the Arthur api server, wrapping it in gunicorn
    :param static_prefix: If set, the index.html asset will be served from the path static_prefix.
                          If left None, the index.html asset will be served from the root path.
    :return: None
    """
    env_map = {}
    if apifly_function:
        env_map[APIFLY_FUNCTIONS] = apifly_function
    if apifly_token:
        env_map[APIFLY_TOKEN] = apifly_token
    if static_prefix:
        env_map[STATIC_PREFIX_ENV_VAR] = static_prefix

    bind_address = "%s:%s" % (host, port)
    bind_address2 = "http//%s:%s" % (host, port)
    if is_reg:
        redis_db=api.data_api(redis_db=3).redis_api(use_type='mem',prefix='REST:SERVICE_LIST:')
        reg_info={}
        funcs_info=load_functions(apifly_function.split(","))
        addr=bind_address2
        token=apifly_token
        reg_info['addr']=addr
        reg_info['token']=token
        reg_info['funcs_list']=funcs_info
        redis_db['REST_SERVICE_REG']=json.dumps(reg_info)
    opts = shlex.split(gunicorn_opts) if gunicorn_opts else []
    exec_cmd(["gunicorn"] + opts + ["-b", bind_address, "-w", "%s" % workers,
                                    "--worker-class","gevent",
                                    "Arthur.api_server.main:app"],env=env_map, stream_output=True)
class ViewApiModelAdd(ViewBase):
    def __init__(self):
        self._rDict = {
            "apifly_function": {'n': "func", 't': str, 'v': None},
            "apifly_token": {'n': "token", 't': str, 'v': None},
            "host": {'n': "host", 't': str, 'v': ''},
            "port": {'n': "port", 't': int, 'v': None}
        }

    def _check_param(self):
        bRet, sRet = super(ViewApiModelAdd, self)._check_param()
        if not bRet:
            return False, sRet
        return True, None

    def _deploy_model_add(self):
        bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        if not bRet:
            return False, sRet
        if not is_admin:
            return False, 'No permission to do this'
        return _run_server(self.func, self.token, self.host, self.port)

    def POST(self):
        bRet, sRet = self.check_login()
        if not bRet:
            return web.seeother("/login")
        bRet, sRet = self.process(self._deploy_model_add)
        if not bRet:
            Log.err("deal_order_add: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(ViewBase.RetMsg.MSG_SUCCESS)
    
    
class ViewAlgoPublish(ViewBase):
    def GET(self):
        if not self.check_login():
            Log.err("user not login");
            return web.seeother("/login")
        return render.algo_deploy_publish()