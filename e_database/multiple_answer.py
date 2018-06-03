from e_database.sql_processor import select 
from e_database.sql_processor import update

def search_multiple_answer(answer_num, user, project):
    sql = "SELECT QUESTION, ANSWER FROM ANSWER_MULTIPLE_" + user + "_" + project + " WHERE ANSWER_NUM = '" + answer_num + "'"
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['question'] = r[0]
        res_dict['answer'] = r[1]
        res.append(res_dict)

    return res

def search_multiple_answer_by_srno(answer_num, srno, user, project):
    sql = "SELECT QUESTION, ANSWER FROM ANSWER_MULTIPLE_" + user + "_" + project + " WHERE ANSWER_NUM = '" + answer_num + "' AND SRNO = " + srno
    result = select.fetch(sql)
    res_dict = {}
    res_dict['question'] = result[0][0]
    res_dict['answer'] = result[0][1]

    return res_dict

def delete_all_multiple_answer(answer_num, user, project):
    sql = "DELETE FROM ANSWER_MULTIPLE_" + user + "_" + project + " WHERE ANSWER_NUM = '" + answer_num + "'"
    update.commit(sql)
    
def insert_multiple_answer(answer_num, srno, question, answer, user, project):
    sql = "INSERT INTO ANSWER_MULTIPLE_" + user + "_" + project + " VALUES ('" + answer_num + "', " + str(srno) + ", '" + question + "', '" + answer + "', 0)"
    update.commit(sql)