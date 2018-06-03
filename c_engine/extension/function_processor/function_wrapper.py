from c_engine.core.util import util
from c_engine.extension.function_processor import continuous_dialogue
from c_engine.extension.function_processor import function_caller
from c_engine.extension.function_processor import connect_external_adapter

def wrap_function(function_nm, p, message_count, this_yn):
    func_len = len(function_nm)
    time, date_from, date_to, question = p.get('time'), p.get('date_from', ''), p.get('date_to', ''), p.get('question', '')
    dialogue_text = continuous_dialogue.check_argument(function_nm, {'time': time, 'date_from': date_from, 'date_to': date_to, 'question' : question})
    if util.isNull(dialogue_text) == False:
        return dialogue_text, p, True, p
    if function_nm[0:3] == 'ext':
        message = connect_external_adapter.send_function_and_param(function_nm, p, message_count, this_yn).get('message', '')
    else:
        function = 'function_caller.' + function_nm[:func_len - 1] + 'p' + function_nm[func_len - 1:]
        message = eval(function)    
    
    return message, '', False, p
