from urllib.request import quote

def get_hyphen_date(date):
    return date[:4] + '-' + date[4:6] + '-' + date[6:]

def get_colon_time(time):
    return time[:2] + ':' + time[2:4] + ':' + time[4:]

def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def lpad(s, l, p):
    while len(s) < l:
        s = p + s
    return s

def rpad(s, l, p):
    while len(s) < l:
        s += p
    return s

def get_quote_word(word):
    return quote(word)

def get_element_by_length(a, length):
    a = reversed(sorted(a, key=len))
    b = []
    for aa in a:
        if len(b) >= length:
            break
        b.append(aa)
    return b

def get_comma_str_by_int(num):
    return str(format(num, ',f')).strip('0').strip('.')

def isNull(s):
    if s == None or s == '':
        return True
    return False
