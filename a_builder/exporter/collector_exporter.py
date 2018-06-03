from e_database import exporter

def question_list_exporter():
    fw1 = open('./a_builder/exporter/data/question_list', 'w', encoding='utf8')
    result = exporter.get_question_list()
    for rr in result:
        for i in range(len(rr)):
            if i < len(rr) - 1:
                fw1.write(str(rr[i]).replace('\n', ' ') + "^")
            else:
                fw1.write(str(rr[i]).replace('\n', ' '))
        fw1.write("\n")
        
def my_question_exporter():
    fw1 = open('./a_builder/exporter/data/my_question', 'w', encoding='utf8')
    result = exporter.get_my_question()
    for rr in result:
        for i in range(len(rr)):
            if i < len(rr) - 1:
                fw1.write(str(rr[i]).replace('\n', ' ') + "^")
            else:
                fw1.write(str(rr[i]).replace('\n', ' '))
        fw1.write("\n")
        
def right_answer_exporter():
    fw1 = open('./a_builder/exporter/data/right_answer', 'w', encoding='utf8')
    result = exporter.get_right_answer()
    for rr in result:
        for i in range(len(rr)):
            if i < len(rr) - 1:
                fw1.write(str(rr[i]).replace('\n', ' ') + "^")
            else:
                fw1.write(str(rr[i]).replace('\n', ' '))
        fw1.write("\n")
        

def wrong_answer_exporter():
    fw1 = open('./a_builder/exporter/data/wrong_answer', 'w', encoding='utf8')
    result = exporter.get_wrong_answer()
    for rr in result:
        for i in range(len(rr)):
            if i < len(rr) - 1:
                fw1.write(str(rr[i]).replace('\n', ' ') + "^")
            else:
                fw1.write(str(rr[i]).replace('\n', ' '))
        fw1.write("\n")
