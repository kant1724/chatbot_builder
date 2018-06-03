from e_database import question_and_answer as qna
from e_database import notice as db_notice
from flask import jsonify

def modify_answer(request):
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    answer_num = req_dict['answer_num']
    rpsn_question = req_dict['rpsn_question']
    answer = req_dict['answer']
    category_num = req_dict['category_num']
    
    qna.update_answer(answer_num, rpsn_question, answer, category_num, user, project)
    
    return jsonify('')
