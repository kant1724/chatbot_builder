from b_trainer.worker import train
from b_trainer.file import training_file_manager
from flask import jsonify

answer_dict_arr = []

def delete_ckpt_file(request): 
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    train.delete_ckpt(user, project)

    return jsonify('')

def start_training(request): 
    user = request.form['user']
    project = request.form['project']
    saving_step = request.form['saving_step']
    train.train(user, project, saving_step)
    
    return jsonify('')

def stop_training(request): 
    user = request.form['user']
    project = request.form['project']
    train.stop(user, project)
    
    return jsonify('')

def get_training_info(request): 
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    training_info, saving_step = train.get_training_info(user, project)
    if training_info == '':
        training_info = '훈련을 준비중입니다..'
    
    return jsonify({'training_info' : training_info, 'saving_step' : saving_step})

def get_is_training(request):
    user = request.form['user']
    project = request.form['project']
    is_training = train.is_training(user, project)
    return jsonify({"is_training" : is_training})
    
def send_training_test_question(request):
    user = request.form['user']
    project = request.form['project']
    question = request.form['question']
    answer_num = train.send_training_test_question(user, project, question)
    answer_dict = None
    for answer_dict_ele in answer_dict_arr:
        if answer_dict_ele['user'] == user and answer_dict_ele['project'] == project:
            answer_dict = answer_dict_ele['answer_dict']
            break
    if answer_dict == None:
        answer_dict = training_file_manager.get_answer_and_answer_num(user, project)
        answer_dict_arr.append({"user" : user, "project" : project, "answer_dict" : answer_dict})
    answer = answer_dict[answer_num]
    
    return jsonify({'answer' : answer})

def delete_compression_tag_ckpt_file(request): 
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    train.delete_compression_tag_ckpt(user, project)

    return jsonify('')

def start_compression_tag_training(request):
    user = request.form['user']
    project = request.form['project']
    saving_step = request.form['saving_step']
    train.compression_tag_train(user, project, saving_step)
    
    return jsonify('')

def stop_compression_tag_training(request): 
    user = request.form['user']
    project = request.form['project']
    train.compression_tag_stop(user, project)
    
    return jsonify('')

def get_compression_tag_training_info(request): 
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    training_info, saving_step = train.get_compression_tag_training_info(user, project)
    if training_info == '':
        training_info = '훈련을 준비중입니다..'
    
    return jsonify({'training_info' : training_info, 'saving_step' : saving_step})

def get_is_compression_tag_training(request):
    user = request.form['user']
    project = request.form['project']
    is_training = train.is_compression_tag_training(user, project)
    return jsonify({"is_training" : is_training})
    