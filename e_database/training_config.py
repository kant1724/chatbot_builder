from e_database.sql_processor import select 
from e_database.sql_processor import update

def search_training_config(user, project):
    sql = "SELECT CONFIG_NAME, CONFIG_VALUE FROM TRAINING_CONFIG_LIST_" + user + "_" + project
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['config_name'] = r[0]
        res_dict['config_value'] = r[1] 
        res.append(res_dict)

    return res
    
def update_training_config(user, project, config_name, config_value):
    sql = "UPDATE TRAINING_CONFIG_LIST_" + user + "_" + project + " SET CONFIG_VALUE = '" + config_value + "' WHERE CONFIG_NAME = '" + config_name + "'"
    update.commit(sql)

def get_project_language(user, project):
    sql = "SELECT LANGUAGE FROM PROJECT_LIST WHERE USER_ID = '" + user + "' AND PROJECT = '" + project + "'"
    result = select.fetch(sql)
    res = ''
    for r in result:
        res = r[0]

    return res

def get_bucket(user, project):
    sql = "SELECT CONFIG_VALUE FROM TRAINING_CONFIG_LIST_" + user + "_" + project + " WHERE CONFIG_NAME = 'BUCKET'"
    result = select.fetch(sql)
    bucket = 1
    if len(result) > 0:
        bucket = result[0][0]

    return bucket
