from c_engine.core.util import util
from e_database import chat

def check_argument(function_nm, argument_dict):
    dialogue_text = ''
    for argument_key in argument_dict.keys():
        if util.isNull(argument_dict.get(argument_key)):
            dialogue_text = chat.get_dialogue_list_by_function_nm_and_argument_nm(function_nm, argument_key)
            if util.isNull(dialogue_text) == False:
                break
    return dialogue_text
