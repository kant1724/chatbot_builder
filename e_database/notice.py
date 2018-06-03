from a_builder.util import util
from e_database.sql_processor import select 
from e_database.sql_processor import update

def search_notice_list(user, project, notice_subject, complete_yn):
    sql = ''
    if notice_subject != None and notice_subject != '':
        sql = "SELECT NOTICE_NUM, NOTICE_SUBJECT, NOTICE_CONTENT, IMAGE_CNT, RGSN_DATE, NOTICE_START_DATE, NOTICE_END_DATE, COMPLETE_YN FROM NOTICE_LIST_" + user + "_" + project + " WHERE COMPLETE_YN= '" + complete_yn + "' AND NOTICE_SUBJECT LIKE '%" + notice_subject + "%' ORDER BY NOTICE_NUM DESC"
    else:
        sql = "SELECT NOTICE_NUM, NOTICE_SUBJECT, NOTICE_CONTENT, IMAGE_CNT, RGSN_DATE, NOTICE_START_DATE, NOTICE_END_DATE, COMPLETE_YN FROM NOTICE_LIST_" + user + "_" + project + " WHERE COMPLETE_YN= '" + complete_yn + "' ORDER BY NOTICE_NUM DESC"
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['notice_num'] = r[0]
        res_dict['notice_subject'] = r[1] 
        res_dict['notice_content'] = r[2]
        res_dict['image_cnt'] = r[3]
        res_dict['rgsn_date'] = util.get_colon_time(r[4])
        res_dict['notice_start_date'] = r[5]
        res_dict['notice_end_date'] = r[6]
        res_dict['complete_yn'] = r[7]
        res.append(res_dict)
        
    return res

def search_notice_list_by_notice_num(user, project, notice_num):
    sql = "SELECT NOTICE_NUM, NOTICE_SUBJECT, NOTICE_CONTENT, IMAGE_CNT, RGSN_DATE, NOTICE_START_DATE, NOTICE_END_DATE, COMPLETE_YN FROM NOTICE_LIST_" + user + "_" + project + " WHERE NOTICE_NUM = " + notice_num
    result = select.fetch(sql)
    res_dict = {}
    res_dict['notice_num'] = result[0][0]
    res_dict['notice_subject'] = result[0][1] 
    res_dict['notice_content'] = result[0][2]
    res_dict['image_cnt'] = result[0][3]
    res_dict['rgsn_date'] = util.get_colon_time(result[0][4])
    res_dict['notice_start_date'] = result[0][5]
    res_dict['notice_end_date'] = result[0][6]
    res_dict['complete_yn'] = result[0][7]
        
    return res_dict

def get_next_notice_num(user, project):
    sql = "SELECT MAX(NOTICE_NUM) + 1 FROM NOTICE_LIST_" + user + "_" + project
    result = select.fetch(sql)
    max_notice_num = 1
    if result[0][0] != None:
        max_notice_num = result[0][0]

    return str(max_notice_num)

def insert_notice(user, project, notice_subject, notice_content, notice_start_date, notice_end_date):
    notice_num = get_next_notice_num(user, project)
    sql = "INSERT INTO NOTICE_LIST_" + user + "_" + project + " VALUES ('" + notice_num + "', '" + notice_subject + "', '" + notice_content + "', 0, CAST(DATE_FORMAT(NOW(), '%Y%m%d') AS CHAR), '" + notice_start_date + "', '" + notice_end_date + "', 'N')"
    update.commit(sql)

def update_notice(user, project, notice_num, notice_subject, notice_content, notice_start_date, notice_end_date):
    sql = "UPDATE NOTICE_LIST_" + user + "_" + project + " SET NOTICE_SUBJECT = '" + notice_subject + "', NOTICE_CONTENT = '" + notice_content + "', NOTICE_START_DATE = '" + notice_start_date + "', NOTICE_END_DATE = '" + notice_end_date + "' WHERE NOTICE_NUM = " + notice_num
    update.commit(sql)

def delete_notice(user, project, notice_num):
    sql = "DELETE FROM NOTICE_LIST_" + user + "_" + project + " WHERE NOTICE_NUM = " + notice_num
    update.commit(sql)

def update_notice_complete(user, project, notice_num):
    sql = "UPDATE NOTICE_LIST_" + user + "_" + project + " SET COMPLETE_YN = 'Y' WHERE NOTICE_NUM = " + notice_num
    update.commit(sql)
