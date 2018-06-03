from e_database.sql_processor import select 
from e_database.sql_processor import update

def search_answer(gubun, subject, user, project):
    sql = ''
    category_select = "(SELECT CONCAT(BIG_CATEGORY,' > ',MIDDLE_CATEGORY,' > ',SMALL_CATEGORY_LV1,' > ',SMALL_CATEGORY_LV2,' > ',SMALL_CATEGORY_LV3) FROM CATEGORY_LIST WHERE CATEGORY_NUM = X.CATEGORY_NUM) AS CATEGORY_NM"
    if subject != '':
        if gubun == '1':
            sql = "SELECT X.RPSN_QUESTION, X.ANSWER_NUM, X.ANSWER, X.CATEGORY_NUM, " + category_select + ", X.IMAGE_CNT, X.RGSN_USER_IP FROM ANSWER_BUILDER_" + user + "_" + project + " X WHERE X.ANSWER_NUM IN (SELECT ANSWER_NUM FROM QUESTION_BUILDER_" + user + "_" + project + " WHERE QUESTION LIKE '%" + subject + "%') ORDER BY X.ANSWER_NUM DESC"
        elif gubun == '2':
            sql = "SELECT X.RPSN_QUESTION, X.ANSWER_NUM, X.ANSWER, X.CATEGORY_NUM, " + category_select + ", X.IMAGE_CNT, X.RGSN_USER_IP FROM ANSWER_BUILDER_" + user + "_" + project + " X WHERE X.ANSWER LIKE '%" + subject + "%' ORDER BY X.ANSWER_NUM DESC"
        elif gubun == '3':
            sql = "SELECT X.RPSN_QUESTION, X.ANSWER_NUM, X.ANSWER, X.CATEGORY_NUM, " + category_select + ", X.IMAGE_CNT, X.RGSN_USER_IP FROM ANSWER_BUILDER_" + user + "_" + project + " X WHERE X.RGSN_USER_IP = '" + subject + "' ORDER BY X.ANSWER_NUM DESC"
    else:
        sql = "SELECT X.RPSN_QUESTION, X.ANSWER_NUM, X.ANSWER, X.CATEGORY_NUM, " + category_select + ", X.IMAGE_CNT, X.RGSN_USER_IP FROM ANSWER_BUILDER_" + user + "_" + project + " X ORDER BY X.ANSWER_NUM DESC"
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['rpsn_question'] = r[0]
        res_dict['answer_num'] = r[1] 
        res_dict['answer'] = r[2]
        res_dict['category_num'] = r[3]
        res_dict['category_nm'] = ''
        if r[4] != None:
            arr = r[4].split(" > ")
            new_arr = []
            for i in range(len(arr)):
                if arr[i] != '':
                    new_arr.append(arr[i])
            res_dict['category_nm'] = " > ".join(new_arr)
        res.append(res_dict)
        res_dict['image_cnt'] = r[5]
        res_dict['rgsn_user'] = r[6]
    return res

def search_answer_by_answer_num(answer_num, user, project):
    category_select = "(SELECT CONCAT(BIG_CATEGORY,' > ',MIDDLE_CATEGORY,' > ',SMALL_CATEGORY_LV1,' > ',SMALL_CATEGORY_LV2,' > ',SMALL_CATEGORY_LV3) FROM CATEGORY_LIST WHERE CATEGORY_NUM = X.CATEGORY_NUM) AS CATEGORY_NM"
    sql = "SELECT X.RPSN_QUESTION, X.ANSWER_NUM, X.ANSWER, X.CATEGORY_NUM, " + category_select + ", X.IMAGE_CNT, X.RGSN_USER_IP FROM ANSWER_BUILDER_" + user + "_" + project + " X WHERE X.ANSWER_NUM = '" + answer_num + "'"
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['rpsn_question'] = r[0]
        res_dict['answer_num'] = r[1] 
        res_dict['answer'] = r[2]
        res_dict['category_num'] = r[3]
        res_dict['category_nm'] = ''
        if r[4] != None:
            arr = r[4].split(" > ")
            new_arr = []
            for i in range(len(arr)):
                if arr[i] != '':
                    new_arr.append(arr[i])
            res_dict['category_nm'] = " > ".join(new_arr)
        res.append(res_dict)
        res_dict['image_cnt'] = r[5]
        res_dict['rgsn_user'] = r[6]
        
    return res

def search_image_cnt_in_answer(user, project, answer_num):
    sql = "SELECT IMAGE_CNT FROM ANSWER_BUILDER_" + user + "_" + project + " WHERE ANSWER_NUM = '" + answer_num + "'"
    result = select.fetch(sql)
    
    return result[0][0]

def search_max_answer_num(user, project):
    sql = "SELECT MAX(ANSWER_NUM) FROM ANSWER_BUILDER_" + user + "_" + project
    result = select.fetch(sql)
    max_answer_num = ''
    for r in result:
        max_answer_num = r[0]

    return max_answer_num

def insert_answer(answer_num, answer, question, category_num, user_ip, rq_num, user, project):
    sql = "INSERT INTO ANSWER_BUILDER_" + user + "_" + project + " VALUES ('" + answer_num + "', '" + answer + "', '" + category_num + "', '" + question + "', 0, '" + user_ip + "', " + rq_num + ", CAST(DATE_FORMAT(NOW(), '%Y%m%d') AS CHAR), CAST(DATE_FORMAT(NOW(), '%Y%m%d') AS CHAR))"
    update.commit(sql)

def update_answer(answer_num, rpsn_question, answer, category_num, user, project):
    sql = "UPDATE ANSWER_BUILDER_" + user + "_" + project + " SET RPSN_QUESTION = '" + rpsn_question + "', ANSWER = '" + answer + "', CATEGORY_NUM = '" + str(category_num) + "', MDFC_RGSN_DATE = CAST(DATE_FORMAT(NOW(), '%Y%m%d') AS CHAR) WHERE ANSWER_NUM = '" + str(answer_num) + "'" 
    update.commit(sql)

def update_image_cnt(user, project, answer_num, image_cnt):
    sql = "UPDATE ANSWER_BUILDER_" + user + "_" + project + " SET IMAGE_CNT = " + image_cnt + " WHERE ANSWER_NUM = '" + str(answer_num) + "'"
    update.commit(sql)

def delete_answer(answer_num, user, project):
    sql = "DELETE FROM ANSWER_BUILDER_" + user + "_" + project + " WHERE ANSWER_NUM = '" + answer_num + "'"
    update.commit(sql)
    sql = "DELETE FROM QUESTION_BUILDER_" + user + "_" + project + " WHERE ANSWER_NUM = '" + answer_num + "'"
    update.commit(sql)

def delete_all_answer(user, project):
    sql = "DELETE FROM ANSWER_BUILDER_" + user + "_" + project
    update.commit(sql)

def search_question(answer_num, user, project):
    sql = ''
    if answer_num != None and answer_num != '':
        sql = "SELECT ANSWER_NUM, QUESTION_SRNO, QUESTION, QUESTION_TAG, QUESTION_VOCA FROM QUESTION_BUILDER_" + user + "_" + project + " WHERE ANSWER_NUM = '" + answer_num + "'"
    else:
        sql = "SELECT ANSWER_NUM, QUESTION_SRNO, QUESTION, QUESTION_TAG, QUESTION_VOCA FROM QUESTION_BUILDER_" + user + "_" + project
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['answer_num'] = r[0]
        res_dict['question_srno'] = r[1]
        res_dict['question'] = r[2]
        res_dict['question_tag'] = r[3]
        res_dict['question_voca'] = r[4]
        res_dict['fragment_yn'] = 'N'
        res.append(res_dict)
            
    return res

def search_question_fragment(answer_num, user, project):
    sql = ''
    if answer_num != None and answer_num != '':
        sql = "SELECT ANSWER_NUM, QUESTION_SRNO, QUESTION FROM QUESTION_FRAGMENT_BUILDER_" + user + "_" + project + " WHERE ANSWER_NUM = '" + answer_num + "'"
    else:
        sql = "SELECT ANSWER_NUM, QUESTION_SRNO, QUESTION FROM QUESTION_FRAGMENT_BUILDER_" + user + "_" + project
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['answer_num'] = r[0]
        res_dict['question_srno'] = r[1]
        res_dict['question'] = r[2]
        res_dict['question_tag'] = ''
        res_dict['question_voca'] = ''
        res_dict['fragment_yn'] = 'Y'
        res.append(res_dict)
            
    return res

def search_question_by_question_nm_and_answer_num(question_nm, answer_num, user, project):
    where_question_nm = ''
    where_answer_num = ''
    if question_nm != None and question_nm != '':
        where_question_nm = " AND QUESTION LIKE '%" + question_nm + "%'"
    if answer_num != None and answer_num != '':
        where_answer_num = " AND ANSWER_NUM = '" + answer_num + "'"
    sql = "SELECT ANSWER_NUM, QUESTION_SRNO, QUESTION, QUESTION_TAG, QUESTION_VOCA FROM QUESTION_BUILDER_" + user + "_" + project + " WHERE 1=1" + where_question_nm + where_answer_num
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['answer_num'] = r[0]
        res_dict['question_srno'] = r[1]
        res_dict['question'] = r[2]
        res_dict['question_tag'] = r[3]
        res_dict['question_voca'] = r[4]
        res_dict['fragment_yn'] = 'N'
        res.append(res_dict)
            
    return res

def search_question_fragment_by_question_nm_and_answer_num(question_nm, answer_num, user, project):
    where_question_nm = ''
    where_answer_num = ''
    if question_nm != None and question_nm != '':
        where_question_nm = " AND QUESTION LIKE '%" + question_nm + "%'"
    if answer_num != None and answer_num != '':
        where_answer_num = " AND ANSWER_NUM LIKE '%" + answer_num + "%'"
    sql = "SELECT ANSWER_NUM, QUESTION_SRNO, QUESTION, QUESTION_VOCA FROM QUESTION_FRAGMENT_BUILDER_" + user + "_" + project + " WHERE 1=1" + where_question_nm + where_answer_num 
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['answer_num'] = r[0]
        res_dict['question_srno'] = r[1]
        res_dict['question'] = r[2]
        res_dict['question_tag'] = ''
        res_dict['question_voca'] = r[3]
        res_dict['fragment_yn'] = 'Y'
        res.append(res_dict)
            
    return res

def search_next_question_srno(user, project):
    sql = "SELECT MAX(QUESTION_SRNO) + 1 FROM QUESTION_BUILDER_" + user + "_" + project
    result = select.fetch(sql)
    next_question_srno = 1
    for r in result:
        if r[0] == None:
            next_question_srno = 1
        else:
            next_question_srno = int(r[0])

    return str(next_question_srno)

def insert_question(answer_num, question, question_tag, user, project):
    question_srno = search_next_question_srno(user, project)
    sql = "INSERT INTO QUESTION_BUILDER_" + user + "_" + project + " VALUES ('" + answer_num + "', '" + question_srno + "', '" + question + "', '" + question_tag + "', '')"
    update.commit(sql)
    
    return question_srno
    
def delete_question(answer_num, question_srno, user, project):
    sql = "DELETE FROM QUESTION_BUILDER_" + user + "_" + project + " WHERE ANSWER_NUM = '" + answer_num + "' AND QUESTION_SRNO = " + question_srno
    update.commit(sql)

def delete_all_question(user, project):
    sql = "DELETE FROM QUESTION_BUILDER_" + user + "_" + project
    update.commit(sql)
    
def update_all_question_voca(conn, user, project, question_voca, answer_num, question_srno):
    sql = "UPDATE QUESTION_BUILDER_" + user + "_" + project + " SET QUESTION_VOCA = '" + question_voca + "' WHERE ANSWER_NUM = '" + answer_num + "' AND QUESTION_SRNO = " + str(question_srno)
    update.execute(conn, sql)

def update_all_question_voca_in_fragment(conn, user, project, question_voca, answer_num, question_srno):
    sql = "UPDATE QUESTION_FRAGMENT_BUILDER_" + user + "_" + project + " SET QUESTION_VOCA = '" + question_voca + "' WHERE ANSWER_NUM = '" + answer_num + "' AND QUESTION_SRNO = " + str(question_srno)
    update.execute(conn, sql)
    
def search_answer_num_and_question_voca_from_question_list_by_question_voca(user, project, subject):
    sql = "SELECT ANSWER_NUM, QUESTION_VOCA FROM QUESTION_BUILDER_" + user + "_" + project + " WHERE ANSWER_NUM IN (SELECT ANSWER_NUM FROM QUESTION_BUILDER_" + user + "_" + project + " WHERE QUESTION_VOCA LIKE '%" + subject + "%')"
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['answer_num'] = r[0]
        res_dict['question_voca'] = r[1] 
        res.append(res_dict)

    return res

def search_question_voca_by_answer_num(user, project, answer_num):
    sql = "SELECT QUESTION_VOCA FROM QUESTION_BUILDER_" + user + "_" + project + " WHERE ANSWER_NUM = '" + answer_num + "'"
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['question_voca'] = r[0] 
        res.append(res_dict)

    return res

def get_latest_new_question(user, project, frst_rgsn_date):
    sql = "SELECT RPSN_QUESTION, FRST_RGSN_DATE, ANSWER_NUM FROM ANSWER_BUILDER_" + user + "_" + project + " WHERE FRST_RGSN_DATE >= '" + frst_rgsn_date + "' ORDER BY FRST_RGSN_DATE DESC, ANSWER_NUM DESC"
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['rpsn_question'] = r[0]
        res_dict['frst_rgsn_date'] = r[1]
        res_dict['answer_num'] = r[2]    
        res.append(res_dict)

    return res
    