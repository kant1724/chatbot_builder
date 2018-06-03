from e_database import question_and_answer as qna
from e_database import compression_tag as db_compression_tag
from e_database import multiple_answer as db_multiple_answer
from e_database import tag as db_tag
from e_database import voca as db_voca
from e_database import synonym as db_synonym
from e_database import category as db_category
from e_database import new_request as db_new_request
from e_database import notice as db_notice
from a_builder.util import util as builder_util
from flask import jsonify
from a_builder.util import voca_util
from c_engine.core.error_detector import sentence_comparator as sc
from e_database.sql_processor import update

def submit_answer(request):
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    answer = req_dict['answer']
    question = req_dict['question']
    question_tag = req_dict['question_tag']
    category_num = req_dict['category_num']
    rq_num = req_dict['rq_num']
    if rq_num == None or rq_num == '':
        rq_num = 'null'
    user_ip = request.remote_addr
    max_answer_num = qna.search_max_answer_num(user, project)
    if max_answer_num == None:
        num = -1
    else:
        num = builder_util.alphabet_to_num(max_answer_num)
    answer_num = builder_util.num_to_alphabet(num + 1)
    qna.insert_answer(answer_num, answer, question, category_num, user_ip, rq_num, user, project)
    qna.insert_question(answer_num, question, question_tag, user, project)
    
    return jsonify('')

def submit_multiple_answer(request):
    req_dict = eval(request.data.decode('utf8'))    
    db_multiple_answer.delete_all_multiple_answer(req_dict[0]['answer_num'], req_dict[0]['user'], req_dict[0]['project'])
    for i in range(len(req_dict)):
        user = req_dict[i]['user']
        project = req_dict[i]['project']
        answer_num = req_dict[i]['answer_num']
        srno = i + 1
        question = req_dict[i]['question']
        answer = req_dict[i]['answer']
        if question != '' or answer != '':
            db_multiple_answer.insert_multiple_answer(answer_num, srno, question, answer, user, project)
    
    return jsonify('')

def submit_image(request):
    user = request.form['user']
    project = request.form['project']
    answer_num = request.form['answer_num']
    image_cnt = request.form['image_cnt']
    
    qna.update_image_cnt(user, project, answer_num, image_cnt)
    
    return jsonify('')
    
def submit_question(request):
    req_dict = eval(request.data.decode('utf8'))
    all_voca = db_voca.search_voca_by_voca_nm('')
    for i in range(len(req_dict)):
        user = req_dict[i]['user']
        project = req_dict[i]['project']
        answer_num = req_dict[i]['answer_num']
        question = req_dict[i]['question']
        question_tag = req_dict[i]['question_tag']
        question_srno = qna.insert_question(answer_num, question, question_tag, user, project)
        question_voca = voca_util.get_voca_from_question(question, all_voca)
        if len(question_voca) == 0:
            continue
        conn = update.get_connection()
        qna.update_all_question_voca(conn, user, project, ";".join(question_voca), answer_num, question_srno)
        update.end_connection(conn)
    
    return jsonify('')

def submit_compression_tag(request):
    req_dict = eval(request.data.decode('utf8'))
    for i in range(len(req_dict)):
        user = req_dict[i]['user']
        project = req_dict[i]['project']
        compression_num = req_dict[i]['compression_num']
        expression = req_dict[i]['expression']
        tag_name = req_dict[i]['tag_name']
        data_type = req_dict[i]['data_type']
        if data_type == "new":
            db_compression_tag.insert_compression_tag(user, project, expression, tag_name)
        elif data_type == "modified":
            db_compression_tag.update_compression_tag(user, project, compression_num, expression, tag_name)
    
    return jsonify('')

def submit_tag(request):
    req_dict = eval(request.data.decode('utf8'))
    tag_nm = req_dict['tag_nm']
    kor_nm = req_dict['kor_nm']
    gubun = req_dict['gubun']
    
    db_tag.insert_tag_list(tag_nm, kor_nm, gubun)
    
    return jsonify('')

def submit_synonym(request):
    req_dict = eval(request.data.decode('utf8'))
    for i in range(len(req_dict)):
        synonym_num = req_dict[i]['synonym_num']
        synonym_nm = req_dict[i]['synonym_nm']
        synonym_tag = req_dict[i]['synonym_tag']
        data_type = req_dict[i]['data_type']
        if data_type == "new":
            db_synonym.insert_synonym(synonym_nm, synonym_tag)
        elif data_type == "modified":
            db_synonym.update_synonym_by_synonym_num(synonym_num, synonym_nm)
    
    return jsonify('')

def submit_voca(request):
    req_dict = eval(request.data.decode('utf8'))
    voca_nm = req_dict['voca_nm']
    res = db_voca.search_voca_by_equal_voca_nm(voca_nm, '')
    if len(res) > 0:
        return jsonify('N')
    db_voca.insert_voca(voca_nm)
    sc.result = None
    
    return jsonify('Y')

def submit_voca_keyword(request):
    req_dict = eval(request.data.decode('utf8'))
    voca_nm = req_dict['voca_nm']
    db_voca.update_keyword_yn(voca_nm)
    
    return jsonify('')

def submit_category(request):
    req_dict = eval(request.data.decode('utf8'))
    for i in range(len(req_dict)):
        category_num = req_dict[i]['category_num']
        big_category = req_dict[i]['big_category']
        middle_category = req_dict[i]['middle_category']
        small_category_lv1 = req_dict[i]['small_category_lv1']
        small_category_lv2 = req_dict[i]['small_category_lv2']
        small_category_lv3 = req_dict[i]['small_category_lv3']
        data_type = req_dict[i]['data_type']
        if data_type == "new":
            db_category.insert_category(big_category, middle_category, small_category_lv1, small_category_lv2, small_category_lv3)
        elif data_type == "modified":
            db_category.update_category_by_category_num(category_num, big_category, middle_category, small_category_lv1, small_category_lv2, small_category_lv3)
    
    return jsonify('')

def submit_notice(request):
    req_dict = eval(request.data.decode('utf8'))    
    user = req_dict['user']
    project = req_dict['project']
    gubun = req_dict['gubun']
    notice_num = req_dict['notice_num']
    notice_subject = req_dict['notice_subject']
    notice_content = req_dict['notice_content']
    notice_start_date = req_dict['notice_start_date']
    notice_end_date = req_dict['notice_end_date']
    if gubun == 'modify':
        db_notice.update_notice(user, project, notice_num, notice_subject, notice_content, notice_start_date, notice_end_date)
    else:
        db_notice.insert_notice(user, project, notice_subject, notice_content, notice_start_date, notice_end_date)
    
    return jsonify('')

def submit_complete_request(request):
    req_dict = eval(request.data.decode('utf8'))    
    user = req_dict['user']
    project = req_dict['project']
    rq_num = req_dict['rq_num']
    db_new_request.update_complete_request(user, project, rq_num)
    
    return jsonify('')

def submit_notice_complete(request):
    req_dict = eval(request.data.decode('utf8'))    
    user = req_dict['user']
    project = req_dict['project']
    notice_num = req_dict['notice_num']
    db_notice.update_notice_complete(user, project, notice_num)
    
    return jsonify('')
