from a_builder.importer import config_importer
from a_builder.importer import qna_importer
from a_builder.importer import voca_importer

def start():
    config_importer.chatbot_config_list_importer('chatbot_tft', 'test')
    config_importer.training_config_list_importer('chatbot_tft', 'test')
    
    qna_importer.answer_builder_importer('chatbot_tft', 'test')
    qna_importer.question_builder_importer('chatbot_tft', 'test')
    
    voca_importer.voca_importer()