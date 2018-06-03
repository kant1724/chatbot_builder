def get_function_by_question(question):
    if question == '내 일정':
        return '$CALL set_my_schedule()'
    elif question == '자주하는질문':
        return '$CALL insert_my_frequent_question()'
    
    return '' 

def is_fixed_question(question):
    if question == '내 일정':
        return True
    elif question == '자주하는질문':
        return True
    
    return False
