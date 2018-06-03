from e_database import chat
from c_engine.core.util import util
from c_engine.core.util import date_util
from c_engine.core.util import time_util
import calendar
from datetime import date
vendor_arr = []

def is_brnc(msg):
    brnc_nm_list = chat.get_all_brnc_nm_list()
    kor_nm = chat.get_kor_nm_by_tag_nm('@where:brnc')
    for i in range(len(msg)):
        j = i
        while j <= len(msg):
            if msg[i : j] in brnc_nm_list:
                replacedMsg = msg.replace(msg[i : j], kor_nm)
                return True, msg[i : j], replacedMsg.strip()
                break
            j += 1
    return False, [''], msg

def is_vendor(msg):
    kor_nm = chat.get_kor_nm_by_tag_nm('@where:vendor')
    for i in range(len(msg)):
        j = i
        while j <= len(msg):
            if msg[i : j] in vendor_arr:
                replacedMsg = msg.replace(msg[i : j], kor_nm)
                return True, msg[i : j], replacedMsg.strip()
                break
            j += 1
    return False, [''], msg

def is_cust_no(msg):
    i = 0
    cust_no = ''
    has = False
    while i < len(msg) - 8:
        s = msg[i : i + 8]
        if util.represents_int(s):
            if i < len(msg) - 9:
                if util.represents_int(msg[i + 8]) == True:
                    i += 1
                    continue
            if i > 0:
                if util.represents_int(msg[i - 1]) == True:
                    i += 1
                    continue
            msg = msg.replace(s, "@what:cust_no")
            has = True
            return has, s, msg
        i += 1
    return has, cust_no, msg

def is_cust_no2(msg):
    i = 0
    cust_no = ''
    has = False
    while i < len(msg) - 7:
        s = msg[i : i + 7]
        if util.represents_int(s):
            if i < len(msg) - 8:
                if util.represents_int(msg[i + 7]) == True:
                    i += 1
                    continue
            if i > 0:
                if util.represents_int(msg[i - 1]) == True:
                    i += 1
                    continue
            msg = msg.replace(s, "@what:cust_no")
            has = True
            return has, s, msg
        i += 1
    return has, cust_no, msg

def is_acct_no(msg):
    i = 0
    cust_no = ''
    has = False
    while i < len(msg) - 14:
        s = msg[i : i + 14]
        if util.represents_int(s):
            if i < len(msg) - 15:
                if util.represents_int(msg[i + 14]) == True:
                    i += 1
                    continue
            if i > 0:
                if util.represents_int(msg[i - 1]) == True:
                    i += 1
                    continue
            msg = msg.replace(s, "@what:acct_no")
            has = True
            return has, s, msg
        i += 1
    return has, cust_no, msg

def is_rnn(msg):
    logic = [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5]
    number = 0
    i = 0
    rnn = ''
    has = False
    while i < len(msg) - 13:
        s = msg[i : i + 13]
        if util.represents_int(s):
            for j in range(0, len(logic)):
                number += int(s[j]) * int(logic[j])
                if 11 - (number % 11) == int(s[12]):
                    msg = msg.replace(s, "@what:rnn")
                    has = True
                    return has, s, msg
        i += 1
    
    return has, rnn, msg

def is_date_from_to(msg):
    today = date.today()
    msg = date_util.scan_and_replace_date(msg)
    date_to = {}
    date_from = {}
    msg_arr = []
    has = False
    for i in range(len(msg)):
        msg_arr.append(msg[i])
    already_1 = False
    already_2 = False
    already_3 = False
    for i in range(len(msg_arr)):
        cur = len(msg_arr) - i - 1
        word = msg_arr[cur]
        if word == '일' or word == '월' or word == '년':
            has = True
            cur -= 1
            d = ''
            index = []
            while util.represents_int(msg_arr[cur]):
                d = str(msg_arr[cur]) + d
                index.append(cur)
                cur -= 1
            if d == '':
                continue
            if word == '일':
                if int(d) > 31 or int(d) < 0:
                    continue
                for i in range(len(index)):
                    if already_1:
                        msg_arr[index[i]] = '#'
                    else:
                        msg_arr[index[i]] = '$'
                d = util.lpad(d, 2, '0')
                if already_1:
                    date_from['일'] = d
                    already_2 = True
                    already_3 = True
                else:
                    date_to['일'] = d
                    already_1 = True
            elif word == '월':
                if int(d) > 12 or int(d) < 0:
                    continue
                for i in range(len(index)):
                    if already_2:
                        msg_arr[index[i]] = '#'
                    else:
                        msg_arr[index[i]] = '$'
                d = util.lpad(d, 2, '0')
                if already_2:
                    date_from['월'] = d
                    already_3 = True
                else:
                    date_to['월'] = d
                    already_1 = True
                    already_2 = True
            elif word == '년':
                if int(d) > 9999 or int(d) < 0:
                    continue
                for i in range(len(index)):
                    if already_3:
                        msg_arr[index[i]] = '#'
                    else:
                        msg_arr[index[i]] = '$'
                if len(d) == 2:
                    d = '20' + d
                d = util.lpad(d, 4, '0')
                if already_3:
                    date_from['년'] = d
                else:
                    date_to['년'] = d
                    already_1 = True
                    already_2 = True
                    already_3 = True
    replacedMsg = ''
    for m in msg_arr:
        replacedMsg += m
    date_to['년'] = date_to.get('년', str(today.year))
    date_to['월'] = date_to.get('월', '12')
    date_to['일'] = date_to.get('일', str(calendar.monthrange(int(date_to['년']), int(date_to['월']))[1]))
    
    date_from['년'] = date_from.get('년', str(today.year))
    date_from['월'] = date_from.get('월', '01')
    date_from['일'] = date_from.get('일', '01')
    
    f_s = -1
    f_e = -1
    t_s = -1
    t_e = -1
    for i in range(len(replacedMsg)):
        if replacedMsg[i] == '#':
            if f_s == -1:
                f_s = i
            else:
                f_e = i
        if replacedMsg[i] == '$':
            if t_s == -1:
                t_s = i
            else:
                t_e = i
    f_e += 1
    t_e += 1
    while f_e < len(replacedMsg):
        if replacedMsg[f_e] in ['년', '월', '일']:
            f_e += 1
        else:
            break
    while t_e < len(replacedMsg):
        if replacedMsg[t_e] in ['년', '월', '일']:
            t_e += 1
        else:
            break
    if f_s != -1 and f_e != -1 and t_s != -1 and t_e != -1:
        kor_nm = chat.get_kor_nm_by_tag_nm('@where:ymd')
        replacedMsg = replacedMsg.replace(replacedMsg[f_s:f_e], kor_nm).replace(replacedMsg[t_s:t_e], kor_nm)

    return has, date_from, date_to, replacedMsg

def is_time(msg):
    msg = time_util.scan_and_replace_time(msg)
    time = []
    msg_arr = []
    has = False
    for i in range(len(msg)):
        msg_arr.append(msg[i])
    for i in range(len(msg_arr)):
        cur = len(msg_arr) - i - 1
        word = msg_arr[cur]
        if word == '시' or word == '분' or word == '초':
            has = True
            cur -= 1
            d = ''
            index = []
            while util.represents_int(msg_arr[cur]):
                d = str(msg_arr[cur]) + d
                index.append(cur)
                cur -= 1
            if d == '':
                continue
            if word == '초':
                if int(d) > 60 or int(d) < 0:
                    continue
                for i in range(len(index)):
                    msg_arr[index[i]] = ''
                d = util.lpad(d, 2, '0')
                time.append(['초', d])
            elif word == '분':
                if int(d) > 60 or int(d) < 0:
                    continue
                for i in range(len(index)):
                    msg_arr[index[i]] = ''
                d = util.lpad(d, 2, '0')                
                time.append(['분', d])
            elif word == '시':
                if int(d) > 24 or int(d) < 0:
                    continue
                for i in range(len(index)):
                    msg_arr[index[i]] = ''
                d = util.lpad(d, 2, '0')
                time.append(['시', d])
    replacedMsg = ''
    for m in msg_arr:
        replacedMsg += m
    kor_nm = chat.get_kor_nm_by_tag_nm('@where:time')
    replacedMsg = replacedMsg.replace('시분초', kor_nm)
    
    return has, time, replacedMsg

def is_time_from_to(msg):
    msg = time_util.scan_and_replace_time(msg)
    time_to = []
    time_from = []
    msg_arr = []
    has = False
    for i in range(len(msg)):
        msg_arr.append(msg[i])
    already_1 = False
    already_2 = False
    already_3 = False
    for i in range(len(msg_arr)):
        cur = len(msg_arr) - i - 1
        word = msg_arr[cur]
        if word == '시' or word == '분' or word == '초':
            has = True
            cur -= 1
            d = ''
            index = []
            while util.represents_int(msg_arr[cur]):
                d = str(msg_arr[cur]) + d
                index.append(cur)
                cur -= 1
            if d == '':
                continue
            if word == '초':
                if int(d) > 60 or int(d) < 0:
                    continue
                for i in range(len(index)):
                    msg_arr[index[i]] = ''
                d = util.lpad(d, 2, '0')
                if already_1:
                    time_from.append(['초', d])
                    already_2 = True
                    already_3 = True
                else:
                    time_to.append(['초', d])
                    already_1 = True
            elif word == '분':
                if int(d) > 60 or int(d) < 0:
                    continue
                for i in range(len(index)):
                    msg_arr[index[i]] = ''
                d = util.lpad(d, 2, '0')
                if already_2:
                    time_from.append(['분', d])
                    already_3 = True
                else:
                    time_to.append(['분', d])
                    already_1 = True
                    already_2 = True
            elif word == '시':
                if int(d) > 24 or int(d) < 0:
                    continue
                for i in range(len(index)):
                    msg_arr[index[i]] = ''
                d = util.lpad(d, 2, '0')
                if already_3:
                    time_from.append(['시', d])
                else:
                    time_to.append(['시', d])
                    already_1 = True
                    already_2 = True
                    already_3 = True
    replacedMsg = ''
    for m in msg_arr:
        replacedMsg += m
    kor_nm = chat.get_kor_nm_by_tag_nm('@where:time')
    replacedMsg = replacedMsg.replace('시분초', kor_nm)
    
    return has, time_from, time_to, replacedMsg
