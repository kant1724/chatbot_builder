import os
import zipfile
import glob
from a_builder.exporter import collector_exporter
from a_builder.exporter import config_exporter
from a_builder.exporter import login_info_exporter
from a_builder.exporter import qna_exporter
from a_builder.exporter import schedule_exporter
from a_builder.exporter import synonym_and_voca_exporter
from a_builder.exporter import trainer_exporter

def start():
    collector_exporter.my_question_exporter()
    collector_exporter.question_list_exporter()
    collector_exporter.right_answer_exporter()
    collector_exporter.wrong_answer_exporter()
    
    config_exporter.training_config_list_exporter('chatbot_tft', 'fund')
    config_exporter.training_config_list_exporter('chatbot_tft', 'test')    
    
    config_exporter.chatbot_config_list_exporter('chatbot_tft', 'fund')    
    config_exporter.chatbot_config_list_exporter('chatbot_tft', 'test')
    
    login_info_exporter.project_list_exporter()
    login_info_exporter.user_info_exporter()
    
    qna_exporter.answer_builder_exporter('chatbot_tft', 'fund')
    qna_exporter.answer_builder_exporter('chatbot_tft', 'test')
    qna_exporter.question_builder_exporter('chatbot_tft', 'fund')
    qna_exporter.question_builder_exporter('chatbot_tft', 'test')
    qna_exporter.question_fragment_builder_exporter('chatbot_tft', 'fund')
    qna_exporter.question_fragment_builder_exporter('chatbot_tft', 'test')    
    qna_exporter.dialogue_list_exporter()
    
    qna_exporter.compression_tag_exporter('chatbot_tft', 'fund')
    
    
    schedule_exporter.schedule_exporter()
    
    synonym_and_voca_exporter.category_list_exporter()
    synonym_and_voca_exporter.synonym_list_exporter()
    synonym_and_voca_exporter.tag_list()
    synonym_and_voca_exporter.voca_exporter()
    
    trainer_exporter.vocab_dec_exporter()
    trainer_exporter.vocab_enc_exporter()
    
    zipf = zipfile.ZipFile('./export_data.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk('./a_builder/exporter/data/'):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()
    filelist = glob.glob('./a_builder/exporter/data/*')
    for file in filelist:
        os.remove(file)
    