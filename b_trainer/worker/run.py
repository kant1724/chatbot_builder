from b_trainer.file import training_file_creator as tfc
from b_trainer.worker import connect_tensorflow as ct

def init_chatbot(user, project):
    enc_vocab = tfc.initialize_vocabulary('enc')
    rev_dec_vocab = tfc.initialize_vocabulary('dec')
    ok = ct.init_chatbot(user, project)
    return enc_vocab, rev_dec_vocab

def run_chatbot(enc_vocab, rev_dec_vocab, sentence, collect_q, language):
    token_ids = tfc.sentence_to_token_ids(sentence, enc_vocab, language)
    reply = ct.run_chatbot(token_ids)
    answer_arr = eval(reply.get('reply', ''))
    if len(answer_arr) == 0:
        answer_arr.append(5)
    answer_num = rev_dec_vocab[answer_arr[0]]
    return answer_arr[0], answer_num

def get_token_ids(sentence, enc_vocab, language):
    return tfc.sentence_to_token_ids(sentence, enc_vocab, language)

def get_token_words(sentence):
    return tfc.char_tokenizer(sentence)

def is_chatbot_ready():
    res = ct.is_chatbot_ready()
    is_ready = res.get('is_ready')
    
    return is_ready
