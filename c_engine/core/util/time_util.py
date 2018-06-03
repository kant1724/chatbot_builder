from datetime import date
from datetime import datetime
from c_engine.core.util import util

def is_time(s):
    from dateutil.parser import parse
    try: 
        parse(s)
        return True
    except ValueError:
        return False

def scan_and_replace_time(msg):
    l = 8
    for ii in range(l):
        g = l - ii - 1
        if g < 3:
            continue
        i = 0
        aa = []
        bb = []
        while i < len(msg) - g + 1:
            cnt = 0
            a = msg[i:i+g+1]
            if ":" not in a:
                i += 1
                continue
            if is_time(a.replace(' ', '^')):
                a = a.strip()
                ar = []
                for iii in range(len(a)):
                    ar.append(a[iii])
                digit = 0
                for iii in range(len(ar)):
                    cur = len(ar) - iii - 1
                    if util.represents_int(ar[cur]):
                        digit += 1
                    if cur == len(ar) - 1:
                        continue
                    if (util.represents_int(ar[cur + 1]) and util.represents_int(ar[cur]) == False) or (util.represents_int(ar[cur]) and cur == 0):
                        if digit > 0:
                            if cnt < 2 and cur > 0:
                                if digit < 2:
                                    ar[cur] = util.rpad(ar[cur], 2, '0')
                            else:
                                if digit < 2:
                                    ar[cur] = util.lpad(ar[cur], 2 - digit + 1, '0')
                            cnt += 1
                            digit = 0
                a_1 = ''
                for am in ar:
                    a_1 += am
                replaced = a_1.replace(' ', '').replace(':', '')
                b = replaced[:2] + '시' + replaced[2:4] + '분' + replaced[4:] + '초'
                aa.append(a)
                bb.append(b)
                i += g
            i += 1
        for i in range(len(aa)):
            msg = msg.replace(aa[i], bb[i])
    return msg

def get_regular_time(time_from, time_to):
    time_f = ''
    time_t = ''
    ymd = ['시', '분', '초']
    now = datetime.now()
    to_hour = ''
    to_minute = ''
    to_second = ''
    for w in ymd:
        has_1 = False
        for d in time_to:
            if d[0] == w:
                has_1 = True
                time_t += d[1]
        if has_1 == False:
            if w == '시':
                time_t += str(now.hour)
            elif w == '분':
                time_t += '60'
            elif w == '초':
                time_t += '60'
        if has_1 and w == '시':
            to_hour = time_t
        if has_1 and w == '분':
            to_minute = time_t[2:]
        if has_1 and w == '초':
            to_second = time_t[4:]
        has_2 = False
        for d in time_from:
            if d[0] == w:
                has_2 = True
                time_f += d[1]
        if has_2 == False:
            if w == '시':
                if to_hour != '':
                    time_f += to_hour
                else:
                    time_f += str(now.hour)
            elif w == '분':
                if to_minute != '':
                    time_f += to_minute
                else:
                    time_f += '00'
            elif w == '초':
                if to_second != '':
                    time_f += to_second
                else:
                    time_f += '00'
        if w == '시':
            if has_1 == False:
                time_t = time_f
                
    return time_f, time_t

