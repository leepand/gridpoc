# -*- coding: UTF-8 -*-

# author: leepand
# time: 2018-11-30
# desc: model deploy

from view_base import ViewBase,render,render_without_base
from Arthur.core.entities.bean.hjs_user import HjsUser
from Arthur.core.entities.dao.hjs_user_dao import HjsUserDao

from Arthur.core.entities.bean.Arthur_service import ArthurService
from Arthur.core.entities.dao.Arthur_msg_dao import ArthurMsg
from Arthur.core.utils.token_util import Connector
from Arthur.core.entities.base.bs_log import Log
import web
from web_util import get_req_all_param
#from Arthur.core.entities.dao.hjs_user_dao import *
#参见view_myproject.py
from Arthur.core.apiserver.client import Client
import json
from Arthur.core.entities.base.bs_util import get_myip
#客户端生成

from arthur_utils.file_process import FileStore
from arthur_utils.algo_publish import model_publish 
from arthur_utils.file_utils import list_subdirs
import os,sys
import time
#重构于2019-01-21
class ViewAlgoAdd(ViewBase):
    def GET(self):
        if not self.check_login():
            Log.err("user not login");
            return web.seeother("/login")
        return render_without_base.service_add()#render.service_add()  

class ViewAlgoList(ViewBase):
    def GET(self):
        if not self.check_login():
            Log.err("user not login");
            return web.seeother("/login")
        return render.service_list()    

from operator import itemgetter 
class ViewAlgoZooList (ViewBase):
    def _deal_service_list(self):
        return ArthurService.service_zoo_list(page=1,length=1000, status='normal', search=None)
    def GET(self):
        bRet, sRet = self.check_login()
        if not bRet:
            Log.err("user not login!")
            return web.seeother("/login")        
    
        #_deal_service_list= ArthurService.service_user_list(uId,page=1,length=1000, status=None, search=None)
        bRet, algoList = self.process(self._deal_service_list)
        if not bRet:
            Log.err("deal_service_list: %s" % (str(algoList)))
            self.make_error(algoList)
        #print 'algoList',algoList
        if  algoList is not None and "service_list" in algoList:
            serviceList=algoList['service_list']
            serviceList_bytime = sorted(serviceList,key = itemgetter('insert_tm'),reverse = True)
        else:
            serviceList=[]
            serviceList_bytime=[]
        
        
        #uname=self.get_user_name()
        return render.service_zoo_list(serviceList,serviceList_bytime)

    def POST(self):
        return self.GET()    
#用于遍历项目的子目录
def list_all_filepaths(absolute_dirpath):
    """Returns all filepaths within dir relative to dir root"""
    return [
        os.path.relpath(os.path.join(dirpath, file), absolute_dirpath)
        for (dirpath, dirnames, filenames) in os.walk(absolute_dirpath)
        for file in filenames
    ]
#2018-12-29 update    
class ViewApiAlgoPublish(ViewBase):
    def __init__(self):
        self._rDict = {
            "aid": {'n': "aId", 't': int, 'v': None}
        }

    def _check_param(self):
        bRet, sRet = super(ViewApiAlgoPublish, self)._check_param()
        if not bRet:
            return False, sRet
        return True, None

    def _deploy_algo_publish(self):
        bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        if not bRet:
            return False, sRet
        if not is_admin:
            return False, 'No permission to do this'
        _bRet , algo_info = ArthurService.algo_info(self.aId)
        if not _bRet:
            return False, algo_info
        project_name=algo_info['algoname']
        #项目目录与创建时所用目录一致-ViewApiServUserAdd（build/add阶段）
        project_path=os.path.abspath('arthur_runs/'+self.get_user_name())      
        #rel_path='arthur_runs/'+self.get_user_name()
        process_exp=FileStore(root_directory=project_path) 
        if process_exp.get_experiment_by_name(project_name) is None:
            return False,'No project to publish'
        #根据项目名（experiment_name）获取该项目所在父目录
        funcspath_bath = os.path.join(process_exp.get_experiment_by_name(project_name).artifact_location,project_name)
        
        funcs_sub=list_subdirs(funcspath_bath)
        #增加项目路径
        tracked_files=list_all_filepaths(funcspath_bath)
        for rel_filepath in set(tracked_files):
            # Ensure new directory will exist in the temp dir
            filename = os.path.basename(rel_filepath)
            rel_dirpath = rel_filepath.replace(filename, "")
            funcs_all_path=os.path.join(funcspath_bath,rel_dirpath)
            #sys.path.insert(0, funcs_all_path)
        #print funcs_all_path,'funcs_all_path'
        funcslist=algo_info['funcslist']
        port=algo_info['port']
        token=algo_info['token']
        experiment_id=process_exp.get_experiment_by_name(project_name).experiment_id
        #test.get_experiment_by_name('leepand').experiment_id
        #test.get_experiment_by_name('leepand').name
        run_path=os.path.join(funcspath_bath,funcs_sub[0])
        publish_class=model_publish()
        publish_status = publish_class._invoke_arthur_run_subprocess(funcslist,token=token,
                                                                     runpath=run_path,experiment_id=experiment_id,run_id=self.aId,port=port)
        """build_shell_cmd=publish_class._build_arthur_run_cmd(apifuncs=funcslist,token=token,runpath=run_path, port=port, workers=None, parameters=None)
        command=' '.join(build_shell_cmd)
        proj_path=process_exp.get_experiment_by_name(project_name).artifact_location
        logpath=os.path.join(proj_path,"logfile.txt")
        pidpath=os.path.join(proj_path,"pidfile.txt")
        shell_cmd='nohup {cmd} > {logpath} & echo $! > {pidpath}'.format(cmd=command,logpath=logpath,pidpath=pidpath)
        publish_status=publish_class.run_nohup(shell_cmd,run_id=self.aId)"""
        time.sleep(20)
        if publish_status.get_status()=="RUNNING":
            ArthurService.algo_publish_status_update(self.aId,'normal')
            return True,'algo publish success!'
        else:
            return False,' algo publish failed!'
        return True,publish_status.get_status()#_run_server(self.func, self.token, self.host, self.port)

    def POST(self):
        bRet, sRet = self.check_login()
        if not bRet:
            return web.seeother("/login")
        bRet, sRet = self.process(self._deploy_algo_publish)
        if not bRet:
            Log.err("deploy_algo_publish: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(ViewBase.RetMsg.MSG_SUCCESS)
    
#2019-01-05 add 
def kill9_byname(strname):
    """
    kill -9 process by name
    """
    fd_pid = os.popen("ps -ef | grep -v grep |grep %s \
            |awk '{print $2}'" % (strname))
    pids = fd_pid.read().strip().split('\n')
    fd_pid.close()
    for pid in pids:
        #print pid
        os.system("kill -9 %s" % (pid))
    return True

class ViewApiAlgoUnpublish(ViewBase):
    def __init__(self):
        self._rDict = {
            "aid": {'n': "aId", 't': int, 'v': None}
        }

    def _check_param(self):
        bRet, sRet = super(ViewApiAlgoUnpublish, self)._check_param()
        if not bRet:
            return False, sRet
        return True, None

    def _deploy_algo_unpublish(self):
        bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        if not bRet:
            return False, sRet
        if not is_admin:
            return False, 'No permission to do this'
        _bRet , algo_info = ArthurService.algo_info(self.aId)
        if not _bRet:
            return False, algo_info
        project_name=algo_info['algoname']
        funcslist=algo_info['funcslist']
        port=algo_info['port']
        token=algo_info['token']
        undeploy=kill9_byname(str(port))
        time.sleep(5)
        if undeploy:
            ArthurService.algo_publish_status_update(self.aId,'stop')
            return True,'algo unpublish success!'
        else:
            return False,' algo unpublish failed!'
        return True,"Unpublished Service"#_run_server(self.func, self.token, self.host, self.port)

    def POST(self):
        bRet, sRet = self.check_login()
        if not bRet:
            return web.seeother("/login")
        bRet, sRet = self.process(self._deploy_algo_unpublish)
        if not bRet:
            Log.err("deploy_algo_unpublish: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(ViewBase.RetMsg.MSG_SUCCESS)
    


    
class ViewApiServUserList(ViewBase):
    def __init__(self):
        self._rDict = {
            "page": {'n': "page", 't': int, 'v': 1},
            "length": {'n': "length", 't': int, 'v': 20},
            "status": {'n': "status", 't': str, 'v': 'all'},
            "search": {'n': "search", 't': str, 'v': ''}
        }
    
    def _check_param(self):
        bRet, sRet = super(ViewApiServUserList, self)._check_param()
        if not bRet:
            return False, sRet
        return True, None

    def _deal_service_list(self):
        _bRet,uId=HjsUser.get_user_uid(self.get_user_name())
        if not _bRet:
            return False, uId
        return ArthurService.service_user_list(uId,self.page, self.length, self.status, self.search)

    # get all service list
    def GET(self):
        bRet, sRet = self.check_login()
        if not bRet:
            return web.seeother("/login")
        bRet, algoList = self.process(self._deal_service_list)
        if not bRet:
            Log.err("deal_service_list: %s" % (str(algoList)))
            return self.make_error(algoList)

        return self.make_response(algoList)

    # do search the service list
    def POST(self):
        bRet, sRet = self.check_login()
        if not bRet:
            return web.seeother("/login")
        bRet, algoList = self.process(self._deal_service_list)
        if not bRet:
            Log.err("deal_search_service_list: %s" % (str(algoList)))
            return self.make_error(algoList)

        return self.make_response(algoList)
    
    
class ViewApiServUserAdd(ViewBase):
    def __init__(self):
        self._rDict = {
            "projectname": {'n': "projectname", 't': str, 'v': None},
            "projectdesc": {'n': "projectdesc", 't': str, 'v': None},
            "tags": {'n': "tags", 't': str, 'v': None},
            "funcspath": {'n': "funcspath", 't': str, 'v': None},
            "funclist": {'n': "funclist", 't': str, 'v': None},
            "host": {'n': "host", 't': str, 'v': None},
            "port": {'n': "port", 't': int, 'v': None},
            "algo_field": {'n': "algo_field", 't': int, 'v': None},
            "opertype": {'n': "opertype", 't': str, 'v': None},
            "projecttm": {'n': "projecttm", 't': str, 'v': None},
            "emailmsg": {'n': "emailmsg", 't': str, 'v': None},
            "remark": {'n': "remark", 't': str, 'v': None}
        }

    def _check_param(self):
        bRet, sRet = super(ViewApiServUserAdd, self)._check_param()
        if not bRet:
            return False, sRet
        return True, None

    def _deal_service_add(self):
        project_path=os.path.abspath('arthur_runs/'+self.get_user_name())
        rel_path='arthur_runs/'+self.get_user_name()
        create_exp=FileStore(root_directory=project_path)
        bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        if not bRet:
            return False, sRet
        if not is_admin:
            return False, 'No permission to do this'
        _bRet,uId=HjsUser.get_user_uid(self.get_user_name())
        if not _bRet:
            return False, uId       
        create_exp.create_experiment(self.funcspath,self.projectname)
        #shell_cmd=nohup command > logfile.txt & echo $! > pidfile.txt
        Token_gen=Connector.encrypt_token( 1, str(uId), 'session_token')
        Token_info=Token_gen['token']
        funcspath_bath = os.path.join(create_exp.get_experiment_by_name(self.projectname).artifact_location,self.projectname)
        
        funcs_sub=list_subdirs(funcspath_bath)
        run_path=os.path.join(funcspath_bath,funcs_sub[0])
        publish_class=model_publish()
        build_shell_cmd=publish_class._build_arthur_run_cmd(apifuncs=self.funclist,token=Token_info,runpath=run_path, port=self.port, workers=None, parameters=None)
        #将执行命令写入项目目录
        codepath=create_exp.get_experiment_by_name(self.projectname).artifact_location
        generated_code_filename = os.path.join(codepath,"run.sh")
        with open(generated_code_filename, "w") as f:
            f.write(' '.join(build_shell_cmd))
        #remarks=self.remark
        #remarks.replaceAll("[^0-9a-zA-Z\u4e00-\u9fa5.，,。？“”]", "");
        #return HjsOrder.order_add(self.cId, self.otype, self.order_tm, self.start_tm, self.end_tm, self.amount, self.cash, self.remark)
        return ArthurService.service_add(uId,self.projectname, self.projectdesc,self.opertype,rel_path,#self.funcspath
                                 self.funclist,self.tags,self.algo_field,self.host,self.port,self.projecttm,
                                 self.emailmsg,str(self.remark))

    def POST(self):
        bRet, sRet = self.check_login()
        if not bRet:
            return web.seeother("/login")
        bRet, sRet = self.process(self._deal_service_add)
        if not bRet:
            Log.err("deal_service_add: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(ViewBase.RetMsg.MSG_SUCCESS)
    
    
class ViewApiServUserMsg(ViewBase):
    
    def _deal_service_msg(self):
        bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        if not bRet:
            return False, sRet
        if not is_admin:
            return False, 'No permission to do this'
        _bRet,uId=HjsUser.get_user_uid(self.get_user_name())
        if not _bRet:
            return False, uId   
        self.msg_info = get_req_all_param()
        print 'self.msg_info',self.msg_info
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
            ArthurMsg.update_node_user_msg(id,content,modified)
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
class ViewApiServMsgUser(ViewBase):
    #def _check_param(self):
    #    bRet, sRet = super(ViewApiServMsgUser, self)._check_param()
    #   if not bRet:
    #        return False, sRet
        
    #    return True, None

    def _deal_msg_user_info(self):
        bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        if not bRet:
            return False, sRet
        #if not is_admin:
        #    return False, 'No permission do user info'
        bRet, user_id =  HjsUser.get_user_uid(self.get_user_name())
        if not bRet:
            return False, user_id
        _bRet, msg_user_list =HjsUserDao.query_node_msg_user_list(user_id,"../static/images/user-icon.png")
        if not _bRet:
            return False, msg_user_list
        return True,msg_user_list

    def GET(self):
        if not self.check_login():
            return self.make_error("user not login")

        bRet, sRet = self.process(self._deal_msg_user_info)
        if not bRet:
            Log.err("deal_msg_user_info: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(sRet)


class ViewApiServMsgList(ViewBase):
    #def _check_param(self):
    #    bRet, sRet = super(ViewApiServMsgUser, self)._check_param()
    #   if not bRet:
    #        return False, sRet
    #    
    #    return True, None
    
    def _deal_msg_user_list(self):
        msg_info = get_req_all_param()
        userName=msg_info.get('userName','')
        projectName = msg_info.get('projectName','')
        #bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        #if not bRet:
        #    return False, sRet
        #if not is_admin:
        #    return False, 'No permission do user info'
        bRet, user_id =  HjsUser.get_user_uid(self.get_user_name())
        if not bRet:
            return False, user_id
        _bRet, msg_user_list=ArthurMsg.query_node_msg_list_by_usrproj(userName,projectName)
        #_bRet, msg_user_list =HjsUserDao.query_node_msg_user_list(user_id,"../static/images/user-icon.png")
        if not _bRet:
            return False, msg_user_list
        #print 'msg_info = get_req_all_param()',msg_info 
        #print 'comments;;;;;;;',msg_user_list
        return True,msg_user_list

    def GET(self):
        if not self.check_login():
            return self.make_error("user not login")

        bRet, sRet = self.process(self._deal_msg_user_list)
        if not bRet:
            Log.err("deal_msg_user_list: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(sRet) 

BASE_INFO = '''
# coding:utf-8
"""
Compatible for python2.x and python3.x
requirement: pip install requests Arthur
"""
from Arthur.api_server.client import Client
client =Client('{ip}',auth_token={token})
'''
INFER_INFO = '''client.{function_name}(**input_data)'''
def load_function(function_spec, path=None, name=None):
    if "." not in function_spec:
        raise Exception("Invalid function: {}, please specify it as module.function".format(function_spec))

    mod_name, func_name = function_spec.rsplit(".", 1)
    path = path or "/"+func_name
    name = name or func_name
    return name

def load_functions(function_specs):
    return [load_function(function_spec) for function_spec in function_specs]


class ViewApiRunApi(ViewBase):
    #def _check_param(self):
    #    bRet, sRet = super(ViewApiServMsgUser, self)._check_param()
    #   if not bRet:
    #        return False, sRet
        
    #    return True, None
    
    def _deal_run_api_example(self):
        msg_info = get_req_all_param()
        #获取api信息
        model_info=eval(msg_info['algoinfo'])
        username= model_info['username']
        proJectname= model_info['algoname']
        _bRet, uId = HjsUser.get_user_uid(username)
        if not _bRet:
            return False,uId
        _bRet_,algo_detail_info= ArthurService.algo_proj_info(uId,proJectname)
        host=algo_detail_info['host']
        port = algo_detail_info['port']
        data=algo_detail_info['remark']
        tags=algo_detail_info['tags']
        token=algo_detail_info['token']
        funcslist_str=algo_detail_info['funcslist']
        bind_address2 = "http://%s:%s" % ('0.0.0.0', int(port))#get_myip()
        client = Client(bind_address2,auth_token=token)
        data=msg_info['data']
        #print input_data,type(input_data),'input_data'
        #base_algo_info=BASE_INFO.format(ip=bind_address2, token=token)
        #eval(base_algo_info)
        if '|' in data:
            datalist=data.split("|")
        else:
            datalist=[data]

        infer_info_dict={}
        funcs_info=load_functions(funcslist_str.split(","))
        for inter in range(len(funcs_info)):
            try:
                datainfo=datalist[inter]
                if len(datainfo)<1:
                    datainfo=None
            except:
                datainfo=None
            #print 'datainfo',datainfo,type(datainfo)
            input_data = eval(datainfo)
            
            result= eval(INFER_INFO.format(function_name=funcs_info[inter]))
            infer_info_dict[funcs_info[inter]]=result
        #infer_algo_info='\n'.join(infer_info_list)
        #python_client_info=base_algo_info+infer_algo_info
        
        
        infer=INFER_INFO.format(data=datainfo,function_name=funcs_info[inter])
        #result=client.pred(**input_data)
        #print 'result',result
        bRet, is_admin = HjsUser.is_admin(self.get_user_name())
        if not bRet:
            return False, sRet
        #if not is_admin:
        #    return False, 'No permission do run example'
        bRet, user_id =  HjsUser.get_user_uid(self.get_user_name())
        if not bRet:
            return False, user_id
        #print 'msg_info = get_req_all_param()',msg_info 
        #print 'comments;;;;;;;',msg_user_list
        return True,json.dumps(infer_info_dict)

    def GET(self):
        if not self.check_login():
            return self.make_error("user not login")

        bRet, sRet = self.process(self._deal_run_api_example)
        if not bRet:
            Log.err("deal_run_api_example: %s" % (str(sRet)))
            return self.make_error(sRet)

        return self.make_response(sRet)  
    
    