import random
from Arthur.core.apiserver.client import Client
from Arthur.core.entities.base.bs_log import Log
from .redis_api import storage,CountApi

class data_api(object):
    def __init__(self,redis_host='127.0.0.1',
                 redis_port=6379,redis_db=5,
                 directory="."):

        self.redis_host=redis_host
        self.redis_port=redis_port
        self.redis_db=redis_db
    def countvisit(self,prefix='arthurService:'):
        store=storage('redis', flush_db=False, host=self.redis_host, port=self.redis_port, db= self.redis_db)
        return CountApi(store,prefix)

class ArthurflyError(Exception):
    pass
def RemoteFunction(client, func_name):
    def wrapped(*args, **kwargs):
        if args:
            raise ArthurflyError('Arthur service functions only accept named arguments')
        return client.call_func(func_name, **kwargs)
    wrapped.__name__ = func_name
    wrapped.__qualname__ = func_name
    wrapped.__doc__ = client.get_doc(func_name)
    return wrapped


class RemoteAPIDriver(object):
    """API for Accessing Arthur Services
    Parameters
    ----------
    remote ip: str
        model service remote path(host/ports)
    service function: str
        predict function
    input data: json
        post data to get model predict result
    api_key/token : str
        credentials to access remote
    Attributes
    ----------
    Methods
    -------
    post_data(input_data)
        post single data point to Arthur scoped by model
    get_data(filter)
        get data information from Arthur scoped by filter
    update_actual(id, actual)
        update the data id with actual values (y_hat)
    get_deployment_info()
        returns deployment info from Arthur deployed models
    """
    def __init__(self, root,arthur_directory_name):
        self.func=''
        self.request_cnt = data_api().countvisit()
    def get_service_key(self, service_name=None, host=None,
                              port=None, address=None,service=None):
        name = service_name or service.name
        #port = port or service.port
        #host = host or service.host
        #k = 'completed_requests:%s:%s:%s' % (name,host,port) or 'completed_requests:%s:%s' % (name,address)
        k = 'completed_requests:%s:%s' % (name,address)
        #print 'get_service_key: %s' % k
        Log.info('get_service_key: %s' % k)
        return k
    @staticmethod    
    def resolve_host(address, protocol="http"):
        # Check for an exact or any subdomain matches
        if isinstance(address,list):
            if len(address)>0:
                backend = random.choice(address)
                return "%s://" % protocol + backend
            else:
                raise Exception('please give remote address')
        else:
            return "%s://" % protocol + address 
    def get_completed_requests(self,function,address):
        completed_requests_key=self.get_service_key(service_name=function, address=address)
        return self.request_cnt[completed_requests_key]
    def get_service_metadata(self,address,token=''):
        response = {"status_code": 200}        
        try:
            backend= self.resolve_host(address)
            client = Client(backend,auth_token=token)
            fn=getattr(client,'_get_metadata')
            response['body']=fn()
            
        except:
            response = {"status_code": 500}    
            response['body']='None service metadata found!!!'
        return response
    def handle(self, address, function,input_data,token=''):
        """
        Handles an incoming HTTP connection.
        """
        open_requests=20
        completed_requests=10
        response = {"status_code": 200}
        try:
            backend= self.resolve_host(address)
            client = Client(backend,auth_token=token)
            fn = RemoteFunction(client,function)
            predict_out = fn(**input_data)
            response = {"status_code": 200, "body": predict_out}
        except:
            #raise Exception('there is some error when call function %s '%function)
            response['status_code'] = 500
        finally:
            completed_requests_key=self.get_service_key(service_name=function, address=address)
            #print completed_requests_key
            self.request_cnt[completed_requests_key]=1
            #completed_requests+=1
            #print 'completed_requests',completed_requests
            #stats_dict['open_requests'] -= 1
            #stats_dict['completed_requests'] = stats_dict.get('completed_requests', 0) + 1
            #stats_dict['bytes_sent'] = stats_dict.get('bytes_sent', 0) + sock.bytes_sent
            #stats_dict['bytes_received'] = stats_dict.get('bytes_received', 0) + sock.bytes_received
        return response
#test=RemoteAPI() 
#test.handle('127.0.0.1:5006', 'fib',{"n":20},token='')