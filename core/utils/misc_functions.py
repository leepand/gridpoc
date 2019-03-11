from Arthur.core.entities.base.bs_log import Log
import subprocess
# pylint:disable=R0903
import time
from datetime import datetime as datetime_in
from functools import wraps

class TraceUsedTime(object):
    """
    Trace used time inside a function.
    Will print to LOGFILE if you initialized logging with cup.log.init_comlog.
    example::
        import time
        from cup import decorators
        @decorators.TraceUsedTime(True)
        def test():
            print 'test'
            time.sleep(4)
        # trace something with context. E.g. event_id
        def _test_trace_time_map(sleep_time):
            print "ready to work"
            time.sleep(sleep_time)
        traced_test_trace_time_map = decorators.TraceUsedTime(
            b_print_stdout=False,
            enter_msg='event_id: 0x12345',
            leave_msg='event_id: 0x12345'
        )(_test_trace_time_map)
        traced_test_trace_time_map(sleep_time=5)
    """
    def __init__(self, b_print_stdout=False, enter_msg='', leave_msg=''):
        """
        :param b_print_stdout:
            When b_print_stdout is True, CUP will print to both LOGFILE
            that passed to cup.log.init_comlog and stdout
        :param enter_msg:
            entrance msg before invoking the function
        :param leave_msg:
            exist msg after leaving the function
        If you never use cup.log.init_comlog, make sure b_print_stdout == True
        """
        self._b_print_stdout = b_print_stdout
        self._enter_msg = enter_msg
        self._leave_msg = leave_msg

    def __call__(self, function):
        @wraps(function)
        def _wrapper_log(*args, **kwargs):
            now = time.time()
            if self._b_print_stdout:
                print '**enter func:%s,time:%s, msg:%s' % (
                    function, datetime_in.now(), self._enter_msg
                )
            Log.info(
                '**enter func:%s, msg:%s' % (function, self._enter_msg)
            )
            function(*args, **kwargs)
            then = time.time()
            used_time = then - now
            Log.info(
                '**leave func:%s, used_time:%f, msg:%s' % (
                    function, used_time, self._enter_msg
                )
            )
            if self._b_print_stdout:
                print '**leave func:%s, time:%s, used_time:%f, msg:%s' % (
                    function, datetime_in.now(), used_time, self._leave_msg
                )
        return _wrapper_log

# Things below for unittest
"""
@TraceUsedTime(True)
def test():
    time.sleep(3)
test()   
"""
# class for colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
class Commands(object):
    def __init__(self):
        Log.info("handling command cmd script")

    def run_cmd(self, shell_cmd):
        try:
            if type(shell_cmd) is list:
                p = subprocess.Popen(shell_cmd, stdout=subprocess.PIPE)
                out, e = p.communicate()
                Log.info("%s"%
                        (shell_cmd))
                if e:
                    Log.info(e)
                    Log.info(
                        bcolors.FAIL + "error while running the command %s" %
                        (shell_cmd))
                else:
                    return {'output': out, 'status': True}
            else:
                process_returncode = subprocess.Popen(
                    shell_cmd, shell=True).wait()
                Log.info("")
                if process_returncode == 0:
                    return {'status': True}
                else:
                    return {'status': False}
        except Exception as e:
            Log.info(e)
            Log.info(bcolors.FAIL + "error while running the command %s" %
                          (shell_cmd))
            return {'status': False}