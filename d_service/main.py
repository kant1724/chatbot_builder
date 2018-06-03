from flask import Flask, render_template, request, jsonify
from b_trainer.worker import train

def my_page_main(request):
    user = request.args.get('user')
    project = request.args.get('project')
    emno = request.args.get('emno')
    user_ip = request.remote_addr
    return render_template("main/my_page_main.html", user = user, project = project, emno = emno, user_ip = user_ip)

def qna_main(request):
    user = request.args.get('user')
    project = request.args.get('project')
    return render_template("main/qna_main.html", user = user, project = project)

def bucket_manager_main(request):
    user = request.args.get('user')
    project = request.args.get('project')
    return render_template("main/bucket_manager_main.html", user = user, project = project)

def compression_tag_main(request):
    user = request.args.get('user')
    project = request.args.get('project')
    is_training = train.is_compression_tag_training(user, project)
    return render_template("main/compression_tag_main.html", user = user, project = project, is_training = is_training)

def notice_manager_main(request):
    user = request.args.get('user')
    project = request.args.get('project')
    return render_template("main/notice_manager_main.html", user = user, project = project)

def train_main(request): 
    user = request.args.get('user')
    project = request.args.get('project')
    is_training = train.is_training(user, project)
    return render_template("main/train_main.html", user = user, project = project, is_training = is_training)

def update_question_voca_main(request, updater_thread): 
    user = request.args.get('user')
    project = request.args.get('project')
    is_update = 'N'
    for i in range(len(updater_thread)):
        if updater_thread[i]['user'] == user and updater_thread[i]['project'] == project:
            is_update = 'Y'
            break
    return render_template("main/update_question_voca_main.html", user = user, project = project, is_updating = is_update)

def synonym_manager_main(request): 
    return render_template("main/synonym_manager_main.html")

def voca_manager_main(request): 
    return render_template("main/voca_manager_main.html")

def category_manager_main(request): 
    return render_template("main/category_manager_main.html")

def error_detection_main(request):
    user = request.args.get('user')
    project = request.args.get('project')
    return render_template("main/error_detection_main.html", user = user, project = project)

def question_generator_main(request, generator_thread):
    user = request.args.get('user')
    project = request.args.get('project')
    is_generate_all_fragment = 'N'
    for i in range(len(generator_thread)):
        if generator_thread[i]['user'] == user and generator_thread[i]['project'] == project:
            is_generate_all_fragment = 'Y'
            break
    
    return render_template("main/question_generator_main.html", user = user, project = project, is_generating_all_fragment = is_generate_all_fragment)

def new_request_main(request):
    user = request.args.get('user')
    project = request.args.get('project')
    return render_template("main/new_request_main.html", user = user, project = project)

def chatbot_config_main(request):
    user = request.args.get('user')
    project = request.args.get('project')
    return render_template("main/chatbot_config_main.html", user = user, project = project)

def training_test_main(request):
    user = request.args.get('user')
    project = request.args.get('project')
    return render_template("main/training_test_main.html", user = user, project = project)

def error_statistics_main(request):
    user = request.args.get('user')
    project = request.args.get('project')
    return render_template("main/error_statistics_main.html", user = user, project = project)

def loading(request):
    user = request.form['user']
    project = request.form['project']
    emno = request.form['emno']
    room_name = request.form['room_name']
    gubun = request.form['gubun']
    return render_template("chat/loading.html", user = user, project = project, emno = emno, room_name = room_name, gubun = gubun)
