from e_database.sql_processor import select

def get_password(user_id):    
    sql = "SELECT PASSWORD FROM USER_INFO WHERE USER_ID = '" + user_id + "'"    
    result = select.fetch(sql)
    password = None
    for r in result:
        password = r[0]    
    return password

def get_project(user_id, project):
    sql = "SELECT PROJECT FROM PROJECT_LIST WHERE USER_ID = '" + user_id + "' AND PROJECT = '" + project + "'"
    result = select.fetch(sql)
    project = None
    for r in result:
        project = r[0]
    return project

def get_emno(user_ip):
    sql = "SELECT EMNO FROM EMPL_INFO WHERE USER_IP = '" + user_ip + "'"
    result = select.fetch(sql)
    emno = 'anonymous'
    for r in result:
        emno = r[0]
    return emno
