import os
from datetime import datetime
from e_database import question_and_answer as qna
from e_database import voca as db_voca
from e_database.sql_processor import update
from a_builder.util import voca_util

class updater():
    root = './a_builder/user'
    stop_yn = False
    def update_question_voca(self, answer_num, user, project, thread_yn):
        if thread_yn == 'Y':
            self.clear_updating_message(user, project)
        res = qna.search_question(answer_num, user, project)
        fragment = qna.search_question_fragment(answer_num, user, project)
        res += fragment
        all_voca = db_voca.search_voca_by_voca_nm('')
        conn = update.get_connection()
        for i in range(len(res)):
            if thread_yn == 'Y':
                if self.stop_yn == True:
                    self.end_updating_message(user, project, i + 1, len(res))
                    break
                self.make_updating_message(user, project, i + 1, len(res))
            answer_num = res[i]['answer_num']
            question_srno = res[i]['question_srno']
            question_voca = voca_util.get_voca_from_question(res[i]['question'], all_voca)
            if len(question_voca) == 0:
                continue
            if res[i]['fragment_yn'] == 'N':
                qna.update_all_question_voca(conn, user, project, ";".join(question_voca), answer_num, question_srno)
            else:
                qna.update_all_question_voca_in_fragment(conn, user, project, ";".join(question_voca), answer_num, question_srno)
        update.end_connection(conn)        
        if thread_yn == 'Y':
            if self.stop_yn == False:
                self.end_updating_message(user, project, len(res), len(res))
            
    def clear_updating_message(self, user, project):
        f1 = open(os.path.join(self.root, user, project, 'update', 'updating_info'), 'w', encoding='utf8')
        f1.write('')
        f1.close()
        f2 = open(os.path.join(self.root, user, project, 'update', 'updating_end_yn'), 'w', encoding='utf8')
        f2.write('N')
        f2.close()
        
    def make_updating_message(self, user, project, step, total):
        f = open(os.path.join(self.root, user, project, 'update', 'updating_info'), 'w', encoding='utf8')
        f.write('진행스탭: ' + str(step) + '/' + str(total) + ', 진행률: ' + str(round(step / total * 100)) + '%')
        f.close()
    
    def end_updating_message(self, user, project, step, total):
        now = datetime.now()
        cur = str(now.year) + '-' + str(now.month) + '-' + str(now.day) + ' ' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second)
        f1 = open(os.path.join(self.root, user, project, 'update', 'updating_info'), 'w', encoding='utf8')
        f1.write('업데이트 완료: ' + cur + ', 진행스텝: ' + str(step) + '/' + str(total))
        f1.close()
        f2 = open(os.path.join(self.root, user, project, 'update', 'updating_end_yn'), 'w', encoding='utf8')
        f2.write('Y')
        f2.close()

    def stop(self):
        self.stop_yn = True
