from c_engine.core.util import util
from c_engine.core.util import time_util
from e_database import chat
from c_engine.extension.function_processor import excel_exporter
from c_engine.extension.function_processor import tag_manager

def set_my_schedule(p):
    user_ip, question, time = p.get('user_ip'), p.get('question'), p.get('time')    
    hour = ''
    minute = ''
    for t in time:
        if t[0] == '시':
            hour = t[1]
        elif t[0] == '분':
            minute = t[1]
    if hour == '':
        return '잘못된 입력입니다. 다시 시도해 주세요. 시간 + 내용 ex) 15시30분 팀원들과 티타임'
    if minute == '':
        minute = '00'
    time = hour + minute
    chat.insert_schedule(user_ip, question, time)
    if time_util.is_time(time) == False:
        return '잘못된 입력입니다. 다시 시도해 주세요. 시간 + 내용 ex) 15시30분 팀원들과 티타임'
    kor_time = hour + "시" + minute + "분"
    msg = '일정이 등록되었습니다.<br>'
    msg += question + '<br>'
    msg += '예약시간: ' + kor_time + '<br>'
    msg += '예약시간에 알림 메세지 보내겠습니다.'
    
    return msg

def insert_my_frequent_question(p):
    user_ip, question = p.get('user_ip'), p.get('question')    
    chat.insert_my_frequent_question(user_ip, question)
    
    return '자주하는 질문으로 등록되었습니다.'

def scan_param(msg):
    param = []
    t = {"time" : '', "date_from" : '', "date_to" : '', "acct_no" : '', "rnn" : '', "cust_no" : ''}
    param.append(t)
    msg = msg.replace(" ", "").replace("-", "")
    has, acct_no, replacedMsg = tag_manager.is_acct_no(msg)
    if has:
        t["acct_no"] = acct_no
    has, cust_no, replacedMsg = tag_manager.is_cust_no(replacedMsg)
    if has:
        t["cust_no"] = cust_no
    has, cust_no, replacedMsg = tag_manager.is_cust_no2(replacedMsg)
    if has:
        t["cust_no"] = cust_no
    has, rnn, replacedMsg = tag_manager.is_rnn(replacedMsg)
    if has:
        t["rnn"] = rnn
    has, date_from, date_to, replacedMsg = tag_manager.is_date_from_to(replacedMsg)
    if has:
        t["date_from"] = date_from
        t["date_to"] = date_to
    has, time, replacedMsg = tag_manager.is_time(replacedMsg)
    if has:
        t["time"] = time
    
    return param, replacedMsg
