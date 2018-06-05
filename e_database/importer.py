from e_database.sql_processor import update

def create_question_builder_table(user, project):
    sql = "CREATE TABLE QUESTION_BUILDER_" + user + "_" + project + " (ANSWER_NUM VARCHAR(10), QUESTION_SRNO INT(7), QUESTION VARCHAR(500), QUESTION_TAG VARCHAR(500), QUESTION_VOCA VARCHAR(500))"
    try:
        update.commit(sql)
    except:
        print("QUESTION_QUESTION_BUILDER table already exists")
        
def create_question_fragment_builder_table(user, project):
    sql = "CREATE TABLE QUESTION_FRAGMENT_BUILDER_" + user + "_" + project + " (ANSWER_NUM VARCHAR(500), QUESTION_SRNO INT(7), QUESTION VARCHAR(500), QUESTION_VOCA VARCHAR(500))"
    try:
        update.commit(sql)
    except:
        print("QUESTION_FRAGMENT_BUILDER table already exists")

def create_answer_builder_table(user, project):
    sql = "CREATE TABLE ANSWER_BUILDER_" + user + "_" + project + " (ANSWER_NUM VARCHAR(10), ANSWER VARCHAR(500), CATEGORY_NUM VARCHAR(7), RPSN_QUESTION VARCHAR(500), IMAGE_CNT INT(3), RGSN_USER_IP VARCHAR(20), RQ_NUM INT(10), FRST_RGSN_DATE VARCHAR(20), MDFC_RGSN_DATE VARCHAR(20))"
    try:
        update.commit(sql)
    except:
        print("ANSWER_BUILDER table already exists")

def create_compression_tag_table(user, project):
    sql = "CREATE TABLE COMPRESSION_TAG_" + user + "_" + project + " (COMPRESSION_NUM INT(10), EXPRESSION VARCHAR(500), TAG_NAME VARCHAR(500))" 
    try:
        update.commit(sql)
    except:
        print("COMPRESSION_TAG table already exists")
    
def create_category_list_table():
    sql = "CREATE TABLE CATEGORY_LIST (CATEGORY_NUM INT(7), BIG_CATEGORY VARCHAR(50), MIDDLE_CATEGORY VARCHAR(50), SMALL_CATEGORY_LV1 VARCHAR(50), SMALL_CATEGORY_LV2 VARCHAR(50), SMALL_CATEGORY_LV3 VARCHAR(50))"
    try:
        update.commit(sql)
    except:
        print("CATEGORY_LIST table already exists")
    
def create_dialogue_list_table():
    sql = "CREATE TABLE DIALOGUE_LIST (DIALOGUE_NUM INT(7), DIALOGUE_TEXT VARCHAR(1000), ARGUMENT_NM VARCHAR(50), FUNCTION_NM VARCHAR(100))"
    try:
        update.commit(sql)
    except:
        print("DIALOGUE_LIST table already exists")
    
def create_my_question_table():
    sql = "CREATE TABLE MY_QUESTION (USER_IP VARCHAR(20), EMNO VARCHAR(10), QUESTION VARCHAR(500), RGSN_DATE VARCHAR(10))"
    try:
        update.commit(sql)
    except:
        print("MY_QUESTION table already exists")

def create_project_list_table():
    sql = "CREATE TABLE PROJECT_LIST (USER_ID VARCHAR(50), PROJECT VARCHAR(50), LANGUAGE VARCHAR(20))"
    try:
        update.commit(sql)
    except:
        print("PROJECT_LIST table already exists")
    
def create_question_list_table():
    sql = "CREATE TABLE QUESTION_LIST (QUESTION VARCHAR(500), ANSWER_NUM VARCHAR(10), RGSN_DATE VARCHAR(20), RGSN_TIME VARCHAR(10), USER_IP VARCHAR(20))"
    try:
        update.commit(sql)
    except:
        print("QUESTION_LIST table already exists")
    
def create_request_question_table(user, project):
    sql = "CREATE TABLE REQUEST_QUESTION_" + user + "_" + project + " (RQ_NUM INT(10), USER_IP VARCHAR(20), QUESTION VARCHAR(500), RGSN_DATE VARCHAR(20), RGSN_TIME VARCHAR(10), RECOMMEND_CNT INT(7), PC_STATUS VARCHAR(2))"
    try:
        update.commit(sql)
    except:
        print("REQUEST_QUESTION table already exists")
    
def create_right_answer_table():
    sql = "CREATE TABLE RIGHT_ANSWER (QUESTION VARCHAR(500), ANSWER_NUM VARCHAR(10), RGSN_DATE VARCHAR(20), RGSN_TIME VARCHAR(10))"
    try:
        update.commit(sql)
    except:
        print("RIGHT_ANSWER table already exists")

def create_schedule_table():
    sql = "CREATE TABLE SCHEDULE (USER_IP VARCHAR(20), MESSAGE VARCHAR(500), RESV_DATE VARCHAR(20), RESV_TIME VARCHAR(10))"
    try:
        update.commit(sql)
    except:
        print("SCHEDULE table already exists")

def create_synonym_list_table():
    sql = "CREATE TABLE SYNONYM_LIST (SYNONYM_NUM INT(7), SYNONYM_NM VARCHAR(50), SYNONYM_TAG VARCHAR(50))"
    try:
        update.commit(sql)
    except:
        print("SYNONYM_LIST table already exists")
    
def create_tag_list_table():
    sql = "CREATE TABLE TAG_LIST (TAG_NUM INT(7), TAG_NM VARCHAR(50), KOR_NM VARCHAR(50), GUBUN VARCHAR(10))"
    try:
        update.commit(sql)
    except:
        print("TAG_LIST table already exists")
    
def create_training_config_list_table(user, project):
    sql = "CREATE TABLE TRAINING_CONFIG_LIST_" + user + "_" + project + " (CONFIG_NAME VARCHAR(500), CONFIG_VALUE VARCHAR(500))"
    try:
        update.commit(sql)
    except:
        print("TRAINING_CONFIG_LIST table already exists")

def create_chatbot_config_list_table(user, project):
    sql = "CREATE TABLE CHATBOT_CONFIG_LIST_" + user + "_" + project + " (CONFIG_NAME VARCHAR(500), CONFIG_VALUE VARCHAR(500))"
    try:
        update.commit(sql)
    except:
        print("CHATBOT_CONFIG_LIST table already exists")

def create_user_info_table():
    sql = "CREATE TABLE USER_INFO (USER_ID VARCHAR(50), PASSWORD VARCHAR(50))"
    try:
        update.commit(sql)
    except:
        print("USER_INFO table already exists")

def create_voca_table():
    sql = "CREATE TABLE VOCA (VOCA_NM VARCHAR(50), VOCA_SYNONYM VARCHAR(500), KEYWORD_YN VARCHAR(2))"
    try:
        update.commit(sql)
    except:
        print("VOCA table already exists")

def create_vocab_dec_table():
    sql = "CREATE TABLE VOCAB_DEC (VOCA_NUM INT(10), VOCA_NM VARCHAR(500))"
    try:
        update.commit(sql)
    except:
        print("VOCAB_DEC table already exists")

def create_vocab_enc_table():
    sql = "CREATE TABLE VOCAB_ENC (VOCA_NUM INT(10), VOCA_NM VARCHAR(50))"
    try:
        update.commit(sql)
    except:
        print("VOCAB_ENC table already exists")

def create_vocab_tag_table():
    sql = "CREATE TABLE VOCAB_TAG (VOCA_NUM INT(10), VOCA_NM VARCHAR(50))"
    try:
        update.commit(sql)
    except:
        print("VOCAB_TAG table already exists")
    
def create_wrong_answer_table():
    sql = "CREATE TABLE WRONG_ANSWER (QUESTION VARCHAR(500), ANSWER_NUM VARCHAR(10), RGSN_DATE VARCHAR(20), RGSN_TIME VARCHAR(10))"
    try:
        update.commit(sql)
    except:
        print("WRONG_ANSWER table already exists")

def create_notice_list_table(user, project):
    sql = "CREATE TABLE NOTICE_LIST_CHATBOT_" + user + "_" + project + " (NOTICE_NUM INT(7), NOTICE_SUBJECT VARCHAR(500), NOTICE_CONTENT VARCHAR(5000), IMAGE_CNT INT(3), RGSN_DATE VARCHAR(20), NOTICE_START_DATE VARCHAR(20), NOTICE_END_DATE VARCHAR(20), COMPLETE_YN VARCHAR(1))"
    try:
        update.commit(sql)
    except:
        print("NOTICE_LIST table already exists")

def import_question_builder(user, project, arr):
    sql = "INSERT INTO QUESTION_BUILDER_" + user + "_" + project + " VALUES ('" + arr[0] + "', '" + arr[1] + "', '" + arr[2] + "', '" + arr[3] + "', '" + arr[4] + "')"
    update.commit(sql)
    
def import_answer_builder(user, project, arr):
    sql = "INSERT INTO ANSWER_BUILDER_" + user + "_" + project + " VALUES ('" + arr[0] + "', '" + arr[1] + "', '" + arr[2] + "', '" + arr[3] + "', " + arr[4] + ", '" + arr[5] + "', " + arr[6] + ", '" +  arr[7] + "', '" +  arr[8] + "')"
    update.commit(sql)

def import_compression_tag(user, project, arr):
    sql = "INSERT INTO COMPRESSION_TAG_" + user + "_" + project + " VALUES ('" + arr[0] + "', '" + arr[1] + "', '" + arr[2] + "')"
    update.commit(sql)

def import_training_config_list(user, project, arr):
    sql = "INSERT INTO TRAINING_CONFIG_LIST_" + user + "_" + project + " VALUES ('" + arr[0] + "', '" + arr[1] + "')"
    update.commit(sql)
    
def import_chatbot_config_list(user, project, arr):
    sql = "INSERT INTO CHATBOT_CONFIG_LIST_" + user + "_" + project + " VALUES ('" + arr[0] + "', '" + arr[1] + "')"
    update.commit(sql)

def import_voca(arr):
    sql = "INSERT INTO VOCA VALUES ('" + arr[0] + "', '" + arr[1] + "', '" + arr[2] + "')"
    update.commit(sql)
