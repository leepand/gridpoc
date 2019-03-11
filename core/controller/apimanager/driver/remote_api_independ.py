import random
from Arthur.core.apiserver.client import Client

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


class RemoteAPI():
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
    def __init__(self, function='def',host='0.0.0.0',port=8001,token=""):
        self.func=''
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

    def handle(self, address, function,input_data,token=''):
        """
        Handles an incoming HTTP connection.
        """
        open_requests=20
        completed_requests=10
        try:
            backend= self.resolve_host(address)
            client = Client(backend,auth_token=token)
            fn = RemoteFunction(client,function)
            predict_out = fn(**input_data)
            response = {"status_code": 200, "body": predict_out}
            return response
        except:
            raise Exception('there is some error when call function %s '%function)
        finally:
            completed_requests+=1
            print 'completed_requests',completed_requests
            #stats_dict['open_requests'] -= 1
            #stats_dict['completed_requests'] = stats_dict.get('completed_requests', 0) + 1
            #stats_dict['bytes_sent'] = stats_dict.get('bytes_sent', 0) + sock.bytes_sent
            #stats_dict['bytes_received'] = stats_dict.get('bytes_received', 0) + sock.bytes_received
test=RemoteAPI() 
test.handle('127.0.0.1:5006', 'fib',{"n":20},token='')