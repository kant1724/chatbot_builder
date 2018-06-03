from e_database import exporter

def training_config_list_exporter(user, project):
    fw1 = open('./a_builder/exporter/data/training_config_list_' + user + '_' + project, 'w', encoding='utf8')
    result = exporter.get_training_config_list(user, project)
    for rr in result:
        for i in range(len(rr)):
            if i < len(rr) - 1:
                fw1.write(str(rr[i]) + "^")
            else:
                fw1.write(str(rr[i]))
        fw1.write("\n")

def chatbot_config_list_exporter(user, project):
    fw1 = open('./a_builder/exporter/data/chatbot_config_list_' + user + '_' + project, 'w', encoding='utf8')
    result = exporter.get_chatbot_config_list(user, project)
    for rr in result:
        for i in range(len(rr)):
            if i < len(rr) - 1:
                fw1.write(str(rr[i]) + "^")
            else:
                fw1.write(str(rr[i]))
        fw1.write("\n")
