from e_database import importer

def create_all():
    importer.create_answer_builder_table('chatbot_tft', 'gcamp')
    importer.create_question_builder_table('chatbot_tft', 'gcamp')
    importer.create_question_fragment_builder_table('chatbot_tft', 'gcamp')
    importer.create_training_config_list_table('chatbot_tft', 'gcamp')
    importer.create_chatbot_config_list_table('chatbot_tft', 'gcamp')
