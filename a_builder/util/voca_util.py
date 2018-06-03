import operator
from e_database import voca as db_voca
from a_builder.util import synonym_util

def get_voca_from_question(question, all_voca):
    question_voca = []
    qs_arr = question.split(" ")
    for qs in qs_arr:
        for voca in all_voca:
            voca_synonym_str = voca['voca_synonym']
            voca_synonym_arr = voca_synonym_str.split("^")
            keyword_yn = voca['keyword_yn']
            if keyword_yn == 'Y':
                for voca_synonym in voca_synonym_arr:
                    if voca_synonym in qs and voca_synonym_str not in question_voca:
                        question_voca.append(voca_synonym_str)
    
    return question_voca

def get_question_voca(question):
    token_arr = question.split(" ")
    voca = []
    while len(token_arr) > 0:
        cur_token = token_arr[0]
        remain_token = ""
        find = False;
        while cur_token != "":
            result = db_voca.search_voca_by_equal_voca_nm(cur_token, 'Y')
            if len(result) == 0:
                word = ""
            else:
                word = result[0]["voca_synonym"]
                if word not in voca:
                    voca.append(word)
            if word != "":
                find = True
                if remain_token != "":
                    token_arr[0] = remain_token
                else:
                    token_arr.pop(0)
                break
            remain_token = cur_token[len(cur_token) - 1] + remain_token
            cur_token = cur_token[0 : -1]
        if find == False:
            token_arr.pop(0)
    res = ""
    for i in range(len(voca)):
        if i < len(voca) - 1:
            res += voca[i] + ";"
        else:
            res += voca[i]
    
    return res

def get_voca_and_appearance_from_question_list_by_answer_num(question_dict, subject, weight_parameter):
    answer_num_and_voca = {}
    for q in question_dict:
        answer_num = q['answer_num']
        if q['question_voca'] == '':
            continue
        arr = q['question_voca'].split(';')
        if answer_num_and_voca.get(answer_num) == None:
            answer_num_and_voca[answer_num] = arr
        else:
            already = answer_num_and_voca[answer_num]
            for ar in arr:
                if ar not in already:
                    already.append(ar)
    key_list = answer_num_and_voca.keys()
    voca_dict = {}
    for key in key_list:
        voca_arr = answer_num_and_voca[key]
        for voca in voca_arr:
            if voca_dict.get(voca) == None:
                voca_dict[voca] = 1
            else:
                voca_dict[voca] += 1
    voca_dict = sorted(voca_dict.items(), key = operator.itemgetter(1), reverse=True)
    res = []
    for i in range(len(voca_dict)):
        if subject != None and subject != '':
            if subject not in voca_dict[i][0]:
                continue
        d = {}
        d["voca_nm"] = voca_dict[i][0]
        d["appearance_count"] = voca_dict[i][1]
        d["voca_weight"] = round(1 / pow(float(weight_parameter), voca_dict[i][1] - 1), 3)
        
        res.append(d)
    
    return res

def get_voca_and_appearance_from_question_list_by_question_srno(question_dict, subject, weight_parameter):
    voca_dict = {}
    for q in question_dict:
        if q['question_voca'] == '':
            continue
        arr = q['question_voca'].split(';')
        for ar in arr:
            if voca_dict.get(ar) == None:
                voca_dict[ar] = 1
            else:
                voca_dict[ar] += 1
    voca_dict = sorted(voca_dict.items(), key = operator.itemgetter(1), reverse=True)
    res = []
    for i in range(len(voca_dict)):
        if subject != None and subject != '':
            if subject not in voca_dict[i][0]:
                continue
        d = {}
        d["voca_nm"] = voca_dict[i][0]
        d["appearance_count"] = voca_dict[i][1]
        d["voca_weight"] = round(1 / pow(float(weight_parameter), voca_dict[i][1] - 1), 3)
        res.append(d)
    
    return res

def get_question_voca_group_by_answer_num(result):
    answer_dict = {}
    res = []
    for r in result:
        if r['question_voca'] == '':
            continue
        voca_arr = r['question_voca'].split(';')
        answer_num = r['answer_num']
        answer_voca_arr = answer_dict.get(answer_num)
        if answer_voca_arr == None:
            answer_dict[answer_num] = voca_arr
        else:
            for voca in voca_arr:
                if voca not in answer_voca_arr:
                    answer_voca_arr.append(voca)
            
    for key in answer_dict.keys():
        res_dict = {}
        res_dict['answer_num'] = key
        res_dict['question_voca'] = ";".join(answer_dict[key])
        res.append(res_dict)
        
    return res

def get_question_voca_group_by_question_srno(result):
    res = []
    for r in result:
        if r['question_voca'] == '':
            continue
        res.append(r)
        
    return res
    
def update_voca_synonym():
    all_voca = db_voca.search_voca_by_voca_nm('')
    for voca in all_voca:
        voca_nm = voca['voca_nm']
        voca_synonym = synonym_util.get_synonym_nm_list_by_voca_nm(voca_nm)
        db_voca.update_voca_synonym(voca_synonym, voca_nm)
    