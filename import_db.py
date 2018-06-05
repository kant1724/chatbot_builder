from a_builder.importer import execute_all
from a_builder.importer import qna_importer
from a_builder.importer import config_importer
from a_builder.importer import voca_importer
from a_builder.importer import create_all_tables

qna_importer.compression_tag_importer('chatbot_tft', 'fund')
