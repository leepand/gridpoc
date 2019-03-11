import logging
import os
import subprocess
from submitted_run import LocalSubmittedRun

_logger = logging.getLogger(__name__)
class model_publish(object):
    def _run_arthur_run_cmd(self,arthur_run_arr, env_map={}):
        """
        Invoke ``arthur run`` in a subprocess, which in turn runs the entry point in a child process.
        Returns a handle to the subprocess. Popen launched to invoke ``arthur run``.
        """
        final_env = os.environ.copy()
        #final_env.update(env_map)
        # Launch `mlflow run` command as the leader of its own process group so that we can do a
        # best-effort cleanup of all its descendant processes if needed
        return subprocess.Popen(
            arthur_run_arr, env=final_env, universal_newlines=True, preexec_fn=os.setsid)

    def _build_arthur_run_cmd(self, apifuncs,token='',runpath='', port=None, workers=None, parameters=None):
        """
        Build and return an array containing an ``Arthur run`` command that can be invoked to locally
        run the project at the specified URI.
        """
        arthur_run_arr = ["Arthur", "apiserver", "-f", apifuncs,"-h","0.0.0.0"]
        if workers is not None:
            arthur_run_arr.extend(["-w", str(workers)])
        else:
            arthur_run_arr.extend(["-w", '2'])
        if port is not None:
            arthur_run_arr.extend(["-p", str(port)])
        else:
            arthur_run_arr.extend(["-p", '5002']) 
        if token:
            arthur_run_arr.extend(["-t", token]) 
        if runpath:
            arthur_run_arr.extend(["--gunicorn-opts", "--chdir %s"%runpath])#"--chdir ../dep_test/"
        #if not use_conda:
        #    pass
            #mlflow_run_arr.append("--no-conda")
        if parameters is not None:
            for key, value in parameters.items():
                arthur_run_arr.extend(["-P", "%s=%s" % (key, value)])
        return arthur_run_arr
    def _invoke_arthur_run_subprocess(self,apifuncs,experiment_id, run_id,token='',runpath='',port=None, workers=None, parameters=None):
        """
        Run an Arthur project asynchronously by invoking ``Arthur run`` in a subprocess, returning
        a SubmittedRun that can be used to query run status.
        """
        _logger.info("=== Asynchronously launching Arthur run with ID %s ===", run_id)
        arthur_run_arr = self._build_arthur_run_cmd(
            apifuncs=apifuncs,token=token, runpath=runpath,port=port, workers=workers,parameters=parameters)
        #print ' '.join(arthur_run_arr)
        arthur_run_subprocess = self._run_arthur_run_cmd(
            arthur_run_arr)
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