from a_builder.util import util
from e_database.sql_processor import select 
from e_database.sql_processor import update

def search_new_request(user, project, subject, pc_status):
    sql = ''
    if subject != None and subject != '':
        sql = "SELECT A.RQ_NUM, A.USER_IP, A.QUESTION, A.RGSN_DATE, A.RGSN_TIME, A.RECOMMEND_CNT, A.PC_STATUS, B.ANSWER FROM REQUEST_QUESTION_" + user + "_" + project + " A LEFT JOIN ANSWER_BUILDER_" + user + "_" + project + " B ON A.RQ_NUM = B.RQ_NUM WHERE A.PC_STATUS = '" + pc_status + "' AND A.QUESTION LIKE '%" + subject + "%' ORDER BY A.RQ_NUM DESC"
    else:
        sql = "SELECT A.RQ_NUM, A.USER_IP, A.QUESTION, A.RGSN_DATE, A.RGSN_TIME, A.RECOMMEND_CNT, A.PC_STATUS, B.ANSWER FROM REQUEST_QUESTION_" + user + "_" + project + " A LEFT JOIN ANSWER_BUILDER_" + user + "_" + project + " B ON A.RQ_NUM = B.RQ_NUM WHERE A.PC_STATUS = '" + pc_status + "' ORDER BY A.RQ_NUM DESC "
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['rq_num'] = r[0]
        res_dict['user_ip'] = r[1] 
        res_dict['question'] = r[2]
        res_dict['rgsn_date'] = util.get_hyphen_date(r[3])
        res_dict['rgsn_time'] = util.get_colon_time(r[4])
        res_dict['recommend_cnt'] = r[5]
        res_dict['pc_status'] = r[6]
        res_dict['answer'] = r[7]
        res.append(res_dict)
        
    return res

def search_new_request_by_rq_num(user, project, rq_num):
    sql = "SELECT RQ_NUM, USER_IP, QUESTION, RGSN_DATE, RGSN_TIME, RECOMMEND_CNT, PC_STATUS FROM REQUEST_QUESTION_" + user + "_" + project + " WHERE RQ_NUM = " + rq_num + " ORDER BY RECOMMEND_CNT DESC"
    result = select.fetch(sql)
    res_dict = {}
    res_dict['rq_num'] = result[0][0]
    res_dict['user_ip'] = result[0][1] 
    res_dict['question'] = result[0][2]
    res_dict['rgsn_date'] = util.get_hyphen_date(result[0][3])
    res_dict['rgsn_time'] = util.get_colon_time(result[0][4])
    res_dict['recommend_cnt'] = result[0][5]
    res_dict['pc_status'] = result[0][6]
        
    return res_dict

def update_complete_request(user, project, rq_num):
    sql = "UPDATE REQUEST_QUESTION_" + user + "_" + project + " SET PC_STATUS = '02' WHERE RQ_NUM = " + rq_num
    update.commit(sql)
