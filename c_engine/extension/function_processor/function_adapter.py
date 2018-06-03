from c_engine.extension.function_processor import function_wrapper
from c_engine.extension.function_processor import function_caller

def get_param_and_replaced_msg(msg):    
    param, replacedMsg = function_caller.scan_param(msg)
    
    return param, replacedMsg

def get_message_by_function(param, message_count, this_yn):
    function_nm = param[0]['function_nm']
    if function_nm == '':
        return ['질문이 올바르지 않은것 같습니다.'], 1, '', 'N'
    msg = []
    temp = []
    for i in range(len(param)):
        message, tmp, continue_yn, param_holder = function_wrapper.wrap_function(function_nm, param[i], message_count, this_yn)
        msg.append(message)
        temp.append(tmp)
    if continue_yn == False:
        temp = ''
        
    return msg, str(temp), function_nm, str(param_holder)

def continue_dialogue(user_ip, question, param):
    param = eval(param)
    param[0]['user_ip'] = user_ip
    param[0]['question'] = question
    new_param, _ = get_param_and_replaced_msg(question)
    for k in param[0].keys():
        if param[0].get(k) == '' and new_param[0].get(k) != '':
            param[0][k] = new_param[0].get(k)
    
    return get_message_by_function(param, '', 'N')
    