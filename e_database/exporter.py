from e_database.sql_processor import select 

def get_question_builder(user, project):
    sql = "SELECT ANSWER_NUM, QUESTION_SRNO, QUESTION, QUESTION_TAG, QUESTION_VOCA FROM QUESTION_BUILDER_" + user + "_" + project
    result = select.fetch(sql)
    
    return result
    
def get_question_fragment_builder(user, project):
    sql = "SELECT ANSWER_NUM, QUESTION_SRNO, QUESTION, QUESTION_VOCA FROM QUESTION_FRAGMENT_BUILDER_" + user + "_" + project
    result = select.fetch(sql)
    
    return result

def get_compression_tag(user, project):
    sql = "SELECT COMPRESSION_NUM, EXPRESSION, TAG_NAME FROM COMPRESSION_TAG_" + user + "_" + project
    result = select.fetch(sql)
    
    return result
    
def get_answer_builder(user, project):
    sql = "SELECT ANSWER_NUM, ANSWER, CATEGORY_NUM, RPSN_QUESTION, IMAGE_CNT, RGSN_USER_IP, RQ_NUM, FRST_RGSN_DATE, MDFC_RGSN_DATE FROM ANSWER_BUILDER_" + user + "_" + project
    result = select.fetch(sql)
    
    return result

def get_dialogue_list():
    sql = "SELECT DIALOGUE_NUM, DIALOGUE_TEXT, ARGUMENT_NM, FUNCTION_NM FROM DIALOGUE_LIST"
    result = select.fetch(sql)
    
    return result

def get_user_info():
    sql = "SELECT USER_ID, PASSWORD FROM USER_INFO"
    result = select.fetch(sql)
    
    return result

def get_project_list():
    sql = "SELECT USER_ID, PROJECT FROM PROJECT_LIST"
    result = select.fetch(sql)
    
    return result

def get_synonym_list():
    sql = "SELECT SYNONYM_NUM, SYNONYM_NM, SYNONYM_TAG FROM SYNONYM_LIST"
    result = select.fetch(sql)
    
    return result

def get_category_list():
    sql = "SELECT CATEGORY_NUM, BIG_CATEGORY, MIDDLE_CATEGORY, SMALL_CATEGORY_LV1, SMALL_CATEGORY_LV2, SMALL_CATEGORY_LV3 FROM CATEGORY_LIST"
    result = select.fetch(sql)
    
    return result

def get_voca():
    sql = "SELECT VOCA_NM, VOCA_SYNONYM, KEYWORD_YN FROM VOCA"
    result = select.fetch(sql)
    
    return result

def get_tag_list():
    sql = "SELECT TAG_NUM, TAG_NM, KOR_NM, GUBUN FROM TAG_LIST"
    result = select.fetch(sql)
    
    return result

def get_question_and_answer_num(user, project):
    sql = "SELECT QUESTION, ANSWER_NUM FROM QUESTION_BUILDER_" + user + "_" + project
    result = select.fetch(sql)
    
    return result

def get_fragment_and_answer_num(user, project):
    sql = "SELECT QUESTION, ANSWER_NUM FROM QUESTION_FRAGMENT_BUILDER_" + user + "_" + project
    result = select.fetch(sql)
    
    return result

def get_answer_and_answer_num(user, project):
    sql = "SELECT ANSWER, ANSWER_NUM FROM ANSWER_BUILDER_" + user + "_" + project
    result = select.fetch(sql)
    
    return result

def get_expression_and_tag_name(user, project):
    sql = "SELECT EXPRESSION, TAG_NAME FROM COMPRESSION_TAG_" + user + "_" + project
    result = select.fetch(sql)
    
    return result

def get_question_list():
    sql = "SELECT QUESTION, ANSWER_NUM, RGSN_DATE, RGSN_TIME, USER_IP FROM QUESTION_LIST"
    result = select.fetch(sql)
    
    return result

def get_my_question():
    sql = "SELECT USER_IP, EMNO, QUESTION, RGSN_DATE FROM MY_QUESTION"
    result = select.fetch(sql)
    
    return result

def get_right_answer():
    sql = "SELECT QUESTION, ANSWER_NUM, RGSN_DATE, RGSN_DATE FROM RIGHT_ANSWER"
    result = select.fetch(sql)
    
    return result

def get_wrong_answer():
    sql = "SELECT QUESTION, ANSWER_NUM, RGSN_DATE, RGSN_DATE FROM WRONG_ANSWER"
    result = select.fetch(sql)
    
    return result

def get_schedule():
    sql = "SELECT USER_IP, MESSAGE, RESV_DATE, RESV_TIME FROM SCHEDULE"
    result = select.fetch(sql)
    
    return result

def get_training_config_list(user, project):
    sql = "SELECT CONFIG_NAME, CONFIG_VALUE FROM TRAINING_CONFIG_LIST_" + user + "_" + project
    result = select.fetch(sql)
    
    return result

def get_chatbot_config_list(user, project):
    sql = "SELECT CONFIG_NAME, CONFIG_VALUE FROM CHATBOT_CONFIG_LIST_" + user + "_" + project
    result = select.fetch(sql)
    
    return result

def get_vocab_dec():
    sql = "SELECT VOCA_NUM, VOCA_NM FROM VOCAB_DEC"
    result = select.fetch(sql)
    
    return result

def get_vocab_enc():
    sql = "SELECT VOCA_NUM, VOCA_NM FROM VOCAB_ENC"
    result = select.fetch(sql)
    
    return result
