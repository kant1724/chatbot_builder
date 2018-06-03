import time
import datetime
import dateutil.relativedelta

alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
def alphabet_to_num(alphabet):
    num_str = ''
    for i in range(len(alphabet)):
        for j in range(len(alpha)):
            if alphabet[i] == alpha[j]:
                num_str += str(j)
                break            
    return int(num_str)
    
def num_to_alphabet(num):
    s = str(num)
    while len(s) < 3:
        s = '0' + s
    key = ""
    for i in range(len(s)):
        key += alpha[int(s[i])]
        
    return key

def get_hyphen_date(date):
    return date[:4] + '-' + date[4:6] + '-' + date[6:]

def get_colon_time(time):
    return time[:2] + ':' + time[2:4] + ':' + time[4:]

def is_in_date(date1, date2):
    now = time.strftime("%Y-%m-%d")
    if now < date1 or now > date2:
        return False 

    return True

def get_one_month_ago():
    now = datetime.datetime.now()
    one_month_ago = now + dateutil.relativedelta.relativedelta(months=-1)
    
    return one_month_ago.strftime("%Y%m%d")
