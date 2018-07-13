from e_database.sql_processor import select 
from e_database.sql_processor import update

def search_entity_by_entity_nm(entity_nm):
    sql = ''
    if entity_nm != None and entity_nm != '':
        sql = "SELECT ENTITY_NM FROM ENTITY WHERE ENTITY_NM LIKE '%" + entity_nm + "%'"
    else:
        sql = "SELECT ENTITY_NM FROM ENTITY"
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['entity_nm'] = r[0]
        res.append(res_dict)

    return res

def search_entity_by_equal_entity_nm(entity_nm):
    sql = "SELECT ENTITY_NM FROM ENTITY WHERE ENTITY_NM = '" + entity_nm + "'"
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['entity_nm'] = r[0]
        res.append(res_dict)

    return res

def insert_entity(entity_nm):
    sql = "INSERT INTO ENTITY VALUES ('" + entity_nm + "')"
    update.commit(sql)

def delete_entity_by_entity_nm(entity_nm):
    sql = "DELETE FROM ENTITY WHERE ENTITY_NM = '" + entity_nm + "'"
    update.commit(sql)
