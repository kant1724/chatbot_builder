import re
from b_trainer.worker import connect_file
from e_database import enc_and_dec
from e_database import exporter

_PAD = "_PAD"
_GO = "_GO"
_EOS = "_EOS"
_UNK = "_UNK"
_START_VOCAB = [_PAD, _GO, _EOS, _UNK]

PAD_ID = 0
GO_ID = 1
EOS_ID = 2
UNK_ID = 3

_WORD_SPLIT = re.compile(b"([.,!?\"':;)(])")
_DIGIT_RE = re.compile(br"\d")

exception = ['?', ' ', '.', '"', ','] 

def representsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def char_tokenizer(sentence):
    words = []
    i = 0
    while i < len(sentence):
        if representsInt(sentence[i]):
            num = ""
            while i < len(sentence) and representsInt(sentence[i]):
                num += str(sentence[i])
                i += 1
            words.append(num.replace('\n', ''))
        else:
            if sentence[i] in exception:
                i += 1
                continue
            words.append(sentence[i].replace('\n', ''))
            i += 1
    return words

def word_tokenizer(sentence):
    return sentence.replace("\n", "").split(" ")

def create_vocabulary(train_arr, max_vocabulary_size, flag, language):
    vocab = {}
    for line in train_arr:
        if flag == 'enc':
            if language == 'eng':
                tokens = word_tokenizer(line)
            elif language == 'kor':
                tokens = char_tokenizer(line)
        else:
            tokens = line.replace('\n', '').split(" ")
        for word in tokens:
            if word in vocab:
                vocab[word] += 1
            else:
                vocab[word] = 1
        vocab_list = _START_VOCAB + sorted(vocab, key=vocab.get, reverse=True)
        if len(vocab_list) > max_vocabulary_size:
            vocab_list = vocab_list[:max_vocabulary_size]

    all_vocab = enc_and_dec.select_all_vocab_nm(flag)
    for w in vocab_list:
        if w not in all_vocab:
            enc_and_dec.insert_vocab(w, flag)
                
def initialize_vocabulary(flag):
    return enc_and_dec.select_all_vocab_num_nm(flag)

def sentence_to_token_ids(sentence, vocabulary, language):
    if language == 'eng':
        words = word_tokenizer(sentence)
    elif language == 'kor':
        words = char_tokenizer(sentence)
    
    return [str(vocabulary.get(w, UNK_ID)) for w in words]

def data_to_token_ids(train_arr, flag, language):
    vocab = initialize_vocabulary(flag)
    rev_vocab = {}
    token_arr = []
    for k, v in vocab.items():
        rev_vocab[v] = k
    for line in train_arr:
        if flag == 'enc':
            token_ids = sentence_to_token_ids(line, vocab, language)
            token_arr.append(" ".join(token_ids))
        else:
            ll = line.replace('\n', '').split(" ")
            token_ids = []
            for l in ll:
                token_ids.append(str(rev_vocab[l]))
            token_arr.append(" ".join(token_ids))
    return token_arr
    
def prepare_custom_data(user, project, enc_vocabulary_size, dec_vocabulary_size, language):
    res = connect_file.get_training_data(user, project)
    train_enc = eval(res['train_enc'])
    train_dec = eval(res['train_dec'])
    
    create_vocabulary(train_enc, enc_vocabulary_size, 'enc', language)
    create_vocabulary(train_dec, dec_vocabulary_size, 'dec', language)

    train_enc_ids = data_to_token_ids(train_enc, 'enc', language)
    train_dec_ids = data_to_token_ids(train_dec, 'dec', language)

    return train_enc_ids, train_dec_ids

def convert_and_replace(user, project):
    question_and_answer_num = exporter.get_question_and_answer_num(user, project)
    fragment_and_answer_num = exporter.get_fragment_and_answer_num(user, project)
    answer_dict = exporter.get_answer_and_answer_num(user, project)
    
    connect_file.send_training_data(user, project, str(answer_dict), str(question_and_answer_num), str(fragment_and_answer_num))

def compression_tag_prepare_custom_data(user, project, enc_vocabulary_size, dec_vocabulary_size, language):
    res = connect_file.get_compression_tag_training_data(user, project)
    train_enc = eval(res['train_enc'])
    train_dec = eval(res['train_dec'])
    
    create_vocabulary(train_enc, enc_vocabulary_size, 'enc', language)
    create_vocabulary(train_dec, dec_vocabulary_size, 'dec', language)

    train_enc_ids = data_to_token_ids(train_enc, 'enc', language)
    train_dec_ids = data_to_token_ids(train_dec, 'dec', language)

    return train_enc_ids, train_dec_ids

def compression_tag_convert_and_replace(user, project):
    expression_and_tag_name = exporter.get_expression_and_tag_name(user, project)
    
    connect_file.send_compression_tag_training_data(user, project, str(expression_and_tag_name))
    