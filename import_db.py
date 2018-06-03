from a_builder.importer import execute_all
from a_builder.importer import qna_importer
from a_builder.importer import voca_importer

qna_importer.answer_builder_importer('chatbot_tft', 'fund')
qna_importer.question_builder_importer('chatbot_tft', 'fund')
voca_importer.voca_importer()
