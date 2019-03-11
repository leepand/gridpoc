# -*- coding: UTF-8 -*-

# author: Leepand
# time: 2019-01-25
# desc: 进程创建封装

import os
import subprocess
from subprocess import Popen,PIPE,traceback
from Arthur.core.entities.base.bs_log import Log
import time

def bs_system(cmd, stdout = False, stderr = True):
    bRet = False
    
    if not stderr:      cmd = "%s >> /dev/null 2>&1" %(cmd)
    elif not stdout:    cmd = "%s >> /dev/null" %(cmd)
    
    try:
        retState = os.system(cmd)
    except Exception, e:
        Log.err("cmd(%s) ERR(%s)" %(cmd, str(e)))
        retState = -1
    
    Log.debug("%s, retstate = %d" %(cmd, retState))
    if retState == 0: bRet = True
    return bRet


# 管道执行命令， 命令小输出还可以， 如果输出比较大推荐走文件输出流
def exec_cmd2(cmd):
    
    Log.debug("cmd: %s" %(cmd))
    content = ""
    try:
        p = Popen(cmd, bufsize = 4096, stdout = PIPE, shell = True)
        
        while True:
            cont = p.stdout.read()
            if cont == "": break
            content += cont
            Log.debug("contLen: %d" %(len(cont)))
            time.sleep(1)
        retState = p.wait()
        
        return retState, content
    except Exception, e:
        Log.err("(%s)" %(traceback.format_exc()))
        return 255, "cmd(%s) err: %s" %(str(cmd), str(e))



class ShellCommandException(Exception):
    pass


def exec_cmd(cmd, throw_on_error=True, env=None, stream_output=False, cwd=None, cmd_stdin=None,
             **kwargs):
    """
    Runs a command as a child process.
    A convenience wrapper for running a command from a Python script.
    Keyword arguments:
    cmd -- the command to run, as a list of strings
    throw_on_error -- if true, raises an Exception if the exit code of the program is nonzero
    env -- additional environment variables to be defined when running the child process
    cwd -- working directory for child process
    stream_output -- if true, does not capture standard output and error; if false, captures these
      streams and returns them
    cmd_stdin -- if specified, passes the specified string as stdin to the child process.
    Note on the return value: If stream_output is true, then only the exit code is returned. If
    stream_output is false, then a tuple of the exit code, standard output and standard error is
    returned.
    """
    cmd_env = os.environ.copy()
    if env:
        cmd_env.update(env)

    if stream_output:
        child = subprocess.Popen(cmd, env=cmd_env, cwd=cwd, universal_newlines=True,
                                 stdin=subprocess.PIPE, **kwargs)
        child.communicate(cmd_stdin)
        exit_code = child.wait()
        if throw_on_error and exit_code is not 0:
            raise ShellCommandException("Non-zero exitcode: %s" % (exit_code))
        return exit_code
    else:
        child = subprocess.Popen(
            cmd, env=cmd_env, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE,
            cwd=cwd, universal_newlines=True, **kwargs)
        (stdout, stderr) = child.communicate(cmd_stdin)
        exit_code = child.wait()
        if throw_on_error and exit_code is not 0:
            raise ShellCommandException("Non-zero exit code: %s\n\nSTDOUT:\n%s\n\nSTDERR:%s" %
                                        (exit_code, stdout, stderr))
        return exit_code, stdout, stderr
    
#  进程池   
class YgProcessPool:
    
    def __init__(self, pidNum, fun, args):
        
        self.pool   =   []      # 进程池
        self.size   =   pidNum
        self.fun    =   fun
        self.args   =   args
    
    def start(self, wait = False):
        
        bRet = True
        try:
            for i in range(self.size):
                pid = os.fork()
                if pid == 0:
                    retCode = 0
                    try:
                        bRet = self.fun(i, self.size, self.args)
                        if not bRet: retCode = -1
                    except Exception, e:
                        Log.err("ERR(%s)" %(traceback.format_exc()))
                        retCode = -1
                         
                    os._exit(retCode)
                    #sys.exit(retCode)
                    
                self.pool.append(pid)
            
            if wait:
                bRet = self.wait()
                
        except Exception, e:
            Log.err("ERR(%s)" %(traceback.format_exc()))
            bRet = False
            
        return bRet
    
    def wait(self):
        
        bRet = True
        for i in range(self.size):
            pid, retCode = os.waitpid(self.pool[i], 0)
            if retCode != 0: bRet = False
        return bRet 
    
    
