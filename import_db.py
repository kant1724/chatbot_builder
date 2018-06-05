from a_builder.importer import execute_all
from a_builder.importer import qna_importer
from a_builder.importer import config_importer
from a_builder.importer import voca_importer
from a_builder.importer import create_all_tables

config_importer.training_config_list_importer('chatbot_tft', 'fund')
config_importer.chatbot_config_list_importer('chatbot_tft', 'fund')
