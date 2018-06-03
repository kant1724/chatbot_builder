from e_database import question_and_answer as qna
from e_database import compression_tag as db_compression_tag
from e_database import voca as db_voca
from e_database import synonym as db_synonym
from e_database import category as db_category
from e_database import notice as db_notice
from flask import jsonify

def delete_answer(request):
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    answer_num = req_dict['answer_num']
    qna.delete_answer(answer_num, user, project)
    
    return jsonify('')

def delete_question(request):
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    answer_num = req_dict['answer_num']
    question_srno = req_dict['question_srno']
    qna.delete_question(answer_num, question_srno, user, project)
    
    return jsonify('')

def delete_compression_tag(request):
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    compression_num = req_dict['compression_num']
    db_compression_tag.delete_compression_tag(user, project, compression_num)
    
    return jsonify('')

def delete_synonym_master(request):
    req_dict = eval(request.data.decode('utf8'))
    synonym_tag = req_dict['synonym_tag']
    db_synonym.delete_synonym_by_synonym_tag(synonym_tag)
    
    return jsonify('')

def delete_synonym_detail(request):
    req_dict = eval(request.data.decode('utf8'))
    synonym_num = req_dict['synonym_num']
    db_synonym.delete_synonym_by_synonym_num(synonym_num)
    
    return jsonify('')

def delete_voca(request):
    req_dict = eval(request.data.decode('utf8'))
    voca_nm = req_dict['voca_nm']
    db_voca.delete_voca_by_voca_nm(voca_nm)
    
    return jsonify('')

def delete_category(request):
    req_dict = eval(request.data.decode('utf8'))
    category_num = req_dict['category_num']
    db_category.delete_category_by_category_num(category_num)
    
    return jsonify('')

def delete_notice(request):
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    notice_num = req_dict['notice_num']
    db_notice.delete_notice(user, project, notice_num)
    
    return jsonify('')

