from d_service import properties

f = open('./e_database/properties/db_properties')
lines = f.readlines()
host, user, password, db_name, charset = properties.get_db_host_ip(), '', '', '', ''
for line in lines:
    key = line.split("=")[0]
    val = line.split("=")[1].replace("\n", '')
    if key == 'user':
        user = val
    elif key == 'password':
        password = val
    elif key == "db_name":
        db_name = val
    elif key == "charset":
        charset = val
f.close()

def get_properties():
    return host, user, password, db_name, charset 
