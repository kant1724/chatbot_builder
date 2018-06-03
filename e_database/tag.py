from e_database.sql_processor import select 
from e_database.sql_processor import update

def search_tag_by_gubun(gubun):
    sql = "SELECT TAG_NUM, TAG_NM, KOR_NM, GUBUN FROM TAG_LIST WHERE GUBUN = '" + gubun + "'"
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['tag_num'] = r[0]
        res_dict['tag_nm'] = r[1] 
        res_dict['kor_nm'] = r[2]
        res_dict['gubun'] = r[3]
        res.append(res_dict)

    return res

def insert_tag_list(tag_nm, kor_nm, gubun):
    tag_num = search_next_tag_num()
    sql = "INSERT INTO TAG_LIST VALUES (" + tag_num + ", '@" + gubun + ":" + tag_nm + "', '" + kor_nm + "', '" + gubun + "')"
    update.commit(sql)
    
def search_next_tag_num():
    sql = "SELECT MAX(TAG_NUM) + 1 FROM TAG_LIST"
    result = select.fetch(sql)
    next_tag_num = 1
    for r in result:
        if r[0] == None:
            next_tag_num = 1
        else:
            next_tag_num = int(r[0])

    return str(next_tag_num)

def get_kor_nm_by_tag_nm(tag_nm):
    sql = "SELECT KOR_NM FROM TAG_LIST WHERE TAG_NM = '" + tag_nm + "'"
    result = select.fetch(sql)
    tag_nm = ''
    if len(result) > 0:
        tag_nm = result[0][0]

    return tag_nm
