from b_trainer.worker import connect_file

def get_answer_and_answer_num(user, project):
    res = connect_file.get_training_data(user, project)
    ad = eval(res['answer_dict'])
    answer_dict = {}
    for line in ad:
        l = line.replace('\n', '')
        ll = l.split('^')
        answer_dict[ll[1]] = ll[0]
        
    return answer_dict
