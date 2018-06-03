import os
from datetime import datetime
from a_builder.util import voca_util
from e_database import question_and_answer as qna
from e_database import generator as db_generator
from e_database import voca as db_voca
from e_database.sql_processor import update

class generator():
    root = './a_builder/user'
    stop_yn = False
    def make_only_one_voca_sentence(self, sent, ans):
        all_voca_sentences, all_voca_answers = [], []
        all_voca = db_voca.search_voca_by_voca_nm('')
        for voca in all_voca:
            voca_nm = voca.get('voca_nm')
            if len(voca_nm) < 2:
                continue
            answer_num = []
            for i in range(len(sent)):
                if voca_nm in sent[i]:
                    if ans[i] not in answer_num:
                        answer_num.append(ans[i])
            if len(answer_num) > 0:
                all_voca_sentences.append(voca_nm)
                all_voca_answers.append(";".join(answer_num))
        return all_voca_sentences, all_voca_answers
        
    def generate_all_fragment(self, user, project):
        self.clear_generating_all_fragment_message(user, project)
        sent = []
        ans = []
        all_sentences = []
        all_answers = []
        res = qna.search_question('', user, project)
        for r in res:
            ans.append(r['answer_num'])
            sent.append(r['question'])
        all_voca_sentences, all_voca_answers = self.make_only_one_voca_sentence(sent, ans)
        all_sentences += all_voca_sentences
        all_answers += all_voca_answers
        for i in range(len(sent)):
            word_arr = sent[i].split(" ")
            answer = ans[i]
            for i in range(len(word_arr) - 1):
                if i == 0:
                    continue
                s = ""
                for j in range(i + 1):
                    s += word_arr[j] + " "
                s = s.strip()
                if s not in all_sentences:
                    all_sentences.append(s)
                    all_answers.append(answer)
                else:
                    for i in range(len(all_sentences)):
                        if all_sentences[i] == s:
                            aa = all_answers[i].split(";")
                            if answer not in aa:
                                all_answers[i] += ";" + answer
                                break
        db_generator.delete_all_question_fragment(user, project)
        all_voca = db_voca.search_voca_by_voca_nm('')
        conn = update.get_connection()
        for i in range(len(all_sentences)):
            if self.stop_yn == True:
                self.end_generating_all_fragment_message(user, project, i + 1, len(all_sentences))
                break
            self.make_generating_all_fragment_message(user, project, i + 1, len(all_sentences))
            question_srno = db_generator.insert_question_fragment(conn, all_answers[i], all_sentences[i], '', user, project)
            question_voca = voca_util.get_voca_from_question(all_sentences[i], all_voca)
            qna.update_all_question_voca_in_fragment(conn, user, project, ";".join(question_voca), all_answers[i], question_srno)
        conn = update.end_connection(conn)
        if self.stop_yn == False:
            self.end_generating_all_fragment_message(user, project, len(all_sentences), len(all_sentences))
        
    def clear_generating_all_fragment_message(self, user, project):
        f1 = open(os.path.join(self.root, user, project, 'generate', 'generating_all_fragment_info'), 'w', encoding='utf8')
        f1.write('')
        f1.close()
        f2 = open(os.path.join(self.root, user, project, 'generate', 'generating_all_fragment_end_yn'), 'w', encoding='utf8')
        f2.write('N')
        f2.close()
        
    def make_generating_all_fragment_message(self, user, project, step, total):
        f = open(os.path.join(self.root, user, project, 'generate', 'generating_all_fragment_info'), 'w', encoding='utf8')
        f.write('진행스탭: ' + str(step) + '/' + str(total) + ', 진행률: ' + str(round(step / total * 100)) + '%')
        f.close()
    
    def end_generating_all_fragment_message(self, user, project, step, total):
        now = datetime.now()
        cur = str(now.year) + '-' + str(now.month) + '-' + str(now.day) + ' ' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second)
        f1 = open(os.path.join(self.root, user, project, 'generate', 'generating_all_fragment_info'), 'w', encoding='utf8')
        f1.write('질문생성 완료: ' + cur + ', 진행스텝: ' + str(step) + '/' + str(total))
        f1.close()
        f2 = open(os.path.join(self.root, user, project, 'generate', 'generating_all_fragment_end_yn'), 'w', encoding='utf8')
        f2.write('Y')
        f2.close()
    
    def stop(self):
        self.stop_yn = True
