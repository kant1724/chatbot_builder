import requests
import json
from d_service import properties
external_adapter_ip = properties.get_external_adapter_ip()

def send_function_and_param(function_name, param, message_count, this_yn):
    url = 'http://' + external_adapter_ip  + '/send_function_and_param'
    response = requests.post(url, data={"function_name" : function_name, "param" : str(param), "message_count" : str(message_count), "this_yn" : this_yn})
    
    return json.loads(response.content.decode('utf8'))
