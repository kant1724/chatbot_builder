import os
from a_builder.worker import update
from a_builder.util import voca_util
from flask import jsonify
from threading import Thread
from c_engine.core.error_detector import sentence_comparator as sc

def start_updating(request, updater_thread): 
    stop_updating(request, updater_thread)
    user = request.args.get('user')
    project = request.args.get('project')    
    updater = update.updater()
    thread = Thread(target = updater.update_question_voca, args = ('', user, project, 'Y'))
    thread.start()
    updater_thread.append({"user" : user, "project" : project, "updater" : updater})
    
    return jsonify('')

def stop_updating(request, updater_thread):
    user = request.args.get('user')
    project = request.args.get('project')
    for i in range(len(updater_thread)):
        if updater_thread[i]['user'] == user and updater_thread[i]['project'] == project:
            updater = updater_thread[i]['updater']
            thread = Thread(target = updater.stop)
            thread.start()
            updater_thread.remove(updater_thread[i])
            break
    
    return jsonify('')

def get_updating_info(request, updater_thread):
    user = request.args.get('user')
    project = request.args.get('project')
    root = './a_builder/user'
    f1 = open(os.path.join(root, user, project, 'update', 'updating_info'), 'r', encoding='utf8')
    updating_info = f1.readline()
    if updating_info == '':
        updating_info = '업데이트를 준비중입니다..'
    f2 = open(os.path.join(root, user, project, 'update', 'updating_end_yn'), 'r', encoding='utf8')
    end_yn = f2.readline()
    if end_yn == 'Y':
        stop_updating(request, updater_thread)
    
    return jsonify({'updating_info' : updating_info, 'end_yn' : end_yn})

def update_voca_synonym(request):
    sc.result = None
    voca_util.update_voca_synonym()

    return jsonify('')

def update_question_voca(request):
    sc.result = None
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    answer_num = req_dict['answer_num']
    updater = update.updater()
    updater.update_question_voca(answer_num, user, project, 'N')
    
    return jsonify('')
