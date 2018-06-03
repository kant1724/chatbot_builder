from a_builder.util import util
from e_database.sql_processor import select 
from e_database.sql_processor import update

def search_wrong_answer(user, project, subject):
    sql = ''
    if subject != None and subject != '':
        sql = "SELECT QUESTION, ANSWER_NUM, RGSN_DATE, RGSN_TIME FROM WRONG_ANSWER WHERE QUESTION LIKE '%" + subject + "%' ORDER BY RGSN_DATE DESC, RGSN_TIME DESC"
    else:
        sql = "SELECT QUESTION, ANSWER_NUM, RGSN_DATE, RGSN_TIME FROM WRONG_ANSWER ORDER BY RGSN_DATE DESC, RGSN_TIME DESC"
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['question'] = r[0]
        res_dict['answer_num'] = r[1]
        res_dict['rgsn_date'] = util.get_hyphen_date(r[2])
        res_dict['rgsn_time'] = util.get_colon_time(r[3])
        res.append(res_dict)
        
    return res
