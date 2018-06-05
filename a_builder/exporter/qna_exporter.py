from e_database import exporter

def question_builder_exporter(user, project):
    fw1 = open('./a_builder/exporter/data/question_builder_' + user + '_' + project, 'w', encoding='utf8')
    result = exporter.get_question_builder(user, project)
    for rr in result:
        for i in range(len(rr)):
            if i < len(rr) - 1:
                fw1.write(str(rr[i]).replace('\n', ' ') + "^")
            else:
                fw1.write(str(rr[i]).replace('\n', ' '))
        fw1.write("\n")

def question_fragment_builder_exporter(user, project):
    fw1 = open('./a_builder/exporter/data/question_fragment_builder_' + user + '_' + project, 'w', encoding='utf8')
    result = exporter.get_question_fragment_builder(user, project)
    for rr in result:
        for i in range(len(rr)):
            if i < len(rr) - 1:
                fw1.write(str(rr[i]).replace('\n', ' ') + "^")
            else:
                fw1.write(str(rr[i]).replace('\n', ' '))
        fw1.write("\n")

def answer_builder_exporter(user, project):
    fw1 = open('./a_builder/exporter/data/answer_builder_' + user + '_' + project, 'w', encoding='utf8')
    result = exporter.get_answer_builder(user, project)
    for rr in result:
        for i in range(len(rr)):
            if i < len(rr) - 1:
                fw1.write(str(rr[i]).replace('\n', ' ') + "^")
            else:
                fw1.write(str(rr[i]).replace('\n', ' '))
        fw1.write("\n")

def dialogue_list_exporter():
    fw1 = open('./a_builder/exporter/data/dialogue_list', 'w', encoding='utf8')
    result = exporter.get_dialogue_list()
    for rr in result:
        for i in range(len(rr)):
            if i < len(rr) - 1:
                fw1.write(str(rr[i]).replace('\n', ' ') + "^")
            else:
                fw1.write(str(rr[i]).replace('\n', ' '))
        fw1.write("\n")
                
def compression_tag_exporter(user, project):
    fw1 = open('./a_builder/exporter/data/compression_tag_' + user + '_' + project, 'w', encoding='utf8')
    result = exporter.get_compression_tag(user, project)
    for rr in result:
        for i in range(len(rr)):
            if i < len(rr) - 1:
                fw1.write(str(rr[i]).replace('\n', ' ') + "^")
            else:
                fw1.write(str(rr[i]).replace('\n', ' '))
        fw1.write("\n")
