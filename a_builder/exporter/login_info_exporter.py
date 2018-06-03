from e_database import exporter

def user_info_exporter():
    fw1 = open('./a_builder/exporter/data/user_info', 'w', encoding='utf8')
    result = exporter.get_user_info()
    for rr in result:
        for i in range(len(rr)):
            if i < len(rr) - 1:
                fw1.write(str(rr[i]) + "^")
            else:
                fw1.write(str(rr[i]))
        fw1.write("\n")
        
def project_list_exporter():
    fw1 = open('./a_builder/exporter/data/project_list', 'w', encoding='utf8')
    result = exporter.get_project_list()
    for rr in result:
        for i in range(len(rr)):
            if i < len(rr) - 1:
                fw1.write(str(rr[i]) + "^")
            else:
                fw1.write(str(rr[i]))
        fw1.write("\n")
