from e_database.sql_processor import select 
from e_database.sql_processor import update

def search_next_question_fragment_srno(conn, user, project):
    sql = "SELECT MAX(QUESTION_SRNO) + 1 FROM QUESTION_FRAGMENT_BUILDER_" + user + "_" + project
    result = select.fetch_with_connection(conn, sql)
    next_question_srno = 1
    for r in result:
        if r[0] == None:
            next_question_srno = 1
        else:
            next_question_srno = int(r[0])

    return str(next_question_srno)

def delete_all_question_fragment(user, project):
    sql = "DELETE FROM QUESTION_FRAGMENT_BUILDER_" + user + "_" + project
    update.commit(sql)

def insert_question_fragment(conn, answer_num, question, question_voca, user, project):
    question_srno = search_next_question_fragment_srno(conn, user, project)
    sql = "INSERT INTO QUESTION_FRAGMENT_BUILDER_" + user + "_" + project + " VALUES ('" + answer_num + "', '" + question_srno + "', '" + question + "', '" + question_voca + "')"
    update.execute(conn, sql)
    return question_srno
