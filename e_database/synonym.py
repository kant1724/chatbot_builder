from e_database.sql_processor import select 
from e_database.sql_processor import update

def search_synonym_by_synonym_nm(synonym_nm):
    sql = ''
    if synonym_nm != None and synonym_nm != '':
        sql = "SELECT SYNONYM_NUM, SYNONYM_NM, SYNONYM_TAG FROM SYNONYM_LIST WHERE SYNONYM_NM LIKE '%" + synonym_nm + "%'"
    else:
        sql = "SELECT SYNONYM_NUM, SYNONYM_NM, SYNONYM_TAG FROM SYNONYM_LIST"
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['synonym_num'] = r[0]
        res_dict['synonym_nm'] = r[1] 
        res_dict['synonym_tag'] = r[2]
        res.append(res_dict)

    return res

def search_synonym_nm_list_by_synonym_nm(synonym_nm):
    sql = "SELECT SYNONYM_NM FROM SYNONYM_LIST WHERE SYNONYM_TAG = (SELECT SYNONYM_TAG FROM SYNONYM_LIST WHERE SYNONYM_NM = '" + synonym_nm + "')"
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['synonym_nm'] = r[0]
        res.append(res_dict)

    return res

def search_synonym_by_synonym_tag(synonym_tag):
    sql = "SELECT SYNONYM_NUM, SYNONYM_NM, SYNONYM_TAG FROM SYNONYM_LIST WHERE SYNONYM_TAG = '" + synonym_tag + "'"
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['synonym_num'] = r[0]
        res_dict['synonym_nm'] = r[1] 
        res_dict['synonym_tag'] = r[2]
        res.append(res_dict)

    return res

def search_next_synonym_num():
    sql = "SELECT MAX(SYNONYM_NUM) + 1 FROM SYNONYM_LIST"
    result = select.fetch(sql)
    next_synonym_num = 1
    for r in result:
        if r[0] == None:
            next_synonym_num = 1
        else:
            next_synonym_num = int(r[0])

    return str(next_synonym_num)

def insert_synonym(synonym_nm, synonym_tag):
    synonym_num = search_next_synonym_num()
    sql = "INSERT INTO SYNONYM_LIST VALUES (" + synonym_num + ", '" + synonym_nm + "', '" + synonym_tag + "')"
    update.commit(sql)

def update_synonym_by_synonym_num(synonym_num, synonym_nm):
    sql = "UPDATE SYNONYM_LIST SET SYNONYM_NM = '" + synonym_nm + "' WHERE SYNONYM_NUM = " + str(synonym_num)
    update.commit(sql)

def delete_synonym_by_synonym_tag(synonym_tag):
    sql = "DELETE FROM SYNONYM_LIST WHERE SYNONYM_TAG = '" + synonym_tag + "'"
    update.commit(sql)
    
def delete_synonym_by_synonym_num(synonym_num):
    sql = "DELETE FROM SYNONYM_LIST WHERE SYNONYM_NUM = " + synonym_num
    update.commit(sql)
