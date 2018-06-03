from e_database import importer

def training_config_list_importer(user, project):
    fw1 = open('./a_builder/importer/data/training_config_list_' + user + '_' + project, 'r', encoding='utf8')
    lines = fw1.readlines()
    for line in lines:
        line = line.replace('\n', '')
        arr = line.split("^")
        importer.import_training_config_list(user, project, arr)

def chatbot_config_list_importer(user, project):
    fw1 = open('./a_builder/importer/data/chatbot_config_list_' + user + '_' + project, 'r', encoding='utf8')
    lines = fw1.readlines()
    for line in lines:
        line = line.replace('\n', '')
        arr = line.split("^")
        importer.import_chatbot_config_list(user, project, arr)
 