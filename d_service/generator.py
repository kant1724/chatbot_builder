import os
from a_builder.worker import generate
from flask import jsonify
from threading import Thread

def start_generating_all_fragment(request, generator_thread): 
    stop_generating_all_fragment(request, generator_thread)
    user = request.args.get('user')
    project = request.args.get('project')    
    generator = generate.generator()
    thread = Thread(target = generator.generate_all_fragment, args = (user, project))
    thread.start()
    generator_thread.append({"user" : user, "project" : project, "generator" : generator})
    
    return jsonify('')

def stop_generating_all_fragment(request, generator_thread):
    user = request.args.get('user')
    project = request.args.get('project')
    for i in range(len(generator_thread)):
        if generator_thread[i]['user'] == user and generator_thread[i]['project'] == project:
            generator = generator_thread[i]['generator']
            thread = Thread(target = generator.stop)
            thread.start()
            generator_thread.remove(generator_thread[i])
            break
    
    return jsonify('')

def get_generating_all_fragment_info(request, generator_thread):
    user = request.args.get('user')
    project = request.args.get('project')
    root = './a_builder/user'
    f1 = open(os.path.join(root, user, project, 'generate', 'generating_all_fragment_info'), 'r', encoding='utf8')
    generating_all_fragment_info = f1.readline()
    if generating_all_fragment_info == '':
        generating_all_fragment_info = '질문 생성을 준비중입니다..'
    f2 = open(os.path.join(root, user, project, 'generate', 'generating_all_fragment_end_yn'), 'r', encoding='utf8')
    end_yn = f2.readline()
    if end_yn == 'Y':
        stop_generating_all_fragment(request, generator_thread)
    
    return jsonify({'generating_all_fragment_info' : generating_all_fragment_info, 'end_yn' : end_yn})
