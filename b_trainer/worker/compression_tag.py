from b_trainer.file import training_file_creator as tfc
from b_trainer.worker import connect_tensorflow as ct

def init_compression_tag(user, project):
    enc_vocab = tfc.initialize_vocabulary('enc')
    rev_dec_vocab = tfc.initialize_vocabulary('dec')
    ok = ct.init_compression_tag(user, project)
    return enc_vocab, rev_dec_vocab

def run_compression_tag(enc_vocab, rev_dec_vocab, sentence, collect_q, language):
    token_ids = tfc.sentence_to_token_ids(sentence, enc_vocab, language)
    reply = ct.run_compression_tag(token_ids)
    answer_num = rev_dec_vocab[eval(reply.get('reply', ''))[0]]
    return answer_num

def is_running(user, project):
    res = ct.is_compression_tag_running(user, project)
    return res['is_running']
