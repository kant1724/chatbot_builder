from e_database.sql_processor import select 
from e_database.sql_processor import update

def search_voca_by_voca_nm(voca_nm):
    sql = ''
    if voca_nm != None and voca_nm != '':
        sql = "SELECT VOCA_NM, VOCA_SYNONYM, KEYWORD_YN FROM VOCA WHERE VOCA_NM LIKE '%" + voca_nm + "%'"
    else:
        sql = "SELECT VOCA_NM, VOCA_SYNONYM, KEYWORD_YN FROM VOCA"
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['voca_nm'] = r[0]
        res_dict['voca_synonym'] = r[1]
        res_dict['keyword_yn'] = r[2]
        res.append(res_dict)

    return res

def search_voca_by_equal_voca_nm(voca_nm, keyword_yn):
    sql = ''
    if keyword_yn != '':
        sql = "SELECT VOCA_NM, VOCA_SYNONYM, KEYWORD_YN FROM VOCA WHERE VOCA_NM = '" + voca_nm + "' AND KEYWORD_YN = '" + keyword_yn + "'"
    else:
        sql = "SELECT VOCA_NM, VOCA_SYNONYM, KEYWORD_YN FROM VOCA WHERE VOCA_NM = '" + voca_nm + "'"
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['voca_nm'] = r[0]
        res_dict['voca_synonym'] = r[1]
        res_dict['keyword_yn'] = r[2] 
        res.append(res_dict)

    return res

def insert_voca(voca_nm):
    sql = "INSERT INTO VOCA VALUES ('" + voca_nm + "', '" + voca_nm + "', 'Y')"
    update.commit(sql)

def delete_voca_by_voca_nm(voca_nm):
    sql = "DELETE FROM VOCA WHERE VOCA_NM = '" + voca_nm + "'"
    update.commit(sql)
    
def update_voca_synonym(voca_synonym, voca_nm):
    sql = "UPDATE VOCA SET VOCA_SYNONYM = '" + voca_synonym + "' WHERE VOCA_NM = '" + voca_nm + "'"
    update.commit(sql)
    
def update_keyword_yn(voca_nm):
    sql = "UPDATE VOCA SET KEYWORD_YN = CASE WHEN KEYWORD_YN = 'Y' THEN '' ELSE 'Y' END WHERE VOCA_NM = '" + voca_nm + "'"
    update.commit(sql)
