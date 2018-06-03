import requests
import json
from d_service import properties

file_ip = properties.get_file_ip()

def send_training_data(user, project, answer_dict, question_and_answer_num, fragment_and_answer_num):
    url = 'http://' + file_ip + '/upload_training_data'
    requests.post(url, data={"user" : user, "project" : project, "answer_dict" : answer_dict, "question_and_answer_num" : question_and_answer_num, "fragment_and_answer_num" : fragment_and_answer_num})

def get_training_data(user, project):
    url = 'http://' + file_ip + '/get_training_data'
    response = requests.post(url, data={"user" : user, "project" : project})
    return json.loads(response.content.decode('utf8'))

def send_compression_tag_training_data(user, project, expression_and_tag_name):
    url = 'http://' + file_ip + '/upload_compression_tag_training_data'
    requests.post(url, data={"user" : user, "project" : project, "expression_and_tag_name" : expression_and_tag_name})

def get_compression_tag_training_data(user, project):
    url = 'http://' + file_ip + '/get_compression_tag_training_data'
    response = requests.post(url, data={"user" : user, "project" : project})
    return json.loads(response.content.decode('utf8'))
