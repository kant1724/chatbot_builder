from flask import Flask, render_template, request
from d_service import properties
from e_database import notice as db_notice

def easy_manager_pop(request):
    user = request.args.get('user')
    project = request.args.get('project')
    return render_template("popup/easy_manager_pop.html", user = user, project = project)

def new_answer_pop(request):
    user = request.args.get('user')
    project = request.args.get('project')
    rq_num = request.args.get('rq_num')
    if rq_num == None:
        rq_num = ''
    return render_template("popup/new_answer_pop.html", user = user, project = project, rq_num = rq_num)

def multiple_answer_pop(request):
    user = request.args.get('user')
    project = request.args.get('project')
    answer_num = request.args.get('answer_num')
    return render_template("popup/multiple_answer_pop.html", user = user, project = project, answer_num = answer_num)

def add_image_pop(request):
    user = request.args.get('user')
    project = request.args.get('project')
    answer_num = request.args.get('answer_num')
    return render_template("popup/add_image_pop.html", user = user, project = project, answer_num = answer_num, file_ip = properties.get_file_ip())

def new_function_pop(request):
    user = request.args.get('user')
    project = request.args.get('project')
    return render_template("popup/new_function_pop.html", user = user, project = project)

def new_question_pop(request): 
    user = request.args.get('user')
    project = request.args.get('project')
    answer_num = request.args.get('answer_num')
    return render_template("popup/new_question_pop.html", user = user, project = project, ans_num = answer_num)

def new_tag_pop(request): 
    return render_template("popup/new_tag_pop.html")

def new_synonym_pop(request): 
    return render_template("popup/new_synonym_pop.html")

def new_notice_pop(request): 
    user = request.args.get('user')
    project = request.args.get('project')
    gubun = request.args.get('gubun')
    notice_num = request.args.get('notice_num')
    notice_subject = ''
    notice_content = ''
    notice_start_date = ''
    notice_end_date = ''
    if gubun == 'modify':
        res = db_notice.search_notice_list_by_notice_num(user, project, notice_num)
        notice_subject = res['notice_subject']
        notice_content = res['notice_content']
        notice_start_date = res['notice_start_date']
        notice_end_date = res['notice_end_date']
        
    return render_template("popup/new_notice_pop.html", user = user, project = project, gubun = gubun, notice_num = notice_num, notice_subject = notice_subject, notice_content = notice_content, notice_start_date = notice_start_date, notice_end_date = notice_end_date)

def modify_answer_pop(request): 
    user = request.form['modify_user']
    project = request.form['modify_project']
    answer_num = request.form['modify_answer_num']
    rpsn_question = request.form['modify_rpsn_question']
    answer = request.form['modify_answer']
    return render_template("popup/modify_answer_pop.html", user = user, project = project, answer_num = answer_num, rpsn_question = rpsn_question, answer = answer)
