def compare_my_question_and_right_question(voca_and_appearance, base, question, right_question_voca):
    right_voca_arr = right_question_voca.split(';')
    has = []
    voca_dict = {}
    for vaa in voca_and_appearance:
        voca_dict[vaa['voca_nm']] = vaa['appearance_count']
    total = 0
    my = 0
    a = []
    b = []
    for right_voca in right_voca_arr:
        if right_voca == '':
            continue
        cur_point = 1 / pow(float(base), voca_dict[right_voca] - 1)
        a.append(right_voca + ":" + str(round(cur_point, 3)))
        total += cur_point
        synonym_list = right_voca.split("^")
        question_arr = question.split(" ")
        question_composition_arr = []
        merged_yn = []
        for i in range(len(question_arr)):
            q = ""
            j = i
            while j < len(question_arr):
                if j == i:
                    merged_yn.append(False)
                else:
                    merged_yn.append(True)
                q += question_arr[j]
                question_composition_arr.append(q)
                j += 1
        for synonym in synonym_list: 
            for i in range(len(question_composition_arr)):
                if synonym in question_composition_arr[i]:
                    if merged_yn[i] and synonym[0] != question_composition_arr[i][0]:
                        continue
                    b.append(right_voca + ":" + str(round(cur_point, 3)))
                    my += cur_point
                    break
    if total == 0:
        total = 1
    point = round(my / total * 100, 3)    
    msg = '일치단어: ' + ",".join(has) + ', 일치 포인트: ' + str(point) + '점<br><br>'
    msg += '일치포인트 산식:<br>∑k=1→n (1 / ' + base + '^(단어출현빈도(a(k)) - 1):a=[내질문∩정답질문])<br>'
    msg += '/<br>'
    msg += '∑k=1→n (1 / ' + base + '^(단어출현빈도(a(k)) - 1):a=[정답질문])<br><br>'
    msg += '내 질문 포인트 :<br>' + "<br>".join(b)
    msg += '<br><br>전체 질문 포인트 :<br>' + "<br>".join(a)
    
    return msg, point
