from c_engine.core.util import util

def is_date(s):
    if '.' in s:
        if s.count('.') == 1:
            s += '.01'
    from dateutil.parser import parse
    try: 
        parse(s)
        return True
    except ValueError:
        return False

def scan_and_replace_date(msg):
    l = 10
    for ii in range(l):
        g = l - ii - 1
        if g < 5:
            continue
        i = 0
        aa = []
        bb = []
        while i < len(msg) - g:
            cnt = 0
            a = msg[i:i+g+1]
            if '-' not in a and '/' not in a and '.' not in a and ',' not in a:
                i += 1
                continue 
            if is_date(a.replace(' ', '^')):
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
                            if cnt < 2:
                                if digit < 2:
                                    ar[cur] = util.rpad(ar[cur], 2, '0')
                            else:
                                if digit < 4:
                                    if digit == 2:
                                        ar[cur] = '20' + ar[cur]
                                    else:    
                                        ar[cur] = util.lpad(ar[cur], 4 - digit + 1, '0')
                            cnt += 1
                            digit = 0
                a_1 = ''
                for am in ar:
                    a_1 += am
                replaced = a_1.replace(' ', '').replace('-', '').replace('/', '').replace('.', '').replace(',', '')
                b = replaced[:4] + '년' + replaced[4:6] + '월' + replaced[6:] + '일'
                aa.append(a)
                bb.append(b)
                i += g
            i += 1
        for i in range(len(aa)):
            msg = msg.replace(aa[i], bb[i])
    return msg

def get_regular_date(date_from, date_to):
    date_f = ''
    date_t = ''
    ymd = ['년', '월', '일']
    for w in ymd:
        date_t += date_to[w]
        date_f += date_from[w]
    
    return date_f, date_t
