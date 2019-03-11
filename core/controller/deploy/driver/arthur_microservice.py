# -*- coding: UTF-8 -*-

# author: leepand
# time: 2019-01-28
# desc: 服务部署基础组件
import os
import itertools
import time
import sys
from Arthur.core.utils.store.exp_file_process import FileStore
from Arthur.core.utils.store.file_utils import list_subdirs
from Arthur.core.utils import  port_for
from Arthur.core.utils.token_util import Connector
from Arthur.core.entities.bean.Arthur_service import ArthurService
from Arthur.core.entities.base.bs_time import get_cur_day
from Arthur.core.entities.base.bs_log import Log
from Arthur.core.entities.bean.hjs_user import HjsUser
from Arthur.core.utils.algo_publish import model_publish
from Arthur.core.utils.spinner import Spinner


class ArthurMicroserviceDeployDriver(object):
    """
    Arthur Microservice deployment driver
    """

    def __init__(self,cmd_pub_type):
        self.pub_type= cmd_pub_type#local/remote
        self.spinner = Spinner()
    def wait_until_algo_published(
        self,publish_status,aId, max_wait_sec=20, interval_sec=0.1
    ):
        """
        wait util the algo published or timeout
        :param publish_status:
            publish status for wait :RUNNING,FAILED,FINISHED
        :param max_wait_sec:
            max wating time until timeout
        :param interval_sec:
            check interval
        :return:
            True if algorithm service publish success.
        """
        curr_wait_sec = 0
        spinner_generator = itertools.cycle(['-', '/', '|', '\\'])
        while curr_wait_sec < max_wait_sec:
        
            if publish_status=="FAILED" or publish_status=="FINISHED" :
                if aId is not None:
                    ArthurService.algo_publish_status_update(aId,'stop')
                return False
            curr_wait_sec += interval_sec
            sys.stdout.write(next(spinner_generator))
            sys.stdout.flush()
            time.sleep(interval_sec)
            sys.stdout.write('\b')  
        #对发布的算法状态进行更新
        if aId is not None:
            ArthurService.algo_publish_status_update(aId,'normal')
        ret="algorithm service publish success!"
        Log.info("****RESP: %s" % ret)
        return True
    def createExpInfo(self,userName):
        project_path=os.path.abspath('arthur_runs/'+userName)
        create_exp=FileStore(root_directory=project_path)
        return create_exp
    def getExpInfo(self,userName,projectName):  
        project_path=os.path.abspath('arthur_runs/'+userName)      
        #rel_path='arthur_runs/'+self.get_user_name()
        process_exp=FileStore(root_directory=project_path) 
        if process_exp.get_experiment_by_name(projectName) is None:
            return False,'No project to publish'
        return process_exp
        
    def algoInfoAdd(self,userName,projectName,funcsPath,funcList,algoField=1,port=None,\
                   projecttm=None,remark=None,emailmsg=None,opertype=None,projectdesc=None,tags=None):
        """
        Validate deployment before packaging the project to push
        prepare algo info for deploy, 
        copy user's algo project to arthur runs path/user
        """
        _bRet,uId=HjsUser.get_user_uid(userName)
        if not _bRet:
            return False, uId  
        create_exp = self.createExpInfo(userName)
        rel_path='arthur_runs/'+userName
        #迁移源项目路径至新建路径
        create_exp.create_experiment(funcsPath,projectName)
        Token_gen=Connector.encrypt_token( 1, str(uId), 'session_token')
        Token_info=Token_gen['token']
        funcspath_bath = os.path.join(create_exp.get_experiment_by_name(projectName).artifact_location,projectName)
        funcs_sub=list_subdirs(funcspath_bath)
        run_path=os.path.join(funcspath_bath,funcs_sub[0])#一个项目只有一个主目录-default
        if port is None:
            port=port_for.select_random()
        if projecttm is None:
            projecttm = get_cur_day(0, format="%Y-%m-%d %H:%M:%S")
        if remark is None:
            remark="请到主页编辑添加"
        if emailmsg is None:
            emailmsg="是"
        if opertype is None:
            opertype="publish"
        if projectdesc is None:
            projectdesc="暂无描述，请到主页编辑添加"
        if tags is None:
            tags='Machine Learning'
        ArthurService.service_add(uId,projectName, projectdesc,opertype,rel_path,
                                     funcList,tags,algoField,'0.0.0.0',port,projecttm,emailmsg,str(remark))
        return create_exp,uId
    def algoDeployCli(self,funcsPath,funcList,userName=None,projectName=None,port=None,token=''):
        pub_type=self.pub_type
        publish_class=model_publish()
        if pub_type=="local":
            if port is None:
                port=port_for.select_random()
            run_path = funcsPath
            publish_status = publish_class._invoke_arthur_run_subprocess(funcList,experiment_id=1,run_id=1,token=token,port=port,runpath=run_path)
            publish_status,pid_info = publish_status.get_status()
            wait_result = self.wait_until_algo_published(publish_status,aId=None) 
            host ="0.0.0.0"
            bind_address = "%s:%s" % (host, port)
            if wait_result:
                Log.info('algo deploy success')
                Log.info('the end point of your algo service %s is %s'% (funcList,bind_address))
                return True,'algo deploy success'
            else:
                Log.err("algo deploy failed");
                return False,'algo deploy failed'
    
        else:
            self.spinner.start()
            create_exp_info,uId = self.algoInfoAdd(userName,projectName,funcsPath,funcList,port=port)#port非指定的情况系统自动生成
            self.spinner.stop()
            _bRet,algoInfo = ArthurService.algo_proj_info(uId,projectName)#AlgoName=projectName
            #funcslist=algoInfo['funcslist']
            port=algoInfo['port']
            token=algoInfo['token']
            aId = algoInfo['aid']
            experiment_id=create_exp_info.get_experiment_by_name(projectName).experiment_id
            runId= aId
            funcspath_bath = os.path.join(create_exp_info.get_experiment_by_name(projectName).artifact_location,projectName)        
            funcs_sub=list_subdirs(funcspath_bath)
            run_path=os.path.join(funcspath_bath,funcs_sub[0])            
            publish_status = publish_class._invoke_arthur_run_subprocess(funcList,experiment_id,runId,token=token,port=port,runpath=run_path)
            #将pid写入项目目录
            pidPath=create_exp_info.get_experiment_by_name(projectName).artifact_location
            publish_status,pid_info = publish_status.get_status()
            generated_pid_filename = os.path.join(pidPath,"pid.pid")
            with open(generated_pid_filename, "w") as f:
                f.write(str(pid_info))
            wait_result = self.wait_until_algo_published(publish_status,aId) 
            host ="0.0.0.0"
            bind_address = "%s:%s" % (host, port)
            if wait_result:
                Log.info('algo deploy success')
                Log.info('the end point of your algo service %s is %s'% (funcList,bind_address))
                return True,'algo deploy success'
            else:
                Log.err("algo deploy failed");
                return False,'algo deploy failed'
    def algoDeployUI(self,aId,userName):
        publish_class=model_publish()
        self.spinner.start()
        _bRet , algo_info = ArthurService.algo_info(aId)
        if not _bRet:
            return False, algo_info
        projectName=algo_info['algoname'] 
        #userName=algo_info['username']
        funcslist=algo_info['funcslist']
        port=algo_info['port']
        token=algo_info['token']
        uId=algo_info['uid']
        process_exp = self.getExpInfo(userName,projectName) 
        #_bRet,uId=HjsUser.get_user_uid(userName)
        #if not _bRet:
        #    return False, uId  
        #create_exp_info,uId = self.algoInfoAdd(userName,projectName,funcsPath,funcList)
        self.spinner.stop()    
        #_bRet,algoInfo = ArthurService.algo_proj_info(uId,projectName)#AlgoName=projectName
        #funcslist=algoInfo['funcslist']
        #funcslist=algoInfo['funcslist']
        #port=algoInfo['port']
        #token=algoInfo['token']
        #aId = algoInfo['aid']
        experiment_id=process_exp.get_experiment_by_name(projectName).experiment_id
        runId= aId
        funcspath_bath = os.path.join(process_exp.get_experiment_by_name(projectName).artifact_location,projectName)        
        funcs_sub=list_subdirs(funcspath_bath)
        run_path=os.path.join(funcspath_bath,funcs_sub[0])            
        publish_status = publish_class._invoke_arthur_run_subprocess(funcslist,experiment_id,runId,token=token,port=port,runpath=run_path)
        #将pid写入项目目录
        pidPath=process_exp.get_experiment_by_name(projectName).artifact_location
        publish_status,pid_info = publish_status.get_status()
        generated_pid_filename = os.path.join(pidPath,"pid.pid")
        with open(generated_pid_filename, "w") as f:
            f.write(str(pid_info))
        wait_result = self.wait_until_algo_published(publish_status,aId) 
        host ="0.0.0.0"
        bind_address = "%s:%s" % (host, port)
        if wait_result:
            Log.info('algo deploy success')
            Log.info('the end point of your algo service %s is %s'% (funcslist,bind_address))
            return True,'algo deploy success'
        else:
            Log.err("algo deploy failed");
            return False,'algo deploy failed'