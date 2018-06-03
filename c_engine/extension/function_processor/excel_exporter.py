from c_engine.core.util import util
from e_database import chat
import pandas as pd
import datetime
import numpy as np

def filter_entire_layout_cnwr_excel(date_from, date_to):
    input_file = './static/data/레이아웃공사내역.xls'
    dt = datetime.datetime.now().isoformat()
    dt = dt.replace('-', '').replace(':', '').replace('.', '')
    output_file = './static/output_' + dt + '.xlsx'
    data_frame = pd.read_excel(input_file, 'sheet1', index_col=None)
    cond = data_frame['승인일자'].str.replace('-', '')
    ymd_from = date_from
    ymd_to = date_to
    t = []
    cnt = 0
    for i in range(len(cond)):
        if cond[i].strip() == '':
            t.append(False)
        elif int(cond[i]) >= int(ymd_from) and int(cond[i]) <= int(ymd_to):
            t.append(True)
            cnt += 1
        else:
            t.append(False) 
    data_frame_value_meets_condition = data_frame.loc[t, :]
    data_frame_value_meets_condition.to_excel(output_file, index=False)
    
    return output_file, cnt

def get_recommended_vendor_by_brnc(brnc):
    input_file = './static/data/레이아웃공사내역.xls'
    dt = datetime.datetime.now().isoformat()
    dt = dt.replace('-', '').replace(':', '').replace('.', '')    
    data_frame = pd.read_excel(input_file, 'sheet1', index_col=None, converters={'연락처' : str})
    cond = data_frame['승인일자'].str.replace('-', '')
    cond2 = data_frame['업체명']
    cond3 = data_frame['신청부점']
    cond4 = data_frame['품의명']
    cond5 = data_frame['연락처']
    date_list = []
    vendor_list = []
    exec_name_list = []
    phone_list = []
    for i in range(len(cond)):
        if brnc in cond3[i] or cond3[i] in brnc:
            date_list.append(cond[i])
            vendor_list.append(cond2[i])
            exec_name_list.append(cond4[i])
            phone_list.append(cond5[i])
    
    idx = np.argsort(date_list)
    date_list = np.array(date_list)[idx]
    vendor_list = np.array(vendor_list)[idx]
    exec_name_list = np.array(exec_name_list)[idx]
    phone_list = np.array(phone_list)[idx]
    
    if len(date_list) == 0:
        return ['해당 지점의 레이아웃 공사내역이 없습니다.']
    
    msg = '최근 품의일자: ' + util.get_hyphen_date(date_list[len(date_list) - 1]) + '<br>품의명: ' + exec_name_list[len(exec_name_list) - 1]
    msg += '<br><br>추천업체: ' + vendor_list[len(vendor_list) - 1]
    msg += '<br>연락처: ' + phone_list[len(phone_list) - 1]
    
    return msg

def get_cnt_and_amt_of_small_cnwr_by_brnc(brnc, date_from, date_to):
    input_file = './static/data/소액공사내역.xls'
    dt = datetime.datetime.now().isoformat()
    dt = dt.replace('-', '').replace(':', '').replace('.', '')
    output_file = './static/output_' + dt + '.xlsx'
    data_frame = pd.read_excel(input_file, 'sheet1', index_col=None)
    cond = data_frame['승인일자'].str.replace('-', '')
    cond2 = data_frame['신청부점']
    cond3 = data_frame['품의금액']
    ymd_from = date_from
    ymd_to = date_to
    t = []
    cnt = 0
    amt = 0
    for i in range(len(cond)):
        try:
            if brnc not in cond2[i] and cond2[i] not in brnc:
                t.append(False)
                continue
        except:
            t.append(False)
            continue
        if cond[i].strip() == '':
            t.append(False)
        elif int(cond[i]) >= int(ymd_from) and int(cond[i]) <= int(ymd_to):
            t.append(True)
            cnt += 1
            amt += cond3[i]
        else:
            t.append(False)

    data_frame_value_meets_condition = data_frame.loc[t, :]
    data_frame_value_meets_condition.to_excel(output_file, index=False)
    
    return output_file, cnt, amt

def get_depreciation_complete_movables_by_brnc(brnc):
    brnc_arr = chat.get_all_brnc_nm_list()
    brnc_nm = ''
    for i in range(len(brnc_arr)):
        if brnc in brnc_arr[i] or brnc_arr[i] in brnc:
            brnc_nm = brnc_arr[i]
            break
    if brnc_nm == '상계역':
        input_file = './static/data/상계역_동산.xls'
    elif brnc_nm == '쌍문역':
        input_file = './static/data/쌍문역_동산.xls'
    
    dt = datetime.datetime.now().isoformat()
    dt = dt.replace('-', '').replace(':', '').replace('.', '')
    output_file = './static/output_' + dt + '.xlsx'
    data_frame = pd.read_excel(input_file, 'sheet1', index_col=None)
    cond = data_frame['잔존가']    
    t = []
    cnt = 0
    for i in range(len(cond)):
        if cond[i] == None:
            t.append(False)
        elif int(cond[i]) <= 1000:
            t.append(True)
            cnt += 1
        else:
            t.append(False)

    data_frame_value_meets_condition = data_frame.loc[t, :]
    data_frame_value_meets_condition.to_excel(output_file, index=False)
    
    return output_file, cnt

def get_furniture_qty_and_amt_by_brnc(brnc):
    brnc_arr = chat.get_all_brnc_nm_list()
    furn_arr = ['의자', '책상', '카운터', '쇼파', '옷장', '탁자', '테이블']
    brnc_nm = ''
    for i in range(len(brnc_arr)):
        if brnc in brnc_arr[i] or brnc_arr[i] in brnc:
            brnc_nm = brnc_arr[i]
            break
    if brnc_nm == '상계역':
        input_file = './static/data/상계역_동산.xls'
    elif brnc_nm == '쌍문역':
        input_file = './static/data/쌍문역_동산.xls'
    
    dt = datetime.datetime.now().isoformat()
    dt = dt.replace('-', '').replace(':', '').replace('.', '')
    output_file = './static/output_' + dt + '.xlsx'
    data_frame = pd.read_excel(input_file, 'sheet1', index_col=None)
    cond = data_frame['물품분류']    
    t = []
    cnt = 0
    for i in range(len(cond)):
        if cond[i] == None:
            t.append(False)
        elif cond[i] in furn_arr:
            t.append(True)
            cnt += 1
        else:
            t.append(False)

    data_frame_value_meets_condition = data_frame.loc[t, :]
    data_frame_value_meets_condition.to_excel(output_file, index=False)
    
    return output_file, cnt

def get_all_from_estimate_by_brnc_for_export_excel(brnc):
    input_file = './static/data/견적요청현황.xls'
    dt = datetime.datetime.now().isoformat()
    dt = dt.replace('-', '').replace(':', '').replace('.', '')
    output_file = './static/output_' + dt + '.xlsx'
    data_frame = pd.read_excel(input_file, 'sheet1', index_col=None)
    cond = data_frame['신청부점명']
    t = []
    cnt = 0
    for i in range(len(cond)):
        try:
            if brnc not in cond[i] and cond[i] not in brnc:
                t.append(False)
                continue
        except:
            t.append(False)
            continue
        
        t.append(True)
        cnt += 1

    data_frame_value_meets_condition = data_frame.loc[t, :]
    data_frame_value_meets_condition.to_excel(output_file, index=False)
    
    return output_file, cnt
