from b_trainer.file import training_file_creator as tfc
from e_database import question_and_answer as qna
from e_database import training_config as db_training_config
from flask import jsonify
from a_builder.util import bucket_util

def search_question_and_bucket_id(request):
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    question_nm = req_dict['question_nm']
    answer_num = req_dict['answer_num']
    bucket_id = req_dict['bucket_id']
    res = qna.search_question_by_question_nm_and_answer_num('', answer_num, user, project)
    fragment = qna.search_question_fragment_by_question_nm_and_answer_num(question_nm, answer_num, user, project)
    res = res + fragment
    buckets = db_training_config.get_bucket(user, project).split(",")
    filtered_answer_num_arr = []
    for i in range(len(res)):
        question = res[i]['question']
        if question_nm in question:
            filtered_answer_num_arr.append(res[i]['answer_num'])
        res[i]['bucket_id'] = bucket_util.get_bucket_id_by_sentence(buckets, question)
        
    new_res = []
    for i in range(len(res)):
        if res[i]['answer_num'] in filtered_answer_num_arr:
            new_res.append(res[i])
            
    res = sorted(new_res, key = lambda x : (x["bucket_id"], x["answer_num"]))
    
    if bucket_id != '':
        new_res = []
        for i in range(len(res)):
            if res[i]['bucket_id'] == bucket_id:
                new_res.append(res[i])
        return jsonify(results = new_res)
    
    return jsonify(results = res)

def search_bucket_id(request):
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    buckets = db_training_config.get_bucket(user, project)
    exception = str(tfc.exception)
    res = {'buckets' : buckets, 'exception' : exception}
    
    return jsonify(results = res)
