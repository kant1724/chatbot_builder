from e_database.sql_processor import select 
from e_database.sql_processor import update

def get_answer_and_answer_num():
    sql = "SELECT ANSWER_NUM, ANSWER FROM ANSWER_LIST_GAD"
    result = select.fetch(sql)
    answer_dict = {}
    for r in result:
        answer_dict[r[0]] = r[1]

    return answer_dict

def get_training_question_list(user, project, answer_num):
    sql = "SELECT QUESTION FROM QUESTION_BUILDER_" + user + "_" + project + " WHERE ANSWER_NUM = '" + answer_num + "'"
    result = select.fetch(sql)
    question_list = []
    for r in result:
        question_list.append(r[0])

    return question_list

def get_all_answer_num_and_rpsn_question(user, project):
    sql = "SELECT ANSWER_NUM, RPSN_QUESTION FROM ANSWER_BUILDER_" + user + "_" + project
    result = select.fetch(sql)
    res = {}
    for r in result:
        res[r[0]] = r[1]

    return res

def get_same_category_question_list(user, project, answer_num):
    table_name = "ANSWER_BUILDER_" + user + "_" + project
    sql = "SELECT RPSN_QUESTION FROM " + table_name + " WHERE CATEGORY_NUM != '' AND CATEGORY_NUM IN (SELECT CATEGORY_NUM FROM " + table_name + " WHERE ANSWER_NUM = '" + answer_num + "')"
    result = select.fetch(sql)
    question_list = []
    for r in result:
        question_list.append(r[0])

    return question_list

def collect_right_answer(question, answer_num):
    sql = "INSERT INTO RIGHT_ANSWER VALUES ('" + question + "', '" + answer_num + "', CAST(DATE_FORMAT(NOW(), '%Y%m%d') AS CHAR), CAST(DATE_FORMAT(NOW(), '%H%i%s') AS CHAR))"
    update.commit(sql)

def collect_wrong_answer(question, answer_num):
    sql = "INSERT INTO WRONG_ANSWER VALUES ('" + question + "', '" + answer_num + "', CAST(DATE_FORMAT(NOW(), '%Y%m%d') AS CHAR), CAST(DATE_FORMAT(NOW(), '%H%i%s') AS CHAR))"
    update.commit(sql)
    
def get_voca_by_voca_nm_list(a):
    res = []
    for aa in a:
        sql = "SELECT VOCA_NM FROM VOCA WHERE VOCA_NM ='" + aa + "'"
        result = select.fetch(sql)
        if len(result) > 0:
            res.append(result[0][0])

    return res;

def get_most_frequent_list(answer_num, rank):
    sql = "SELECT ROWNUM, ANSWER_NUM, COUNT FROM (SELECT ROWNUM, ANSWER_NUM, COUNT FROM (SELECT @ROWNUM := @ROWNUM + 1 AS ROWNUM, ANSWER_NUM, COUNT(QUESTION) COUNT FROM QUESTION_LIST WHERE ANSWER_NUM != '" + answer_num + "' GROUP BY ANSWER_NUM) A ORDER BY COUNT DESC, ANSWER_NUM ASC) B"
    result = select.fetch(sql)
    answer_num_list = []
    count = []
    for r in result:
        answer_num_list.append(r[1])
        count.append(r[2])

    return answer_num_list, count
    
def collect_question(user_ip, question, answer_num):
    sql = "INSERT INTO QUESTION_LIST VALUES ('" + question + "', '" + answer_num + "', CAST(DATE_FORMAT(NOW(), '%Y%m%d') AS CHAR), CAST(DATE_FORMAT(NOW(), '%H%i%s') AS CHAR), '" + user_ip + "')"
    update.commit(sql)

def insert_schedule(user_ip, msg, time):
    sql = "INSERT INTO SCHEDULE VALUES ('" + user_ip + "', '" + msg + "', CAST(DATE_FORMAT(NOW(), '%Y%m%d') AS CHAR), '" + time + "')"
    update.commit(sql)
    
def select_schedule(user_ip, time):
    sql = ''
    if time != '':
        sql = "SELECT MESSAGE FROM SCHEDULE WHERE USER_IP ='" + user_ip + "' AND RESV_DATE = CAST(DATE_FORMAT(NOW(), '%Y%m%d') AS CHAR) AND RESV_TIME = '" + time + "'"
    else:
        sql = "SELECT MESSAGE FROM SCHEDULE WHERE USER_IP ='" + user_ip + "' AND RESV_DATE = CAST(DATE_FORMAT(NOW(), '%Y%m%d') AS CHAR) AND RESV_TIME > CAST(DATE_FORMAT(NOW(), '%H%i') AS CHAR) ORDER BY RESV_TIME ASC"
    result = select.fetch(sql)
    msg = []
    if len(result) > 0:
        for r in result:
            d = {}
            d['message'] = r[0]
            msg.append(d)

    return msg

def insert_my_frequent_question(user_ip, question):
    sql = "INSERT INTO MY_QUESTION VALUES ('" + user_ip + "', '', '" + question + "', CAST(DATE_FORMAT(NOW(), '%Y%m%d') AS CHAR))"
    update.commit(sql)

def get_next_rq_num(user, project):
    sql = "SELECT MAX(RQ_NUM) + 1 FROM REQUEST_QUESTION_" + user + "_" + project
    result = select.fetch(sql)
    rq_num = 1
    for r in result:
        if r[0] == None:
            rq_num = 1
        else:
            rq_num = int(r[0])

    return str(rq_num)

def insert_request_question(user, project, user_ip, question):
    rq_num = get_next_rq_num(user, project)
    sql = "INSERT INTO REQUEST_QUESTION_" + user + "_" + project + " VALUES ('" + rq_num + "', '" + user_ip + "', '" + question + "', CAST(DATE_FORMAT(NOW(), '%Y%m%d') AS CHAR), CAST(DATE_FORMAT(NOW(), '%H%i%s') AS CHAR), 0, '01')"
    update.commit(sql)
    
def get_request_question(user, project, user_ip):
    sql = '' 
    if user_ip != '':
        sql = "SELECT RQ_NUM, QUESTION, RECOMMEND_CNT, PC_STATUS FROM REQUEST_QUESTION_" + user + "_" + project + " WHERE USER_IP = '" + user_ip + "' ORDER BY RECOMMEND_CNT DESC"
    else:
        sql = "SELECT RQ_NUM, QUESTION, RECOMMEND_CNT, PC_STATUS FROM REQUEST_QUESTION_" + user + "_" + project + " ORDER BY RECOMMEND_CNT DESC"
    result = select.fetch(sql)
    res = []
    for r in result:
        res.append({'rq_num' : r[0], 'question' : r[1], 'recommend_cnt' : r[2], 'pc_status' : r[3]})

    return res

def update_request_question_recommend_cnt(user, project, rq_num):
    sql = "UPDATE REQUEST_QUESTION_" + user + "_" + project + " SET RECOMMEND_CNT = RECOMMEND_CNT + 1 WHERE RQ_NUM = " + str(rq_num)
    update.commit(sql)

def get_my_question(user_ip):
    sql = "SELECT QUESTION FROM MY_QUESTION WHERE USER_IP = '" + user_ip + "'"
    result = select.fetch(sql)
    msg = []
    for i in range(len(result)):
        msg.append(result[i][0])

    return msg

def get_latest_question(user_ip):
    sql = "SELECT QUESTION FROM QUESTION_LIST WHERE USER_IP = '" + user_ip + "' AND RGSN_DATE = CAST(DATE_FORMAT(NOW(), '%Y%m%d') AS CHAR) ORDER BY RGSN_DATE DESC, RGSN_TIME DESC"
    result = select.fetch(sql)
    msg = []
    for i in range(len(result)):
        msg.append(result[i][0])

    return msg

def word_tokenizer(sentence):
    token_arr = sentence.split(" ")
    new_words = []
    tokenized_arr = []
    while len(token_arr) > 0:
        cur_token = token_arr[0]
        remain_token = ""
        find = False;
        while cur_token != "":
            sql = "SELECT VOCA_NM FROM VOCA WHERE VOCA_NM ='" + cur_token + "'"
            result = select.fetch(sql)
            if len(result) == 0:
                word = ""
            else:
                word = result[0][0]
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
            new_words.append(remain_token)
            tokenized_arr.append(remain_token)
        else:
            tokenized_arr.append(cur_token)

    return tokenized_arr

def get_all_brnc_nm_list():
    sql = "SELECT BRNC_NM FROM BRNC_LIST"
    result = select.fetch(sql)
    brnc_nm_list = []
    for i in range(len(result)):
        brnc_nm_list.append(result[i][0])

    return brnc_nm_list

def get_kor_nm_by_tag_nm(tag_nm):
    sql = "SELECT KOR_NM FROM TAG_LIST WHERE TAG_NM = '" + tag_nm + "'"
    result = select.fetch(sql)
    tag_nm = ''
    if len(result) > 0:
        tag_nm = result[0][0]

    return tag_nm

def get_dialogue_list_by_function_nm_and_argument_nm(function_nm, argument_nm):
    sql = "SELECT MAX(DIALOGUE_TEXT) FROM DIALOGUE_LIST WHERE FUNCTION_NM = '" + function_nm + "' AND ARGUMENT_NM = '" + argument_nm + "'"
    result = select.fetch(sql)
    dialogue_text = ''
    if len(result) > 0:
        dialogue_text = result[0][0]

    return dialogue_text

def get_next_chat_room_no():
    sql = "SELECT MAX(ROOM_NO) + 1 FROM CHAT_ROOM_LIST"
    result = select.fetch(sql)
    room_no = 1
    for r in result:
        if r[0] == None:
            room_no = 1
        else:
            room_no = int(r[0])

    return str(room_no)

def insert_new_chat_room(room_name, password):
    room_no = get_next_chat_room_no()
    sql = "INSERT INTO CHAT_ROOM_LIST VALUES (" + room_no + ", '" + room_name + "', '" + password + "', 0)"
    update.commit(sql)
    
    return room_no
    
def insert_new_chat_member(room_no, user_ip, user_name):
    sql = "INSERT INTO CHAT_MEMBER_LIST VALUES (" + room_no + ", '" + user_ip + "', '" + user_name + "')"
    update.commit(sql)

def get_chat_room(room_name):
    if room_name != '':
        sql = "SELECT ROOM_NO, ROOM_NAME, PASSWORD FROM CHAT_ROOM_LIST WHERE ROOM_NAME = '" + room_name + "'"
    else:
        sql = "SELECT ROOM_NO, ROOM_NAME, PASSWORD FROM CHAT_ROOM_LIST"
    result = select.fetch(sql)
    room_no = None
    room_name = ''
    password = ''
    if len(result) > 0:
        room_no = str(result[0][0])
        room_name = result[0][1]
        password = result[0][2]
        
    return room_no, room_name, password

def get_answer_by_answer_num(user, project, answer_num):
    sql = "SELECT ANSWER, MDFC_RGSN_DATE FROM ANSWER_BUILDER_" + user + "_" + project + " WHERE ANSWER_NUM = '" + answer_num + "'"
    result = select.fetch(sql)
    answer = ''
    mdfc_rgsn_date = ''
    if len(result) > 0:
        answer = str(result[0][0])
        mdfc_rgsn_date = str(result[0][1])
        
    return answer, mdfc_rgsn_date
