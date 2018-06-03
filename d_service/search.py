from e_database import question_and_answer as qna
from e_database import compression_tag as db_compression_tag
from e_database import multiple_answer as db_multiple_answer
from e_database import tag as db_tag
from e_database import voca as db_voca
from e_database import synonym as db_synonym
from e_database import category as db_category
from e_database import new_request as db_new_request
from e_database import training_config as db_training_config
from e_database import chatbot_config as db_chatbot_config
from e_database import notice as db_notice
from e_database import statistics as db_statistics
from a_builder.util import voca_util
from a_builder.util import bucket_util
from flask import jsonify

def search_answer(request):    
    req_dict = eval(request.data.decode('utf8'))
    subject = req_dict['subject']
    user = req_dict['user']
    gubun = req_dict['gubun']
    project = req_dict['project']
    res = qna.search_answer(gubun, subject, user, project)
    
    return jsonify(results = res)

def search_answer_by_answer_num(request):
    req_dict = eval(request.data.decode('utf8'))
    answer_num = req_dict['answer_num']
    user = req_dict['user']
    project = req_dict['project']
    res = qna.search_answer_by_answer_num(answer_num, user, project)
    
    return jsonify(results = res)

def search_multiple_answer(request):
    req_dict = eval(request.data.decode('utf8'))
    answer_num = req_dict['answer_num']
    user = req_dict['user']
    project = req_dict['project']
    res = db_multiple_answer.search_multiple_answer(answer_num, user, project)

    return jsonify(results = res)

def search_question(request):
    req_dict = eval(request.data.decode('utf8'))
    answer_num = req_dict['answer_num']
    user = req_dict['user']
    project = req_dict['project']
    res = qna.search_question(answer_num, user, project)
    buckets = db_training_config.get_bucket(user, project).split(",")
    for i in range(len(res)):
        question = res[i]['question']
        res[i]['bucket_id'] = bucket_util.get_bucket_id_by_sentence(buckets, question)
    
    return jsonify(results = res)

def search_compression_tag(request):
    req_dict = eval(request.data.decode('utf8'))
    subject = req_dict['subject']
    user = req_dict['user']
    project = req_dict['project']
    res = db_compression_tag.search_compression_tag(subject, user, project)
    
    return jsonify(results = res)

def search_tag(request):
    req_dict = eval(request.data.decode('utf8'))
    gubun = req_dict['gubun']
    res = db_tag.search_tag_by_gubun(gubun)
    
    return jsonify(results = res)

def search_synonym(request):
    req_dict = eval(request.data.decode('utf8'))
    synonym_nm = req_dict['synonym_nm']
    res = db_synonym.search_synonym_by_synonym_nm(synonym_nm)
    
    return jsonify(results = res)

def search_synonym_by_synonym_tag(request):
    req_dict = eval(request.data.decode('utf8'))
    synonym_tag = req_dict['synonym_tag']
    res = db_synonym.search_synonym_by_synonym_tag(synonym_tag)
    
    return jsonify(results = res)

def search_voca(request):
    req_dict = eval(request.data.decode('utf8'))
    voca_nm = req_dict['voca_nm']
    res = db_voca.search_voca_by_voca_nm(voca_nm)
    
    return jsonify(results = res)

def search_voca_and_appearance(request):
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    gubun = req_dict['gubun']
    subject = req_dict['subject']
    weight_parameter = req_dict['weight_parameter']
    res = search_voca_and_appearance_by_gubun(user, project, gubun, subject, weight_parameter)
    
    return jsonify(results = res)

def search_voca_and_appearance_by_gubun(user, project, gubun, subject, weight_parameter):
    result = qna.search_question('', user, project)
    if gubun == '1':
        res = voca_util.get_voca_and_appearance_from_question_list_by_answer_num(result, subject, weight_parameter)
    elif gubun == '2':
        res = voca_util.get_voca_and_appearance_from_question_list_by_question_srno(result, subject, weight_parameter)
    
    return res

def search_answer_num_and_question_voca(request):
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    gubun = req_dict['gubun']
    subject = req_dict['subject']
    result = qna.search_answer_num_and_question_voca_from_question_list_by_question_voca(user, project, subject)
    res = []
    if gubun == '1':
        res = voca_util.get_question_voca_group_by_answer_num(result)
    elif gubun == '2':
        res = voca_util.get_question_voca_group_by_question_srno(result)
    
    return jsonify(results = res)

def search_category(request):
    res = db_category.search_category()
    
    return jsonify(results = res)

def search_new_request(request):
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    subject = req_dict['subject']
    pc_status = req_dict['pc_status']
    res = db_new_request.search_new_request(user, project, subject, pc_status)
    
    return jsonify(results = res)

def search_new_request_by_rq_num(request):
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    rq_num = req_dict['rq_num']
    res = db_new_request.search_new_request_by_rq_num(user, project, rq_num)
    
    return jsonify(results = res)

def search_training_config(request):
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    res = db_training_config.search_training_config(user, project)
    
    return jsonify(results = res)

def search_chatbot_config(request):
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    res = db_chatbot_config.search_chatbot_config(user, project)
    
    return jsonify(results = res)

def search_notice(request):
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    complete_yn = req_dict['complete_yn']
    subject = req_dict['subject']
    res = db_notice.search_notice_list(user, project, subject, complete_yn)
    
    return jsonify(results = res)

def search_wrong_answer(request):
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    subject = req_dict['subject']
    res = db_statistics.search_wrong_answer(user, project, subject)
    
    return jsonify(results = res)

def search_bucket_id_by_sentence(request):
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    question = req_dict['question']
    buckets = db_training_config.get_bucket(user, project).split(",")
    res = bucket_util.get_bucket_id_by_sentence(buckets, question)
    
    return jsonify(res)
