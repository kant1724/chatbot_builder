from e_database import training_config as db_training_config
from e_database import chatbot_config as db_chatbot_config
from b_trainer.worker import connect_tensorflow as ct
from flask import jsonify

def submit_training_config(request):
    req_dict = eval(request.data.decode('utf8'))
    for i in range(len(req_dict)):
        user = req_dict[i]['user']
        project = req_dict[i]['project']
        config_name = req_dict[i]['config_name']
        config_value = req_dict[i]['config_value']
        db_training_config.update_training_config(user, project, config_name, config_value)
    
    training_config = db_training_config.search_training_config(user, project)
    config_data = {"user" : user, "project" : project}
    for i in range(len(training_config)):
        config_data[training_config[i]['config_name']] = training_config[i]['config_value']
    
    ct.update_training_config(config_data)
    
    return jsonify('')

def submit_chatbot_config(request):
    req_dict = eval(request.data.decode('utf8'))
    for i in range(len(req_dict)):
        user = req_dict[i]['user']
        project = req_dict[i]['project']
        config_name = req_dict[i]['config_name']
        config_value = req_dict[i]['config_value']
        db_chatbot_config.update_chatbot_config(user, project, config_name, config_value)
    
    return jsonify('')
