from a_builder.util import bucket_util
from b_trainer.worker import run
from b_trainer.file import training_file_manager
from a_builder.util import util
from e_database import question_and_answer as db_qna
from e_database import chat as db_chat
from e_database import enc_and_dec
from flask import Flask, render_template, request
from flask import jsonify
from c_engine.core.message_manager import message_container
from c_engine.core.schedule_manager import schedule_manager
from c_engine.extension.faq_processor import faq_manager
from c_engine.extension.function_processor import function_adapter
from c_engine.extension.function_processor import fixed_question_processor
from c_engine.extension.image_processor import conv_net
from e_database import notice as db_notice
from e_database import training_config as db_training_config
from d_service import properties

buckets = []
answer_dict_arr = []
answer_num_and_rpsn_question = {}
language = ''
message_count = 0
p_threshold = 0.0
enc_vocab = None
rev_dec_vocab = None

def chat_bot(request): 
    global answer_num_and_rpsn_question, enc_vocab, rev_dec_vocab, language, buckets 
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    language = db_training_config.get_project_language(user, project)
    enc_vocab, rev_dec_vocab = run.init_chatbot(user, project)
    answer_dict = training_file_manager.get_answer_and_answer_num(user, project)
    answer_num_and_rpsn_question = db_chat.get_all_answer_num_and_rpsn_question(user, project)
    answer_dict_arr.append({"user" : user, "project" : project, "answer_dict" : answer_dict})
    buckets = db_training_config.get_bucket(user, project).split(",")
    
    return ''

def chat_window(request):
    user = request.args.get('user')
    project = request.args.get('project')
    res = db_notice.search_notice_list(user, project, '', 'N')
    notice_list = []
    for r in res:
        if util.is_in_date(r['notice_start_date'], r['notice_end_date']):
            notice_list.append(r['notice_content'])
    
    return render_template("chat/chat.html", user = user, project = project, notice_list = str(notice_list))
    
def group_chat(request):
    user = request.args.get('user')
    project = request.args.get('project')
    emno = request.args.get('emno')
    room_name = request.args.get('room_name')
    group_chat_ip = properties.get_group_chat_ip()
    
    return render_template("chat/group_chat.html", user = user, project = project, emno = emno, room_name = room_name, group_chat_ip = group_chat_ip)
    
def create_new_chat_room(request):
    user_ip = request.remote_addr
    user_name = request.form['emno']
    room_name = request.form['room_name']
    room_password = request.form['room_password']
    _, room_nm, _ = db_chat.get_chat_room(room_name)
    res = {'already' : 'N'}
    if room_nm != '':
        res['already'] = 'Y'
    else:
        room_no = db_chat.insert_new_chat_room(room_name, room_password)
        db_chat.insert_new_chat_member(room_no, user_ip, user_name)

    return jsonify(res)

def enter_chat_room(request):
    user_ip = request.remote_addr
    user_name = request.form['emno']
    room_name = request.form['room_name']
    room_password = request.form['room_password']
    room_no, room_name, password = db_chat.get_chat_room(room_name)
    res = {'has_room_name' : 'Y', 'right_password' : 'Y'}
    if room_name == '':
        res['has_room_name'] = 'N'
    elif password != room_password:
        res['right_password'] = 'N'
    else:
        db_chat.insert_new_chat_member(room_no, user_ip, user_name)
    
    return jsonify(res)

def action_principle(request):
    user = request.args.get('user')
    project = request.args.get('project')
    
    return render_template("chat/action_principle.html", user = user, project = project)
    
def get_action_principle(request):
    user = request.form['user']
    project = request.form['project']
    question = request.form['question']
    enc_token_words = run.get_token_words(question)
    enc_token_ids = run.get_token_ids(question, enc_vocab, language)
    dec_token_ids, dec_token_words = run.run_chatbot(enc_vocab, rev_dec_vocab, question, False, language)

    res = {}
    res['enc_token_words'] = str(enc_token_words)
    res['enc_token_ids'] = str(enc_token_ids)
    res['dec_token_words'] = str(dec_token_words)
    res['dec_token_ids'] = str(dec_token_ids)
    
    answer_dict = get_answer_dict(user, project)
    dec_token_words_arr = dec_token_words.split(";")
    answer = ''
    if len(dec_token_words_arr) > 1:
        for i in range(len(dec_token_words_arr)):
            answer += '(' + str(i + 1) + ')\n' + answer_dict[dec_token_words_arr[i]] + '\n'
    else:
        answer = answer_dict[dec_token_words]
    
    res['answer'] = answer
    
    return jsonify(res)
    
def is_chatbot_ready(request):
    is_ready = run.is_chatbot_ready()
    res = {"is_ready" : is_ready}
    
    return jsonify(res)
    
def reply(request):
    user, project = request.form['user'], request.form['project']
    global message_count
    msg, question, image_path, tmp, page, answer_num, right_yn, collect_q, cq_num, cq, schedule_updated, trained_yn = [], request.form['msg'], '', request.form['tmp'], request.form['pge'], '', '', True, 0, [], 'N', True
    mdfc_rgsn_date = ''
    multiple_answer_num = request.form['multiple_answer_num']
    message_count += 1
    function_yn = 'N'
    user_ip = request.remote_addr
    param_holder = ''
    if multiple_answer_num != '':
        msg, tmp = faq_manager.get_answer_in_multiple(multiple_answer_num, question, user, project), ''
        multiple_answer_num = ''
    elif tmp != '':
        msg, tmp, function_nm, param_holder = function_adapter.continue_dialogue(user_ip, question, tmp)
        if function_nm == 'set_my_schedule()':
            schedule_updated = 'Y'
    else:
        param, replacedMsg = function_adapter.get_param_and_replaced_msg(question)
        is_fixed = fixed_question_processor.is_fixed_question(question)
        if is_fixed == False:
            _, answer_num = run.run_chatbot(enc_vocab, rev_dec_vocab, replacedMsg, collect_q, language)
            if answer_num == '':
                _, answer_num = run.run_chatbot(enc_vocab, rev_dec_vocab, replacedMsg + ' ', collect_q, language)
            if len(answer_num.split(";")) > 1:
                answer = ''
                message = faq_manager.get_reserve_question_list(question, answer_num, answer_num_and_rpsn_question)
                msg.append(message)
            else:
                answer, mdfc_rgsn_date = db_chat.get_answer_by_answer_num(user, project, answer_num)
        else:
            answer = fixed_question_processor.get_function_by_question(question)
        multiple_answer_num = ''
        if answer != '':
            if answer[:1] == '$':                
                param[0]['function_nm'] = answer.replace('\n', '').split(" ")[1]
                msg, tmp, function_nm, param_holder = function_adapter.get_message_by_function(param, message_count, 'N')
                function_yn = 'Y'
            else:
                tmp = ''
                multiple_answer_num, multiple_answer = faq_manager.check_multiple_answer(answer_num, user, project)
                if multiple_answer_num != '':
                    msg.append(multiple_answer)
                else:
                    msg, right_yn, image_path, trained_yn = faq_manager.get_faq_answer(user, project, msg, answer_num, answer, question, message_count, mdfc_rgsn_date)
            db_chat.collect_question(user_ip, question, answer_num)
            cq = db_chat.get_same_category_question_list(user, project, answer_num)
            cq_num = len(cq)
    
    num = len(msg)
    res = {'num' : str(num), 'cq_num' : str(cq_num), 'message_count' : message_count, 'qst' : question, 'ans_num' : answer_num, 'image_path' : str(image_path), 'right_yn' : right_yn, 'temp' : tmp, 'page' : page, 'schedule_updated' : schedule_updated, 'multiple_answer_num' : multiple_answer_num}
    res['rpsn_question'] = ''
    res['function_yn'] = function_yn
    res['param_holder'] = param_holder
    if trained_yn == True:
        res['rpsn_question'] = answer_num_and_rpsn_question.get(answer_num, '')    
    for i in range(num):
        res['text' + str(i + 1)] = msg[i]
    for i in range(cq_num):
        res['cq' + str(i + 1)] = cq[i]
    
    return jsonify(res)


def reply_dynamic_popup(request):
    user, project = request.form['user'], request.form['project']
    question = request.form['msg']
    param_holder = eval(request.form['param_holder'])
    _, answer_num = run.run_chatbot(enc_vocab, rev_dec_vocab, question, False, language)
    answer, _ = db_chat.get_answer_by_answer_num(user, project, answer_num)
    param = [param_holder]
    msg = ['']
    if answer[:1] == '$':
        param[0]['function_nm'] = answer.replace('\n', '').split(" ")[1]
        msg, _, _, param_holder = function_adapter.get_message_by_function(param, -1, 'Y')
    
    res = {'text' : msg[0]}
    
    return jsonify(res)

def reply_group_chat(request):
    user, project = request.form['user'], request.form['project']
    question = request.form['msg']
    _, answer_num = run.run_chatbot(enc_vocab, rev_dec_vocab, question, False, language)
    if answer_num == '':
        _, answer_num = run.run_chatbot(enc_vocab, rev_dec_vocab, question + ' ', False, language)
    if len(answer_num.split(";")) > 1:
        answer = '해당 질문에 대한 답변이 하나 이상입니다. 좀더 구체적으로 부탁드립니다!'
    else:
        answer = db_chat.get_answer_by_answer_num(user, project, answer_num)
    res = {'answer' : answer}
    
    return jsonify(res)

def reserve_list(request):
    question = request.form['msg']
    collect_q = False
    _, answer_num = run.run_chatbot(enc_vocab, rev_dec_vocab, question, collect_q, language)
    if answer_num == '':
        _, answer_num = run.run_chatbot(enc_vocab, rev_dec_vocab, question + ' ', collect_q, language)
    q_list = []
    print(question, answer_num)
    answer_num_arr = answer_num.split(";")
    for aa in answer_num_arr:
        q_list.append(answer_num_and_rpsn_question[aa])
    num = len(q_list)
    res = {'num' : str(num)}
    for i in range(num):
        res['text' + str(i + 1)] = q_list[i]
    bucket_id = bucket_util.get_bucket_id_by_sentence(buckets, question)
    res['bucket_id'] = bucket_id
    res['bucket_range'] = ''
    if bucket_id < len(buckets) - 1:
        res['bucket_range'] = buckets[bucket_id] + '~' + str(int(buckets[bucket_id + 1]) - 1)
    else:
        res['bucket_range'] = buckets[bucket_id] + '~∞'

    return jsonify(res)

def get_answer_dict(user, project):
    for i in range(len(answer_dict_arr)):
        if answer_dict_arr[i]['user'] == user and answer_dict_arr[i]['project'] == project:
            answer_dict = answer_dict_arr[i]['answer_dict']
            return answer_dict
    
    return None

def get_request_question(request):
    user, project = request.form['user'], request.form['project']
    gubun = request.form['gubun']
    if gubun == 'my':
        user_ip = request.remote_addr
    else:
        user_ip = ''
    request_question_list = db_chat.get_request_question(user, project, user_ip)
    num = len(request_question_list)
    res = {'num' : str(num)}
    for i in range(num):
        res['rq_num' + str(i + 1)] = str(request_question_list[i]['rq_num'])
    for i in range(num):
        res['question' + str(i + 1)] = request_question_list[i]['question']
    for i in range(num):
        res['recommend_cnt' + str(i + 1)] = str(request_question_list[i]['recommend_cnt'])
    for i in range(num):
        res['pc_status' + str(i + 1)] = str(request_question_list[i]['pc_status'])
    
    return jsonify(res)

def my_question(request):
    user_ip = request.remote_addr
    print(user_ip)
    q_list = db_chat.get_my_question(user_ip)
    num = len(q_list)
    res = {'num' : str(num)}
    for i in range(num):
        res['text' + str(i + 1)] = q_list[i]
    
    return jsonify(res)

def latest_new_question(request):    
    user, project = request.form['user'], request.form['project']
    one_month_ago = util.get_one_month_ago()
    new_question_list = db_qna.get_latest_new_question(user, project, one_month_ago)
    answer_dict = get_answer_dict(user, project)    
    trained_new_question_list = []
    for i in range(len(new_question_list)):
        if answer_dict.get(new_question_list[i]['answer_num']) != None:
            trained_new_question_list.append(new_question_list[i]['rpsn_question'])
    num = len(trained_new_question_list)
    res = {'num' : num}    
    for i in range(num):        
        res['text' + str(i + 1)] = trained_new_question_list[i]
    return jsonify(res)

def latest_question(request):
    user_ip = request.remote_addr
    print(user_ip)
    q_list = db_chat.get_latest_question(user_ip)
    num = len(q_list)
    res = {'num' : str(num)}
    for i in range(num):
        res['text' + str(i + 1)] = q_list[i]
    
    return jsonify(res)

def right_answer(request):
    qst = request.form['qst']
    ans_num = request.form['ans_num']
    db_chat.collect_right_answer(qst, ans_num)
    return ''

def wrong_answer(request):
    qst = request.form['qst']
    ans_num = request.form['ans_num']
    db_chat.collect_wrong_answer(qst, ans_num)
    return ''

def request_new_answer(request):
    user = request.form['user']
    project = request.form['project']
    question = request.form['qst']
    user_ip = request.remote_addr
    db_chat.insert_request_question(user, project, user_ip, question)
    
    return ''

def recommend_request(request):
    user = request.form['user']
    project = request.form['project']
    rq_num = request.form['rq_num']
    db_chat.update_request_question_recommend_cnt(user, project, rq_num)
    
    return ''

def get_schedule(request):
    user_ip = request.remote_addr
    print(request.form['time'])
    my_schedule = schedule_manager.get_schedule(user_ip, request.form['time'])
    
    return jsonify(my_schedule)

def get_all_schedule(request):
    user_ip = request.remote_addr
    res = schedule_manager.get_schedule(user_ip, '')
    
    return jsonify(res)

def send_file(request):
    image_file = request.data
    res = {'text' : ''}
    res['text'] = conv_net.get_text_by_image(image_file)
    return jsonify(res)
