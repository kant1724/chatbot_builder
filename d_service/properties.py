with open('./server_ip', encoding="utf8") as f:
    lines = f.readlines()
    BUILDER_IP = lines[0].split("=")[1].replace('\n', '')
    TF_IP = lines[1].split("=")[1].replace('\n', '')
    TF_COMPRESSION_TAG_IP = lines[2].split("=")[1].replace('\n', '')
    FILE_IP = lines[3].split("=")[1].replace('\n', '')
    DB_HOST_IP = lines[4].split("=")[1].replace('\n', '')
    GROUP_CHAT_IP = lines[5].split("=")[1].replace('\n', '')
    EXTERNAL_ADAPTER_IP = lines[6].split("=")[1].replace('\n', '')
    
IMAGE_FILE_ROOT_PATH = '/static/data/images/user/' 
    
def get_builder_ip():
    return BUILDER_IP

def get_tf_ip():
    return TF_IP

def get_tf_compression_tag_ip():
    return TF_COMPRESSION_TAG_IP

def get_file_ip():
    return FILE_IP

def get_external_adapter_ip():
    return EXTERNAL_ADAPTER_IP

def get_db_host_ip():
    return DB_HOST_IP

def get_group_chat_ip():
    return GROUP_CHAT_IP

def get_image_file_root_path():
    return IMAGE_FILE_ROOT_PATH
