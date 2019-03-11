# -- coding:utf-8 --
import os
import subprocess
import threading
import warnings
import signal
class ShellExec(object):  # pylint: disable=R0903
    """
    For shell command execution.
    ::
        from cup import shell
        shellexec = shell.ShellExec()
        # timeout=None will block the execution until it finishes
        shellexec.run('/bin/ls', timeout=None)
        # timeout>=0 will open non-blocking mode
        # The process will be killed if the cmd timeouts
        shellexec.run(cmd='/bin/ls', timeout=100)
    """

    def __init__(self):
        self._subpro = None
        self._subpro_data = None

    def __kill_process(self, pid):
        os.kill(pid, signal.SIGKILL)

    def kill_all_process(self, async_content):
        """
        to kill all process
        """
        for pid in async_content.child_list:
            self.__kill_process(pid)

    def get_async_run_status(self, async_content):
        """
        get the command's status
        """
        try:
            from cup.res import linux
            async_process = linux.Process(async_content.pid)
            res = async_process.get_process_status()
        except err.NoSuchProcess:
            res = "process is destructor"
        return res

    def get_async_run_res(self, async_content):
        """
        if the process is still running the res shoule be None,None,0
        """
        return async_content.ret

    def async_run(self, cmd, timeout):
        """
        async_run
        return a dict {uuid:pid}
        self.argcontent{cmd,timeout,ret,cmdthd,montor}
        timeout:returncode:999
        cmd is running returncode:-999
        """

        def _signal_handle():
            """
            signal setup
            """
            signal.signal(signal.SIGPIPE, signal.SIG_DFL)

        def _target(argcontent):
            argcontent.__subpro = subprocess.Popen(
                    argcontent.cmd, shell=True, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    preexec_fn=_signal_handle)
            from cup.res import linux
            parent = linux.Process(argcontent.__subpro.pid)
            children = parent.children(True)
            ret_dict = []
            for process in children:
                ret_dict.append(process)
            argcontent.child_list = ret_dict

        def _monitor(start_time, argcontent):
            while(int(time.mktime(datetime.datetime.now().timetuple())) - int(start_time) <
                    int(argcontent.timeout)):
                time.sleep(1)
                if argcontent.__subpro.poll() is not None:
                    self._subpro_data = argcontent.__subpro.communicate()
                    argcontent.ret['returncode'] = argcontent.__subpro.returncode
                    argcontent.ret['stdout'] = self._subpro_data[0]
                    argcontent.ret['stderr'] = self._subpro_data[1]
                    return
            str_warn = (
                'Shell "%s"execution timout:%d. To kill it' % (argcontent.cmd,
                    argcontent.timeout)
            )
            argcontent.__subpro.terminate()
            argcontent.ret['returncode'] = 999
            argcontent.ret['stderr'] = str_warn

            for process in argcontent.child_list:
                self.__kill_process(process)
            del argcontent.child_list[:]

        argcontent = Asynccontent()
        argcontent.cmd = cmd
        argcontent.timeout = timeout
        argcontent.ret = {
            'stdout': None,
            'stderr': None,
            'returncode': -999
        }
        argcontent.__cmdthd = threading.Thread(target=_target, args=(argcontent,))
        argcontent.__cmdthd.start()
        start_time = int(time.mktime(datetime.datetime.now().timetuple()))
        argcontent.__cmdthd.join(0.1)
        argcontent.pid = argcontent.__subpro.pid
        argcontent.__monitorthd = threading.Thread(target=_monitor,
                args=(start_time, argcontent))
        argcontent.__monitorthd.start()
        #this join should be del if i can make if quicker in Process.children
        argcontent.__cmdthd.join(0.5)
        return argcontent

    def run(self, cmd, timeout):
        """
        refer to the class description
        :param timeout:
            If the cmd is not returned after [timeout] seconds, the cmd process
            will be killed. If timeout is None, will block there until the cmd
            execution returns
        :return:
            returncode == 0 means success, while 999 means timeout
            {
                'stdout' : 'Success',
                'stderr' : None,
                'returncode' : 0
            }
        E.g.
        ::
            import cup
            shelltool = cup.shell.ShellExec()
            print shelltool.run('/bin/ls', timeout=1)
        """

        def _signal_handle():
            """
            signal setup
            """
            signal.signal(signal.SIGPIPE, signal.SIG_DFL)

        def _target(cmd):
            self._subpro = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=_signal_handle
            )
            self._subpro_data = self._subpro.communicate()
        ret = {
            'stdout': None,
            'stderr': None,
            'returncode': 0
        }
        cmdthd = threading.Thread(target=_target, args=(cmd, ))
        cmdthd.start()
        cmdthd.join(timeout)
        if cmdthd.isAlive() is True:
            str_warn = (
                'Shell "%s"execution timout:%d. To kill it' % (cmd, timeout)
            )
            warnings.warn(str_warn, RuntimeWarning)
            self._subpro.terminate()
            ret['returncode'] = 999
            ret['stderr'] = str_warn
        else:
            self._subpro.wait()
            times = 0
            while self._subpro.returncode is None and times < 10:
                time.sleep(1)
                times += 1
            ret['returncode'] = self._subpro.returncode
            assert type(self._subpro_data) == tuple, \
                'self._subpro_data should be a tuple'
            ret['stdout'] = self._subpro_data[0]
            ret['stderr'] = self._subpro_data[1]
        return ret


def _do_execshell(cmd, b_printcmd=True, timeout=None):
    """
    do execshell
    """
    if timeout is not None and timeout < 0:
        raise cup.err.ShellException(
            'timeout should be None or >= 0'
        )
    if b_printcmd is True:
        print 'To exec cmd:%s' % cmd
    shellexec = ShellExec()
    return shellexec.run(cmd, timeout)


def execshell(cmd, b_printcmd=True, timeout=None):
    """
    执行shell命令，返回returncode
    """
    return _do_execshell(
        cmd, b_printcmd=b_printcmd, timeout=timeout)['returncode']


def kill9_byname(strname):
    """
    kill -9 process by name
    """
    fd_pid = os.popen("ps -ef | grep -v grep |grep %s \
            |awk '{print $2}'" % (strname))
    pids = fd_pid.read().strip().split('\n')
    fd_pid.close()
    for pid in pids:
        os.system("kill -9 %s" % (pid))
#kill9_byname('gunicorn')