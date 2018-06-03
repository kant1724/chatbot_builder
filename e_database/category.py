from e_database.sql_processor import select 
from e_database.sql_processor import update

def search_category():
    sql = "SELECT CATEGORY_NUM, BIG_CATEGORY, MIDDLE_CATEGORY, SMALL_CATEGORY_LV1, SMALL_CATEGORY_LV2, SMALL_CATEGORY_LV3 FROM CATEGORY_LIST"
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['category_num'] = r[0]
        res_dict['big_category'] = r[1]
        res_dict['middle_category'] = r[2]
        res_dict['small_category_lv1'] = r[3]
        res_dict['small_category_lv2'] = r[4]
        res_dict['small_category_lv3'] = r[5]
        res.append(res_dict)

    return res

def search_next_category_num():
    sql = "SELECT MAX(CATEGORY_NUM) + 1 FROM CATEGORY_LIST"
    result = select.fetch(sql)
    next_category_num = 1
    for r in result:
        if r[0] == None:
            next_category_num = 1
        else:
            next_category_num = int(r[0])

    return str(next_category_num)

def insert_category(big_category, middle_category, small_category_lv1, small_category_lv2, small_category_lv3):
    category_num = search_next_category_num()
    sql = "INSERT INTO CATEGORY_LIST VALUES (" + category_num + ", '" + big_category + "', '" + middle_category + "',"
    sql += "'" + small_category_lv1 + "', '" + small_category_lv2 + "', '" + small_category_lv3 + "')"
    update.commit(sql)

def update_category_by_category_num(category_num, big_category, middle_category, small_category_lv1, small_category_lv2, small_category_lv3):
    sql = "UPDATE CATEGORY_LIST SET BIG_CATEGORY = '" + big_category + "',"
    sql += "MIDDLE_CATEGORY = '" + middle_category + "'," 
    sql += "SMALL_CATEGORY_LV1 = '" + small_category_lv1 + "',"
    sql += "SMALL_CATEGORY_LV2 = '" + small_category_lv2 + "',"
    sql += "SMALL_CATEGORY_LV3 = '" + small_category_lv3 + "' "
    sql += "WHERE CATEGORY_NUM = " + str(category_num) 
    update.commit(sql)

def delete_category_by_category_num(category_num):
    sql = "DELETE FROM CATEGORY_LIST WHERE CATEGORY_NUM = " + str(category_num)
    update.commit(sql)
