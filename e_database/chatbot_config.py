from e_database.sql_processor import select 
from e_database.sql_processor import update

def search_chatbot_config(user, project):
    sql = "SELECT CONFIG_NAME, CONFIG_VALUE FROM CHATBOT_CONFIG_LIST_" + user + "_" + project
    result = select.fetch(sql)
    res = []
    for r in result:
        res_dict = {}
        res_dict['config_name'] = r[0]
        res_dict['config_value'] = r[1] 
        res.append(res_dict)

    return res
    
def update_chatbot_config(user, project, config_name, config_value):
    sql = "UPDATE CHATBOT_CONFIG_LIST_" + user + "_" + project + " SET CONFIG_VALUE = '" + config_value + "' WHERE CONFIG_NAME = '" + config_name + "'"
    update.commit(sql)
