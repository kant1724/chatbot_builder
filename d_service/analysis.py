from d_service import search
from a_builder.util import error_detecting_util
from flask import jsonify
from a_builder.util import voca_util

def compare_my_question_and_right_question(request):
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    gubun = req_dict['gubun']
    base = req_dict['base']
    subject = req_dict['subject']
    my_question = req_dict['my_question']
    right_question_voca = req_dict['right_question_voca']
    result = search.search_voca_and_appearance_by_gubun(user, project, gubun, subject, base)
    res, point = error_detecting_util.compare_my_question_and_right_question(result, base, my_question, right_question_voca)
    
    return jsonify(results = res)
