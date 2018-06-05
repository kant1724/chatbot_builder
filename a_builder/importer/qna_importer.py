from e_database import importer

def question_builder_importer(user, project):
    fw1 = open('./a_builder/importer/data/question_builder_' + user + '_' + project, 'r', encoding='utf8')
    lines = fw1.readlines()
    for line in lines:
        line = line.replace('\n', '')
        arr = line.split("^")
        for i in range(len(arr)):
            if arr[i] == 'None':
                arr[i] = 'null'
        importer.import_question_builder(user, project, arr)

def answer_builder_importer(user, project):
    fw1 = open('./a_builder/importer/data/answer_builder_' + user + '_' + project, 'r', encoding='utf8')
    lines = fw1.readlines()
    for line in lines:
        line = line.replace('\n', '')
        arr = line.split("^")
        for i in range(len(arr)):
            if arr[i] == 'None':
                arr[i] = 'null'
        importer.import_answer_builder(user, project, arr)
        
def compression_tag_importer(user, project):
    fw1 = open('./a_builder/importer/data/compression_tag_' + user + '_' + project, 'r', encoding='utf8')
    lines = fw1.readlines()
    for line in lines:
        line = line.replace('\n', '')
        arr = line.split("^")
        for i in range(len(arr)):
            if arr[i] == 'None':
                arr[i] = 'null'
        importer.import_compression_tag(user, project, arr)
 