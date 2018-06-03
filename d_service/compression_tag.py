from flask import jsonify
from b_trainer.worker import compression_tag
from e_database import compression_tag as db_compression_tag
from e_database import training_config as db_training_config

all_tag_name_and_all_expression = {}
enc_vocab = None
rev_dec_vocab = None
language = ''

def init_compression_tag(user, project):
    global all_tag_name_and_all_expression, enc_vocab, rev_dec_vocab, language
    enc_vocab, rev_dec_vocab = compression_tag.init_compression_tag(user, project)
    all_question = db_compression_tag.search_compression_tag('', user, project)
    language = db_training_config.get_project_language(user, project)
    for question in all_question:
        if all_tag_name_and_all_expression.get(question['tag_name']) == None:
            all_tag_name_and_all_expression[question['tag_name']] = [question['expression']]
        else:
            all_tag_name_and_all_expression[question['tag_name']].append(question['expression'])

def get_compression_tag(request): 
    req_dict = eval(request.data.decode('utf8'))
    user = req_dict['user']
    project = req_dict['project']
    expression = req_dict['expression']
    global enc_vocab, rev_dec_vocab
    is_running = compression_tag.is_running(user, project)
    if is_running == 'N' or enc_vocab == None or rev_dec_vocab == None: 
        init_compression_tag(user, project)
    tag_name = compression_tag.run_compression_tag(enc_vocab, rev_dec_vocab, expression, '', language)
    q_list = all_tag_name_and_all_expression[tag_name]
    num = len(q_list)
    res = {'num' : str(num)}
    for i in range(num):
        res['text' + str(i + 1)] = q_list[i]
    
    return jsonify(res)
