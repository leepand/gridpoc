# -*- coding: UTF-8 -*-

# author: leepand
# time: 2019-02-21
# desc: control base
import os

from Arthur.core.entities.base.bs_log import Log
from Arthur.core.utils.dynamically_load_class import get_class_contructor
from Arthur.core.utils.json_store import JSONStore
from Arthur.core.utils.exceptions import (InvalidProjectPath)
from Arthur.config import Config


class BaseController(object):
    """BaseController is used to setup the repository. It serves as the basis for all other Controller objects
    Parameters
    ----------
    home : str, optional
        directory for the project, default is to pull from config
    Attributes
    ----------
    home : str
        absolute filepath for the location of the project
    config : JSONStore
        this is the set of configurations used to create a project
    dal : datmo.core.storage.DAL
    model : datmo.core.entity.model.Model
    code_driver : datmo.core.controller.code.driver.CodeDriver
    file_driver : datmo.core.controller.file.driver.FileDriver
    environment_driver : datmo.core.controller.environment.driver.EnvironmentDriver
    is_initialized : bool
    Methods
    -------
    dal_instantiate()
        Instantiate a version of the DAL
    set_config_value(key, default_value)
        Returns value adn sets to default if no value present
    config_loader(key)
        Return the config dictionary based on key
    get_config_defaults()
        Return the configuration defaults
    """

    def __init__(self, home=None):
        self.home = Config().home if not home else home
        #if not os.path.isdir(self.home):
        #    raise InvalidProjectPath(
        #        __("error", "controller.base.__init__", self.home))
        self.logger = Log
        # property caches and initial values
        self._is_initialized = False
        self._dal = None
        self._model = None
        self._remoteApi_driver = None
        self._file_driver = None
        self._environment_driver = None

    @property
    def remote_api_driver(self):
        if self._remoteApi_driver == None:
            module_details = self.config_loader("controller.remoteapi.driver")
            self._remoteApi_driver = module_details["constructor"](
                **module_details["options"])
        return self._remoteApi_driver
    @property
    def abtesting_client_driver(self):
        if self._abtestingclient_driver == None:
            module_details = self.config_loader("controller.abtestingclient.driver")
            self._abtestingclient_driver = module_details["constructor"](
                **module_details["options"])
        return self._abtestingclient_driver
    @property
    # Controller objects are only in sync if the data drivers are the same between objects
    # Currently pass dal_driver down from controller to controller to ensure syncing dals
    # TODO: To fix dal from different controllers so they sync within one session; they do NOT currently
    def dal(self):
        if self._dal == None:
            dal_dict = self.config_loader("storage.local")
            self._dal = dal_dict["constructor"](**dal_dict["options"])
        return self._dal

    @property
    def is_initialized(self):
        if not self._is_initialized:
            if self.file_driver.is_initialized and \
                self.dal.is_initialized and \
                self.code_driver.is_initialized and \
                self.environment_driver.is_initialized and \
                self.model:
                self._is_initialized = True
        return self._is_initialized

    @property
    def model(self):
        if not self.dal.is_initialized:
            self._model = None
        else:
            models = self.dal.model.query({})
            self._model = models[0] if models else None
        return self._model

    def config_loader(self, key):
        defaults = self.get_config_defaults()
        module_details = defaults[key]
        module_details["constructor"] = get_class_contructor(
            module_details["class_constructor"])
        return module_details

    def get_config_defaults(self):
        return {
            "controller.remoteapi.driver": {
                "class_constructor":
                    "Arthur.core.controller.apimanager.driver.remote_api_depend.RemoteAPIDriver",
                "options": {
                    "root": self.home,
                    "arthur_directory_name": Config().arthur_directory_name
                }
            },
            " controller.abtestingclient.driver": {
                "class_constructor":
                    "Arthur.core.controller.abtesting.driver.abtesting_client.SessionDriver",
                "options": {
                    "host": 'http://localhost:5001',
                    "timeout": 0.5
                }
            },
        
        }