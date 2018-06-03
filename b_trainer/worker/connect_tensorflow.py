import requests
import json
from d_service import properties

tf_ip = properties.get_tf_ip()
tf_compression_tag_ip = properties.get_tf_compression_tag_ip()

def update_training_config(config_data):
    url = 'http://' + tf_ip + '/update_training_config'
    requests.post(url, data=config_data)

def init_chatbot(user, project):
    url = 'http://' + tf_ip + '/init_chatbot'
    response = requests.post(url, data={"user" : user, "project" : project})
    return json.loads(response.content.decode('utf8'))

def is_chatbot_ready():
    url = 'http://' + tf_ip + '/is_chatbot_ready'
    response = requests.post(url, data={})
    return json.loads(response.content.decode('utf8'))

def run_chatbot(token_ids):
    url = 'http://' + tf_ip + '/run_chatbot'
    response = requests.post(url, data={"token_ids" : str(token_ids)})
    return json.loads(response.content.decode('utf8'))

def init_compression_tag(user, project):
    project += '_compression_tag'
    url = 'http://' + tf_compression_tag_ip + '/init_chatbot'
    response = requests.post(url, data={"user" : user, "project" : project})
    return json.loads(response.content.decode('utf8'))

def run_compression_tag(token_ids):
    url = 'http://' + tf_compression_tag_ip + '/run_chatbot'
    response = requests.post(url, data={"token_ids" : str(token_ids)})
    return json.loads(response.content.decode('utf8'))

def start_training(user, project, saving_step, train_enc_ids, train_dec_ids):
    url = 'http://' + tf_ip + '/start_training'
    requests.post(url, data={"user" : user, "project" : project, "saving_step" : saving_step, "train_enc_ids" : str(train_enc_ids), "train_dec_ids" : str(train_dec_ids)})

def stop_training(user, project):
    url = 'http://' + tf_ip + '/stop_training'
    requests.post(url, data={"user" : user, "project" : project})

def get_training_info(user, project):
    url = 'http://' + tf_ip + '/get_training_info'
    response = requests.post(url, data={"user" : user, "project" : project})
    return json.loads(response.content.decode('utf8'))

def is_training(user, project):
    url = 'http://' + tf_ip + '/is_training'
    response = requests.post(url, data={"user" : user, "project" : project})
    return json.loads(response.content.decode('utf8'))

def is_running(user, project):
    url = 'http://' + tf_ip + '/is_running'
    response = requests.post(url, data={"user" : user, "project" : project})
    return json.loads(response.content.decode('utf8'))

def delete_ckpt(user, project):
    url = 'http://' + tf_ip + '/delete_ckpt'
    requests.post(url, data={"user" : user, "project" : project})

def send_training_test_question(user, project, token_ids):
    url = 'http://' + tf_ip + '/training_test'
    response = requests.post(url, data={"user" : user, "project" : project, "token_ids" : str(token_ids)})
    return json.loads(response.content.decode('utf8'))

def start_compression_tag_training(user, project, saving_step, train_enc_ids, train_dec_ids):
    project += '_compression_tag'
    url = 'http://' + tf_compression_tag_ip + '/start_training'
    requests.post(url, data={"user" : user, "project" : project, "saving_step" : saving_step, "train_enc_ids" : str(train_enc_ids), "train_dec_ids" : str(train_dec_ids)})

def stop_compression_tag_training(user, project):
    project += '_compression_tag'
    url = 'http://' + tf_compression_tag_ip + '/stop_training'
    requests.post(url, data={"user" : user, "project" : project})

def get_compression_tag_training_info(user, project):
    project += '_compression_tag'
    url = 'http://' + tf_compression_tag_ip + '/get_training_info'
    response = requests.post(url, data={"user" : user, "project" : project})
    return json.loads(response.content.decode('utf8'))

def is_compression_tag_training(user, project):
    project += '_compression_tag'
    url = 'http://' + tf_compression_tag_ip + '/is_training'
    response = requests.post(url, data={"user" : user, "project" : project})
    return json.loads(response.content.decode('utf8'))

def is_compression_tag_running(user, project):
    project += '_compression_tag'
    url = 'http://' + tf_compression_tag_ip + '/is_running'
    response = requests.post(url, data={"user" : user, "project" : project})
    return json.loads(response.content.decode('utf8'))

def delete_compression_tag_ckpt(user, project):
    project += '_compression_tag'
    url = 'http://' + tf_compression_tag_ip + '/delete_ckpt'
    requests.post(url, data={"user" : user, "project" : project})
