import logging
import os
import subprocess
from submitted_run import LocalSubmittedRun
import shlex

__version__ = '0.0.8'
APIFLY_FUNCTIONS="APIFLY_FUNCTIONS"
APIFLY_TOKEN="APIFLY_TOKEN"
STATIC_PREFIX_ENV_VAR="STATIC_PREFIX_ENV_VAR"

_logger = logging.getLogger(__name__)
def _runServerCmdbase(apifly_function, apifly_token, host, port, workers, static_prefix,gunicorn_opts):
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
    
    opts = shlex.split(gunicorn_opts) if gunicorn_opts else []
    exec_cmd(["gunicorn"] + opts + ["-b", bind_address, "-w", "%s" % workers,
                                    "--worker-class","gevent",
                                    "Arthur.core.apiserver.main:app"],
             env=env_map, stream_output=True)
    
class model_publish(object):
    def _run_arthur_run_cmd(self,arthur_run_arr,apifly_function, apifly_token='',static_prefix='',env_map={}):
        """
        Invoke ``arthur run`` in a subprocess, which in turn runs the entry point in a child process.
        Returns a handle to the subprocess. Popen launched to invoke ``arthur run``.
        """
        #final_env = os.environ.copy()
        #env_map = {}
        if apifly_function:
            env_map[APIFLY_FUNCTIONS] = apifly_function
        if apifly_token:
            env_map[APIFLY_TOKEN] = apifly_token
        if static_prefix:
            env_map[STATIC_PREFIX_ENV_VAR] = static_prefix
        cmd_env = os.environ.copy()
        if env:
            cmd_env.update(env_map)
        #final_env.update(env_map)
        # Launch `mlflow run` command as the leader of its own process group so that we can do a
        # best-effort cleanup of all its descendant processes if needed
        return subprocess.Popen(
            arthur_run_arr, env=cmd_env, universal_newlines=True, preexec_fn=os.setsid)

    def _build_arthur_run_cmd(self,runpath='', port=None, workers=None, parameters=None,gunicorn_opts=''):
        """
        Build and return an array containing an ``Arthur run`` command that can be invoked to locally
        run the project at the specified URI.
        Run the Arthur api server, wrapping it in gunicorn
    :param static_prefix: If set, the index.html asset will be served from the path static_prefix.
        If left None, the index.html asset will be served from the root path.
    :return: None
    
        """
        if workers is not None:
            #arthur_run_arr.extend(["-w", str(workers)])
            workers=str(workers)
        else:
            #arthur_run_arr.extend(["-w", '2'])
            workers=str(2)
        if port is not None:
            #arthur_run_arr.extend(["-p", str(port)])
            port=port
        else:
            #arthur_run_arr.extend(["-p", '5002']) 
            port ='5002'

        host ="0.0.0.0"
        bind_address = "%s:%s" % (host, port)
        gunicorn_opts+="--chdir %s"%runpath  #"--chdir ../dep_test/"
        opts = shlex.split(gunicorn_opts) if gunicorn_opts else []
        base_arr=["gunicorn"] + opts + ["-b", bind_address, "-w", "%s" % workers,
                                    "--worker-class","gevent",
                                    "Arthur.core.apiserver.main:app"]
        
        #arthur_run_arr = ["Arthur", "apiserver", "-f", apifuncs,"-h","0.0.0.0"]

        #if not use_conda:
        #    pass
            #mlflow_run_arr.append("--no-conda")
        if parameters is not None:
            for key, value in parameters.items():
                base_arr.extend(["-P", "%s=%s" % (key, value)])
        return base_arr#arthur_run_arr
    def _invoke_arthur_run_subprocess(self,apifuncs,experiment_id, run_id,token='',runpath='',port=None, workers=None, parameters=None,\
                                      gunicorn_opts='',static_prefix=''):
        """
        Run an Arthur project asynchronously by invoking ``Arthur run`` in a subprocess, returning
        a SubmittedRun that can be used to query run status.
        """
        _logger.info("=== Asynchronously launching Arthur run with ID %s ===", run_id)
        arthur_run_arr = self._build_arthur_run_cmd(runpath=runpath,port=port, workers=workers,parameters=parameters,\
                                                   gunicorn_opts=gunicorn_opts)
        print 'arthur_run_arr',arthur_run_arr
        arthur_run_subprocess = self._run_arthur_run_cmd(arthur_run_arr,apifuncs,token,static_prefix=static_prefix)
        return LocalSubmittedRun(run_id, arthur_run_subprocess)
    def run_nohup(self,arthur_run_arr,run_id):
        """
        Run an Arthur project asynchronously by invoking ``Arthur run`` in a subprocess, returning
        a SubmittedRun that can be used to query run status.
        """
        _logger.info("=== Asynchronously launching Arthur run with ID %s ===", run_id)
        arthur_run_subprocess = self._run_arthur_run_cmd(
            [arthur_run_arr])
        return LocalSubmittedRun(run_id, arthur_run_subprocess)