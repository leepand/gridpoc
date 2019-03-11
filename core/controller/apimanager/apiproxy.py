from Arthur.core.controller.base import BaseController
from Arthur.core.entities.base.bs_log import Log
from Arthur.core.utils.exceptions import (RemoteApiInitError)


class RemoteAPIController(BaseController):
    """CodeController inherits from BaseController and manages business logic related to the
    code.
    Methods
    -------
    create(code_id=None)
        create a code object within the project
    list()
        list all code objects within the project
    delete(id)
        delete the specified code object from the project
    """

    def __init__(self):
        try:
            super(RemoteAPIController, self).__init__()
        except RemoteApiInitError:
            Log.warning("warn", "controller.apicontrol.init.failed")
    def post_data(self,input_data,address='127.0.0.1:5006',function='fib',token=''):
        """Run post request and gather result and return to user
        Returns
        -------
        prediction
            prediction result
        
        """
        response = self.remote_api_driver.handle(address, function,input_data,token)
        #self.check_unstaged_changes()
        # Return the code object with this hash id
        return response
    def get_completed_requests(self,function,address):
        """Get the request counts of service/project
        Returns
        -------
        requests
            post requests of service
        """
        response = {"status_code": 200}
        try:
            response = {"status_code": 200, "body": self.remote_api_driver.get_completed_requests(function,address)}
        except:
            response['status_code'] = 500
        # Return the code object with this hash id
        return response

    def get_deployment_info(self,address,token=''):
        # run get request with the filters (using Arthur client) and gather and return results
        response = self.remote_api_driver.get_service_metadata(address,token)
        return response
    
    