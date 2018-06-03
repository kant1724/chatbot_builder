from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
from flask_cors import CORS
from d_service import search
from d_service import submit
from d_service import modify
from d_service import delete
from d_service import popup
from d_service import trainer
from d_service import login as login_service
from d_service import main
from d_service import chat
from d_service import chat_popup
from d_service import updater
from d_service import analysis
from d_service import generator
from d_service import properties
from d_service import bucket
from d_service import config
from d_service import compression_tag

ip_addr = properties.get_builder_ip()

app = Flask(__name__, static_url_path="/static") 
app.secret_key = "chatbot_secret_key"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
CORS(app)

generator_thread = []
updater_thread = []
no_check_session = ['login', 'login_chat', 'login_try', 'static']

@app.before_request
def before_request():
    if request.endpoint not in no_check_session:
        my_session = session.get('k', None)
        if my_session == None:
            return render_template("login/no_session.html")
        
@app.route('/search_answer', methods=['POST'])
def search_answer():
    return search.search_answer(request)

@app.route('/search_answer_by_answer_num', methods=['POST'])
def search_answer_by_answer_num():
    return search.search_answer_by_answer_num(request)

@app.route('/search_multiple_answer', methods=['POST'])
def search_multiple_answer():
    return search.search_multiple_answer(request)

@app.route('/search_question', methods=['POST'])
def search_question():
    return search.search_question(request)

@app.route('/search_compression_tag', methods=['POST'])
def search_compression_tag():
    return search.search_compression_tag(request)

@app.route('/search_tag', methods=['POST'])
def search_tag():
    return search.search_tag(request)

@app.route('/search_synonym', methods=['POST'])
def search_synonym():
    return search.search_synonym(request)

@app.route('/search_voca', methods=['POST'])
def search_voca():
    return search.search_voca(request)

@app.route('/search_voca_and_appearance', methods=['POST'])
def search_voca_and_appearance():
    return search.search_voca_and_appearance(request)

@app.route('/search_synonym_by_synonym_tag', methods=['POST'])
def search_synonym_by_synonym_tag():
    return search.search_synonym_by_synonym_tag(request)

@app.route('/search_answer_num_and_question_voca', methods=['POST'])
def search_answer_num_and_question_voca():
    return search.search_answer_num_and_question_voca(request)

@app.route('/search_category', methods=['POST'])
def search_category():
    return search.search_category(request)

@app.route('/search_notice', methods=['POST'])
def search_notice():
    return search.search_notice(request)

@app.route('/search_new_request', methods=['POST'])
def search_new_request():
    return search.search_new_request(request)

@app.route('/search_new_request_by_rq_num', methods=['POST'])
def search_new_request_by_rq_num():
    return search.search_new_request_by_rq_num(request)

@app.route('/search_training_config', methods=['POST'])
def search_training_config():
    return search.search_training_config(request)

@app.route('/search_chatbot_config', methods=['POST'])
def search_chatbot_config():
    return search.search_chatbot_config(request)

@app.route('/search_bucket_id', methods=['POST'])
def search_bucket_id():
    return bucket.search_bucket_id(request)

@app.route('/search_question_and_bucket_id', methods=['POST'])
def search_question_and_bucket_id():
    return bucket.search_question_and_bucket_id(request)

@app.route('/search_wrong_answer', methods=['POST'])
def search_wrong_answer():
    return search.search_wrong_answer(request)

@app.route('/search_bucket_id_by_sentence', methods=['POST'])
def search_bucket_id_by_sentence():
    return search.search_bucket_id_by_sentence(request)

@app.route('/compare_my_question_and_right_question', methods=['POST'])
def compare_my_question_and_right_question():
    return analysis.compare_my_question_and_right_question(request)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    return submit.submit_answer(request)

@app.route('/submit_multiple_answer', methods=['POST'])
def submit_multiple_answer():
    return submit.submit_multiple_answer(request)

@app.route('/submit_image', methods=['POST'])
def submit_image():
    return submit.submit_image(request)

@app.route('/submit_question', methods=['POST'])
def submit_question():
    return submit.submit_question(request)

@app.route('/submit_compression_tag', methods=['POST'])
def submit_compression_tag():
    return submit.submit_compression_tag(request)

@app.route('/submit_tag', methods=['POST'])
def submit_tag():
    return submit.submit_tag(request)

@app.route('/submit_synonym', methods=['POST'])
def submit_synonym():
    return submit.submit_synonym(request)

@app.route('/submit_voca', methods=['POST'])
def submit_voca():
    return submit.submit_voca(request)

@app.route('/submit_voca_keyword', methods=['POST'])
def submit_voca_keyword():
    return submit.submit_voca_keyword(request)

@app.route('/submit_category', methods=['POST'])
def submit_category():
    return submit.submit_category(request)

@app.route('/submit_notice', methods=['POST'])
def submit_notice():
    return submit.submit_notice(request)

@app.route('/submit_training_config', methods=['POST'])
def submit_training_config():
    return config.submit_training_config(request)

@app.route('/submit_complete_request', methods=['POST'])
def submit_complete_request():
    return submit.submit_complete_request(request)

@app.route('/submit_chatbot_config', methods=['POST'])
def submit_chatbot_config():
    return config.submit_chatbot_config(request)

@app.route('/submit_notice_complete', methods=['POST'])
def submit_notice_complete():
    return submit.submit_notice_complete(request)

@app.route('/modify_answer', methods=['POST'])
def modify_answer():
    return modify.modify_answer(request)

@app.route('/delete_answer', methods=['POST'])
def delete_answer():
    return delete.delete_answer(request)

@app.route('/delete_question', methods=['POST'])
def delete_question():
    return delete.delete_question(request)

@app.route('/delete_compression_tag', methods=['POST'])
def delete_compression_tag():
    return delete.delete_compression_tag(request)

@app.route('/delete_synonym_master', methods=['POST'])
def delete_synonym_master():
    return delete.delete_synonym_master(request)

@app.route('/delete_synonym_detail', methods=['POST'])
def delete_synonym_detail():
    return delete.delete_synonym_detail(request)

@app.route('/delete_voca', methods=['POST'])
def delete_voca():
    return delete.delete_voca(request)

@app.route('/delete_category', methods=['POST'])
def delete_category():
    return delete.delete_category(request)

@app.route('/delete_notice', methods=['POST'])
def delete_notice():
    return delete.delete_notice(request)

@app.route("/easy_manager_pop")
def easy_manager_pop():
    return popup.easy_manager_pop(request)

@app.route("/new_answer_pop")
def new_answer_pop():
    return popup.new_answer_pop(request)

@app.route("/multiple_answer_pop")
def multiple_answer_pop():
    return popup.multiple_answer_pop(request)

@app.route("/add_image_pop")
def add_image_pop():
    return popup.add_image_pop(request)

@app.route("/new_function_pop")
def new_function_pop():
    return popup.new_function_pop(request)

@app.route("/new_question_pop", methods=['GET'])
def new_question_pop(): 
    return popup.new_question_pop(request)

@app.route("/new_tag_pop", methods=['GET'])
def new_tag_pop(): 
    return popup.new_tag_pop(request)

@app.route("/new_synonym_pop", methods=['GET'])
def new_synonym_pop(): 
    return popup.new_synonym_pop(request)

@app.route("/modify_answer_pop", methods=['POST'])
def modify_answer_pop(): 
    return popup.modify_answer_pop(request)

@app.route("/new_notice_pop")
def new_notice_pop():
    return popup.new_notice_pop(request)

@app.route("/train_main")
def train_main(): 
    return main.train_main(request)

@app.route('/update_question_voca_main')
def update_question_voca_main():
    return main.update_question_voca_main(request, updater_thread)

@app.route("/synonym_manager_main", methods=['GET'])
def synonym_manager_main(): 
    return main.synonym_manager_main(request)

@app.route("/voca_manager_main", methods=['GET'])
def voca_manager_main(): 
    return main.voca_manager_main(request)

@app.route("/category_manager_main", methods=['GET'])
def category_manager_main(): 
    return main.category_manager_main(request)

@app.route("/error_detection_main", methods=['GET'])
def error_detection_main(): 
    return main.error_detection_main(request)

@app.route("/question_generator_main", methods=['GET'])
def question_generator_main(): 
    return main.question_generator_main(request, generator_thread)

@app.route("/new_request_main", methods=['GET'])
def new_request_main(): 
    return main.new_request_main(request)

@app.route("/chatbot_config_main", methods=['GET'])
def chatbot_config_main(): 
    return main.chatbot_config_main(request)

@app.route("/bucket_manager_main", methods=['GET'])
def bucket_manager_main(): 
    return main.bucket_manager_main(request)

@app.route("/notice_manager_main", methods=['GET'])
def notice_manager_main(): 
    return main.notice_manager_main(request)

@app.route("/training_test_main")
def training_test_main(): 
    return main.training_test_main(request)

@app.route("/error_statistics_main")
def error_statistics_main(): 
    return main.error_statistics_main(request)

@app.route("/delete_ckpt_file", methods=['POST'])
def delete_ckpt_file(): 
    return trainer.delete_ckpt_file(request)

@app.route("/start_training", methods=['POST'])
def start_training(): 
    return trainer.start_training(request)

@app.route("/stop_training", methods=['POST'])
def stop_training(): 
    return trainer.stop_training(request)

@app.route("/get_training_info", methods=['POST'])
def get_training_info():
    return trainer.get_training_info(request)

@app.route("/get_is_training", methods=['POST'])
def get_is_training():
    return trainer.get_is_training(request)

@app.route("/send_training_test_question", methods=['POST'])
def send_training_test_question():
    return trainer.send_training_test_question(request)

@app.route("/get_compression_tag", methods=['POST'])
def get_compression_tag(): 
    return compression_tag.get_compression_tag(request)

@app.route("/delete_compression_tag_ckpt_file", methods=['POST'])
def delete_compression_tag_ckpt_file(): 
    return trainer.delete_compression_tag_ckpt_file(request)

@app.route("/start_compression_tag_training", methods=['POST'])
def start_compression_tag_training(): 
    return trainer.start_compression_tag_training(request)

@app.route("/stop_compression_tag_training", methods=['POST'])
def stop_compression_tag_training(): 
    return trainer.stop_compression_tag_training(request)

@app.route("/get_compression_tag_training_info", methods=['POST'])
def get_compression_tag_training_info():
    return trainer.get_compression_tag_training_info(request)

@app.route("/get_is_compression_tag_training", methods=['POST'])
def get_is_compression_tag_training():
    return trainer.get_is_compression_tag_training(request)

@app.route("/update_voca_synonym", methods=['POST'])
def update_voca_synonym():
    return updater.update_voca_synonym(request)

@app.route("/update_question_voca", methods=['POST'])
def update_question_voca():
    return updater.update_question_voca(request)

@app.route("/start_updating")
def start_updating(): 
    return updater.start_updating(request, updater_thread)

@app.route("/stop_updating")
def stop_updating(): 
    return updater.stop_updating(request, updater_thread)

@app.route("/get_updating_info", methods=['POST'])
def get_updating_info(): 
    return updater.get_updating_info(request, updater_thread)

@app.route("/start_generating_all_fragment")
def start_generating_all_fragment(): 
    return generator.start_generating_all_fragment(request, generator_thread)

@app.route("/stop_generating_all_fragment")
def stop_generating_all_fragment(): 
    return generator.stop_generating_all_fragment(request, generator_thread)

@app.route("/get_generating_all_fragment_info", methods=['POST'])
def get_generating_all_fragment_info(): 
    return generator.get_generating_all_fragment_info(request, generator_thread)

@app.route("/login_try", methods=['POST'])
def login_try(): 
    res = login_service.login_try(request)
    if res['success'] == 'Y':
        session['k'] = 'v'
    return jsonify(res)

@app.route("/frame", methods=['GET'])
def frame():
    user = request.args.get('user')
    project = request.args.get('project')
    emno = request.args.get('emno')
    return render_template("frame.html", user = user, project = project, emno = emno)

@app.route("/my_page_main", methods=['GET'])
def my_page_main():
    return main.my_page_main(request)

@app.route("/qna_main", methods=['GET'])
def qna_main():
    return main.qna_main(request)

@app.route("/compression_tag_main", methods=['GET'])
def compression_tag_main():
    return main.compression_tag_main(request)

@app.route("/")
def login():
    return login_service.login(request)

@app.route("/login_chat")
def login_chat():
    return login_service.login_chat(request)

@app.route("/login_success")
def login_success():
    return login_service.login_success(request)

@app.route("/logout", methods=['GET'])
def logout(): 
    session.pop('k', None)
    return login_service.logout(request)

@app.route("/loading", methods=['POST'])
def loading():
    return main.loading(request)

####chat
@app.route("/chat_bot", methods=['POST'])
def chat_bot(): 
    return chat.chat_bot(request)

@app.route("/chat_window")
def chat_window(): 
    return chat.chat_window(request)

@app.route("/dynamic_grid_pop", methods=['POST'])
def dynamic_grid_pop(): 
    return chat_popup.dynamic_grid_pop(request)

@app.route("/dynamic_info_pop", methods=['POST'])
def dynamic_info_pop(): 
    return chat_popup.dynamic_info_pop(request)

@app.route("/hwp_report_pop", methods=['POST'])
def hwp_report_pop(): 
    return chat_popup.hwp_report_pop(request)

@app.route("/group_chat")
def group_chat(): 
    return chat.group_chat(request)

@app.route("/create_new_chat_room", methods=['POST'])
def create_new_chat_room(): 
    return chat.create_new_chat_room(request)

@app.route("/enter_chat_room", methods=['POST'])
def enter_chat_room(): 
    return chat.enter_chat_room(request)

@app.route("/action_principle")
def action_principle(): 
    return chat.action_principle(request)

@app.route("/get_action_principle", methods=['POST'])
def get_action_principle(): 
    return chat.get_action_principle(request)

@app.route("/is_chatbot_ready", methods=['POST'])
def is_chatbot_ready(): 
    return chat.is_chatbot_ready(request)

@app.route('/message', methods=['POST'])
def reply():
    return chat.reply(request)

@app.route('/reply_dynamic_popup', methods=['POST'])
def reply_dynamic_popup():
    return chat.reply_dynamic_popup(request)

@app.route('/message_group_chat', methods=['POST'])
def reply_group_chat():
    return chat.reply_group_chat(request)

@app.route('/reserve_list', methods=['POST'])
def reserve_list():
    return chat.reserve_list(request)

@app.route('/get_request_question', methods=['POST'])
def get_request_question():
    return chat.get_request_question(request)

@app.route('/my_question', methods=['POST'])
def my_question():
    return chat.my_question(request)

@app.route('/latest_new_question', methods=['POST'])
def latest_new_question():
    return chat.latest_new_question(request)

@app.route('/latest_question', methods=['POST'])
def latest_question():
    return chat.latest_question(request)

@app.route('/right_answer', methods=['POST'])
def right_answer():
    return chat.right_answer(request)

@app.route('/wrong_answer', methods=['POST'])
def wrong_answer():
    return chat.wrong_answer(request)

@app.route('/request_new_answer', methods=['POST'])
def request_new_answer():
    return chat.request_new_answer(request)

@app.route('/recommend_request', methods=['POST'])
def recommend_request():
    return chat.recommend_request(request)

@app.route('/get_schedule', methods=['POST'])
def get_schedule():
    return chat.get_schedule(request)

@app.route('/get_all_schedule', methods=['POST'])
def get_all_schedule():
    return chat.get_all_schedule(request)

@app.route('/send_file', methods=['POST'])
def send_file():
    return chat.send_file(request)

if (__name__ == "__main__"): 
    app.run(threaded=True, host=ip_addr, port = 5000) 
