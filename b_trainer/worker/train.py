import os
from b_trainer.file import training_file_creator as tfc
from b_trainer.worker import connect_tensorflow as ct
from e_database import training_config as db_training_config

enc_vocab_size = 1000
dec_vocab_size = 1000
language = 'kor'
enc_vocab = None
rev_dec_vocab = None

def train(user, project, saving_step):
    global language, enc_vocab, rev_dec_vocab
    saving_step = int(saving_step)        
    language = db_training_config.get_project_language(user, project)
    tfc.convert_and_replace(user, project)
    enc_vocab = tfc.initialize_vocabulary('enc')
    rev_dec_vocab = tfc.initialize_vocabulary('dec')
    train_enc_ids, train_dec_ids = tfc.prepare_custom_data(user, project, enc_vocab_size, dec_vocab_size, language)
    ct.start_training(user, project, saving_step, train_enc_ids, train_dec_ids)

def stop(user, project):
    ct.stop_training(user, project)

def get_training_info(user, project):
    res = ct.get_training_info(user, project)
    return res['training_info'], res['saving_step']
    
def is_training(user, project):
    res = ct.is_training(user, project)
    return res['is_training']

def delete_ckpt(user, project):
    ct.delete_ckpt(user, project)

def send_training_test_question(user, project, question):
    global enc_vocab, rev_dec_vocab
    if enc_vocab == None:
        enc_vocab = tfc.initialize_vocabulary('enc')
    if rev_dec_vocab == None:
        rev_dec_vocab = tfc.initialize_vocabulary('dec')
    token_ids = tfc.sentence_to_token_ids(question, enc_vocab, language)
    reply = ct.send_training_test_question(user, project, token_ids)
    answer_arr = eval(reply.get('reply', ''))
    if len(answer_arr) == 0:
        answer_arr.append(5)
    answer_num = rev_dec_vocab[answer_arr[0]]
    
    return answer_num
    
def compression_tag_train(user, project, saving_step):
    saving_step = int(saving_step)        
    language = 'kor'
    tfc.compression_tag_convert_and_replace(user, project)
    train_enc_ids, train_dec_ids = tfc.compression_tag_prepare_custom_data(user, project, enc_vocab_size, dec_vocab_size, language)
    ct.start_compression_tag_training(user, project, saving_step, train_enc_ids, train_dec_ids)

def compression_tag_stop(user, project):
    ct.stop_compression_tag_training(user, project)

def get_compression_tag_training_info(user, project):
    res = ct.get_compression_tag_training_info(user, project)
    return res['training_info'], res['saving_step']
    
def is_compression_tag_training(user, project):
    res = ct.is_compression_tag_training(user, project)
    return res['is_training']

def delete_compression_tag_ckpt(user, project):
    ct.delete_compression_tag_ckpt(user, project)
    