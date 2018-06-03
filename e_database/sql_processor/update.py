import pymysql
from e_database.properties import get_db_properties 
c_host, c_user, c_password, c_db, c_charset = get_db_properties.get_properties()

def commit(sql):
    conn = pymysql.connect(host=c_host, user=c_user, password=c_password, db=c_db, charset=c_charset)    
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()

def get_connection():
    return pymysql.connect(host=c_host, user=c_user, password=c_password, db=c_db, charset=c_charset)

def execute(conn, sql):
    c = conn.cursor()
    c.execute(sql)
    
def end_connection(conn):
    conn.commit()
    conn.close()
