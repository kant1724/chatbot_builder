from c_engine.core.message_manager import message_container
from c_engine.core.error_detector import sentence_comparator
from d_service import properties
from e_database import question_and_answer as qna
from e_database import multiple_answer as db_multiple_answer

file_ip = open('./server_ip', encoding="utf8").readlines()[3].split("=")[1].replace('\n', '')

def get_faq_answer(user, project, msg, answer_num, answer, question, message_count, mdfc_rgsn_date):
    trained_yn = False
    cnt = 0
    image_path = []
    if sentence_comparator.compare_by_formula(user, project, question, answer_num) == False:
        msg.append(message_container.get_not_trained_message())
        right_yn = message_container.get_wrong_input_msg(message_count)
    else:
        trained_yn = True
        msg.append(answer + message_container.get_last_mdfc_date(mdfc_rgsn_date))
        right_yn = message_container.get_right_yn_href_msg(message_count)
        cnt = qna.search_image_cnt_in_answer(user, project, answer_num)
        path = properties.get_image_file_root_path() + user + '/' + project + '/' + answer_num
        if cnt != None and cnt > 0:
            for i in range(cnt):
                image_path.append('http://' + file_ip + path + '/image' + str(i + 1) + '.jpg') 
        
    return msg, right_yn, image_path, trained_yn

def get_reserve_question_list(question, answer_num, answer_num_and_rpsn_question):
    if len(question) == 1:
        message = message_container.get_not_trained_message()
    else:
        all_ans = answer_num.split(";")
        message = message_container.get_select_question_from_list()
        has = 0
        for i in range(len(all_ans)):
            reserve_question = answer_num_and_rpsn_question.get(all_ans[i], '')
            question_arr = question.split(" ")
            for q in question_arr:
                if q in reserve_question.replace(" ", ""):
                    has += 1
                    break
            message += message_container.get_reserve_question(reserve_question)
        if has < len(all_ans) / 3:
            print('포함단어 :', has, '전체 :', len(all_ans))
            message = message_container.get_not_trained_message()
    
    return message

def check_multiple_answer(answer_num, user, project):
    res = db_multiple_answer.search_multiple_answer(answer_num, user, project)
    if len(res) > 0:
        multiple_answer = message_container.get_select_answer_from_list()
        for i in range(len(res)):
            multiple_answer += str(i + 1) + '. ' + res[i]['question'] + '<br><br>'

        return answer_num, multiple_answer
    
    return '', ''

def get_answer_in_multiple(answer_num, srno, user, project):
    res = db_multiple_answer.search_multiple_answer_by_srno(answer_num, srno, user, project)
    
    return [res['answer']]
