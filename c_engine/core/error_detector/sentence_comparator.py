from a_builder.util import error_detecting_util
from e_database import chat
from a_builder.util import voca_util
from e_database import chatbot_config
from e_database import question_and_answer as db_qna

result = None
voca_and_appearance = None
def compare_by_formula(user, project, question, answer_num):
    config = chatbot_config.search_chatbot_config(user, project)
    threshold = 0
    weight = '1.1'
    for c in config:
        if c['config_name'] == 'USE_ERROR_DETECTION':
            if c['config_value'] == 'N':
                return True
        elif c['config_name'] == 'ERROR_DETECTION_THRESHOLD':
            threshold = int(c['config_value'])
        elif c['config_name'] == 'ERROR_DETECTION_WEIGHT':
            weight = c['config_value']

    global result, voca_and_appearance
    if result == None:
        result = db_qna.search_question('', user, project)
        voca_and_appearance = voca_util.get_voca_and_appearance_from_question_list_by_answer_num(result, '', weight)
    
    res = db_qna.search_question_voca_by_answer_num(user, project, answer_num)
    right_question_voca_arr = []
    for r in res:
        for arr in r['question_voca'].split(";"):
            if arr not in right_question_voca_arr:
                right_question_voca_arr.append(arr)
    res, point = error_detecting_util.compare_my_question_and_right_question(voca_and_appearance, weight, question, ";".join(right_question_voca_arr))
    print("point:" + str(point), "threshold:" + str(threshold), "weight:" + str(weight))
    if point < threshold:
        return False, point

    return True, point

def compare_two(input_1, input_2, p_threshold):
    if p_threshold == 0.0:
        return True
    a = chat.get_voca_by_voca_nm_list(chat.word_tokenizer(input_1))
    b = {}
    c = []
    minimum_appear_cnt = 2
    for ele in input_2:
        e = chat.get_voca_by_voca_nm_list(chat.word_tokenizer(ele))
        for ee in e:
            if b.get(ee) == None:
                b[ee] = 1
            else:
                b[ee] += 1
            if b[ee] >= minimum_appear_cnt and ee not in c:
                c.append(ee)
    cnt = get_sync_count(a, c)
    if len(c) == 0:
        c = 'x'
    if cnt / len(c) >= p_threshold:
        return True
    else:
        return False

def get_sync_count(a, b):
    cnt = 0
    for aa in a:
        if aa in b:
            cnt += 1
    return cnt
    
def is_almost_same(a, b):
    if a == b:
        return True
    return False
