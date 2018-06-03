import pymysql
from e_database.properties import get_db_properties 
c_host, c_user, c_password, c_db, c_charset = get_db_properties.get_properties()

def fetch(sql):
    conn = pymysql.connect(host=c_host, user=c_user, password=c_password, db=c_db, charset=c_charset)
    c = conn.cursor()
    c.execute(sql)
    result = c.fetchall()
    conn.close()
    
    return result

def fetch_with_connection(conn, sql):
    c = conn.cursor()
    c.execute(sql)
    result = c.fetchall()
    
    return result
    