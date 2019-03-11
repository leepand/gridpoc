import os,sys
import yaml
from .file_utils import (build_path,exists,mkdir,is_directory,write_yaml,
                        find,read_yaml,list_subdirs,mv,get_parent_dir,_copy_file_or_tree)
from Arthur.core.utils.experiment.experiment import Experiment
from Arthur.core.utils.store.abstract_store import AbstractStore
from Arthur.core.utils.env import get_env
from Arthur.core.utils.entities.ViewType import ViewType
from Arthur.core.entities.base.bs_log import Log

from Arthur.core.utils.experiment.validation import _validate_run_id,_validate_experiment_id
#PY2 = (sys.version_info.major == 2)
#if PY2:
#    from backports import tempfile
#else:
#    import tempfile

_TRACKING_DIR_ENV_VAR = "ARTHUR_TRACKING_DIR"


def _default_root_dir():
    return get_env(_TRACKING_DIR_ENV_VAR) or os.path.abspath("arthur_runs")


class FileStore(AbstractStore):
    TRASH_FOLDER_NAME = ".trash"
    ARTIFACTS_FOLDER_NAME = "artifacts"
    METRICS_FOLDER_NAME = "metrics"
    PARAMS_FOLDER_NAME = "params"
    TAGS_FOLDER_NAME = "tags"
    META_DATA_FILE_NAME = "meta.yaml"

    def __init__(self, root_directory=None, artifact_root_uri=None):
        """
        Create a new FileStore with the given root directory and a given default artifact root URI.
        """
        super(FileStore, self).__init__()
        self.root_directory = root_directory or _default_root_dir()
        self.artifact_root_uri = artifact_root_uri or self.root_directory
        self.trash_folder = build_path(self.root_directory, FileStore.TRASH_FOLDER_NAME)
        # Create root directory if needed
        if not exists(self.root_directory):
            mkdir(self.root_directory)
            #self._create_experiment_with_id(name="Default",
            #                                experiment_id=Experiment.DEFAULT_EXPERIMENT_ID,
            #                                artifact_uri=None)
        # Create trash folder if needed
        if not exists(self.trash_folder):
            mkdir(self.trash_folder)
    def _check_root_dir(self):
        """
        Run checks before running directory operations.
        """
        if not exists(self.root_directory):
            raise Exception("'%s' does not exist." % self.root_directory)
        if not is_directory(self.root_directory):
            raise Exception("'%s' is not a directory." % self.root_directory)
    def _get_experiment_path(self, experiment_id, view_type=ViewType.ALL):
        parents = []
        if view_type == ViewType.ACTIVE_ONLY or view_type == ViewType.ALL:
            parents.append(self.root_directory)
        if view_type == ViewType.DELETED_ONLY or view_type == ViewType.ALL:
            parents.append(self.trash_folder)
        for parent in parents:
            exp_list = find(parent, str(experiment_id), full_path=True)
            if len(exp_list) > 0:
                return exp_list[0]
        return None
       
    def _get_run_dir(self, experiment_id, run_uuid):
        #_validate_run_id(run_uuid)
        if not self._has_experiment(experiment_id):
            return None
        return build_path(self._get_experiment_path(experiment_id), run_uuid)
    def _get_artifact_dir(self, experiment_id, run_uuid):
        #_validate_run_id(run_uuid)
        artifacts_dir = build_path(self.get_experiment(experiment_id).artifact_location,
                                   run_uuid,
                                   FileStore.ARTIFACTS_FOLDER_NAME)
        return artifacts_dir
    def _get_active_experiments(self, full_path=False):
        exp_list = list_subdirs(self.root_directory, full_path)
        return [exp for exp in exp_list if not exp.endswith(FileStore.TRASH_FOLDER_NAME)]

    def _get_deleted_experiments(self, full_path=False):
        return list_subdirs(self.trash_folder, full_path)

    def list_experiments(self, view_type=ViewType.ACTIVE_ONLY):
        self._check_root_dir()
        rsl = []
        if view_type == ViewType.ACTIVE_ONLY or view_type == ViewType.ALL:
            rsl += self._get_active_experiments(full_path=False)
        if view_type == ViewType.DELETED_ONLY or view_type == ViewType.ALL:
            rsl += self._get_deleted_experiments(full_path=False)
        experiments = []
        for exp_id in rsl:
            try:
                # trap and warn known issues, will raise unexpected exceptions to caller
                experiment = self._get_experiment(exp_id, view_type)
                if experiment:
                    experiments.append(experiment)
            except :
                # Trap malformed experiments and log warnings.
                Log.warning("Malformed experiment '%s'. Detailed error" %str(exp_id))
        return experiments

    def _create_experiment_with_id(self, project_path,name, experiment_id, artifact_uri=None):
        self._check_root_dir()
        meta_dir = mkdir(self.root_directory, str(experiment_id))
        artifact_uri = artifact_uri or build_path(self.artifact_root_uri, str(experiment_id))
        experiment = Experiment(experiment_id, name, artifact_uri, Experiment.ACTIVE_LIFECYCLE)
        write_yaml(meta_dir, FileStore.META_DATA_FILE_NAME, dict(experiment))
        #copy project files to experiment path from web source
        _copy_file_or_tree(project_path,artifact_uri,dst_dir=name)
        return experiment_id

    def create_experiment(self, project_path,name, artifact_location=None):
        self._check_root_dir()
        if name is None or name == "":
            raise Exception("Invalid experiment name '%s'" % name)
        experiment = self.get_experiment_by_name(name)
        if experiment is not None:
            raise Exception("Experiment '%s' already exists." % experiment.name)
        # Get all existing experiments and find the one with largest ID.
        # len(list_all(..)) would not work when experiments are deleted.
        experiments_ids = [e.experiment_id for e in self.list_experiments(ViewType.ALL)]
        experiment_id = max(experiments_ids) + 1 if experiments_ids else 0
        return self._create_experiment_with_id(project_path,name, experiment_id, artifact_location)

    def _has_experiment(self, experiment_id):
        return self._get_experiment_path(experiment_id) is not None 
    def get_experiment(self, experiment_id):
        """
        Fetches the experiment. This will search for active as well as deleted experiments.
        :param experiment_id: Integer id for the experiment
        :return: A single Experiment object if it exists, otherwise raises an Exception.
        """
        experiment = self._get_experiment(experiment_id)
        if experiment is None:
            raise Exception("Experiment '%s' does not exist." % experiment_id)
        return experiment
    def get_experiment_by_name(self, name):
        self._check_root_dir()
        for experiment in self.list_experiments(ViewType.ALL):
            if experiment.name == name:
                return experiment
        return None
    def _get_experiment(self, experiment_id, view_type=ViewType.ALL):
        self._check_root_dir()
        _validate_experiment_id(experiment_id)
        experiment_dir = self._get_experiment_path(experiment_id, view_type)
        if experiment_dir is None:
            raise Exception("Could not find experiment with ID %s" % experiment_id)
        meta = read_yaml(experiment_dir, FileStore.META_DATA_FILE_NAME)
        if experiment_dir.startswith(self.trash_folder):
            meta['lifecycle_stage'] = Experiment.DELETED_LIFECYCLE
        else:
            meta['lifecycle_stage'] = Experiment.ACTIVE_LIFECYCLE
        experiment = Experiment.from_dictionary(meta)
        if int(experiment_id) != experiment.experiment_id:
            logging.warning("Experiment ID mismatch for exp %s. ID recorded as '%s' in meta data. "
                            "Experiment will be ignored.",
                            str(experiment_id), str(experiment.experiment_id), exc_info=True)
            return None
        return experiment
    def delete_experiment(self, experiment_id):
        experiment_dir = self._get_experiment_path(experiment_id, ViewType.ACTIVE_ONLY)
        if experiment_dir is None:
            raise Exception("Could not find experiment with ID %s" % experiment_id)
        mv(experiment_dir, self.trash_folder)
    def restore_experiment(self, experiment_id):
        experiment_dir = self._get_experiment_path(experiment_id, ViewType.DELETED_ONLY)
        if experiment_dir is None:
            raise Exception("Could not find deleted experiment with ID %d" % experiment_id)
        conflict_experiment = self._get_experiment_path(experiment_id, ViewType.ACTIVE_ONLY)
        if conflict_experiment is not None:
            raise Exception(
                    "Cannot restore eperiment with ID %d. "
                    "An experiment with same ID already exists." % experiment_id)
        mv(experiment_dir, self.root_directory)
    def rename_experiment(self, experiment_id, new_name):
        meta_dir = os.path.join(self.root_directory, str(experiment_id))
        # if experiment is malformed, will raise error
        experiment = self._get_experiment(experiment_id)
        if experiment is None:
            raise Exception("Experiment '%s' does not exist." % experiment_id)
        experiment._set_name(new_name)
        if experiment.lifecycle_stage != Experiment.ACTIVE_LIFECYCLE:
            raise Exception("Cannot rename experiment in non-active lifecycle stage."
                            " Current stage: %s" % experiment.lifecycle_stage)
        write_yaml(meta_dir, FileStore.META_DATA_FILE_NAME, dict(experiment), overwrite=True)
    def _find_experiment_folder(self, run_path):
        """
        Given a run path, return the parent directory for its experiment.
        """
        parent = get_parent_dir(run_path)
        if os.path.basename(parent) == FileStore.TRASH_FOLDER_NAME:
            return get_parent_dir(parent)
        return parent
#test=FileStore()
#test._get_experiment_path(0)
#test._get_run_dir(0,'110')
#test._get_artifact_dir(0,'110')
#test._get_active_experiments()
#test._get_deleted_experiments()
#test.list_experiments()
#test._create_experiment_with_id('leepand',4)
#test.create_experiment('arthur')
#test.delete_experiment(4)
#test.restore_experiment(4)
#test.rename_experiment(5,'arthur_new')
#test._find_experiment_folder('../')
#test.list_experiments()
#test.create_experiment('../tttt','arthur')
#_copy_file_or_tree('../tttt','arthur_runs/',dst_dir='code')