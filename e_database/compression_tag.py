from e_database.sql_processor import select 
from e_database.sql_processor import update

def search_compression_tag(subject, user, project):
    sql = ''
    if subject != '':
        sql = "SELECT COMPRESSION_NUM, EXPRESSION, TAG_NAME FROM COMPRESSION_TAG_" + user + "_" + project + " WHERE EXPRESSION LIKE '%" + subject + "%' ORDER BY TAG_NAME ASC, COMPRESSION_NUM DESC"
    else:
        sql = "SELECT COMPRESSION_NUM, EXPRESSION, TAG_NAME FROM COMPRESSION_TAG_" + user + "_" + project + " ORDER BY TAG_NAME ASC, COMPRESSION_NUM DESC"
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['compression_num'] = r[0]
        res_dict['expression'] = r[1] 
        res_dict['tag_name'] = r[2]
        res.append(res_dict)

    return res

def search_next_compression_num(user, project):
    sql = "SELECT MAX(COMPRESSION_NUM) + 1 FROM COMPRESSION_TAG_" + user + "_" + project
    result = select.fetch(sql)
    next_compression_num = 1
    for r in result:
        if r[0] == None:
            next_compression_num = 1
        else:
            next_compression_num = int(r[0])

    return str(next_compression_num)

def insert_compression_tag(user, project, expression, tag_name):
    compression_num = search_next_compression_num(user, project)
    sql = "INSERT INTO COMPRESSION_TAG_" + user + "_" + project + " VALUES ('" + compression_num + "', '" + expression + "', '" + tag_name + "')"
    update.commit(sql)
    
def update_compression_tag(user, project, compression_num, expression, tag_name):
    sql = "UPDATE COMPRESSION_TAG_" + user + "_" + project + " SET EXPRESSION = '" + expression + "', TAG_NAME = '" + tag_name + "' WHERE COMPRESSION_NUM = " + str(compression_num)
    update.commit(sql)

def delete_compression_tag(user, project, compression_num):
    sql = "DELETE FROM COMPRESSION_TAG_" + user + "_" + project + " WHERE COMPRESSION_NUM = " + compression_num
    update.commit(sql)
