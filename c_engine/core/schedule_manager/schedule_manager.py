from e_database import chat

def add_schedule(user_ip, msg, time):
    chat.insert_schedule(user_ip, msg, time)

def get_schedule(user_ip, time):
    return chat.select_schedule(user_ip, time)
