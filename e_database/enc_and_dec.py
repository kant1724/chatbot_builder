from e_database.sql_processor import select
from e_database.sql_processor import update

def insert_vocab(voca_nm, t):
    table = ''
    if t == 'enc':
        table = 'VOCAB_ENC'
    elif t == 'dec':
        table = 'VOCAB_DEC'
    sql = "SELECT MAX(VOCA_NUM) + 1 FROM " + table
    result = select.fetch(sql)
    voca_num = result[0][0]
    if voca_num == None:
        voca_num = 1
    sql = "INSERT INTO " + table + " VALUES (" + str(voca_num) + ", '" + voca_nm + "')"
    update.commit(sql)

def select_vocab(voca_nm, t):
    table = ''
    if t == 'enc':
        table = 'VOCAB_ENC'
    elif t == 'dec':
        table = 'VOCAB_DEC'
    sql = "SELECT VOCA_NM FROM " + table + " WHERE VOCA_NM = '" + voca_nm + "'"
    result = select.fetch(sql)
    if len(result) > 0:
        voca_nm = result[0][0]
    else:
        voca_nm = None

    return voca_nm

def select_all_vocab_nm(flag):
    table = ''
    if flag == 'enc':
        table = 'VOCAB_ENC'
    elif flag == 'dec':
        table = 'VOCAB_DEC'
    sql = "SELECT VOCA_NM FROM " + table
    result = select.fetch(sql)
    all_vocab = []
    for r in result:
        all_vocab.append(r[0])

    return all_vocab

def select_all_vocab_num_nm(flag):
    table = ''
    if flag == 'enc':
        table = 'VOCAB_ENC'
    elif flag == 'dec':
        table = 'VOCAB_DEC'
    sql = "SELECT VOCA_NUM, VOCA_NM FROM " + table
    result = select.fetch(sql)
    all_vocab = {}
    for r in result:
        if flag == 'enc':
            all_vocab[r[1]] = r[0]
        else:
            all_vocab[r[0]] = r[1]

    return all_vocab
