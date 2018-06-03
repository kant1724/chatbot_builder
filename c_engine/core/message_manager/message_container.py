def get_wrong_input_msg(message_count):
    return '이 질문의 신규답변을 학습 시키겠습니까?<br> - 요청 진행상태는 우측 [신규요청(MY)] 또는 [신규요청(ALL)] 에서 확인 가능합니다. 추천순위로 채택시 챗봇에 반영됩니다.<br><a href="#" onclick="requestNewAnswer(&quot;' + str(message_count) + '&quot;);return false;">[예]</a><br><br><a href="#" onclick="noRequestNewAnswer(&quot;' + str(message_count) + '&quot;);return false;">[아니오]</a>'

def get_right_yn_href_msg(message_count):
    thumbs_up = '<img class="thumbs-up-image" onclick="rightAnswer(&quot;' + str(message_count) + '&quot;);return false;" src="/static/res/thumbs_up.png" />'
    thumbs_down = '<img class="thumbs-up-image" onclick="wrongAnswer(&quot;' + str(message_count) + '&quot;);return false;" src="/static/res/thumbs_down.png" />'
    html = '<a style="font-weight:700;font-size:0.9em;">해당 답변이  도움이 되셨습니까?</a><br><a style="font-size:0.9em;">* 신규답변 학습 및 등록 요청시 :<br> - 요청 진행상태는 우측 [신규요청(MY)] 또는 [신규요청(ALL)] 에서 확인 가능합니다. 추천순위로 채택시 챗봇에 반영됩니다.</a>'
    html += '<p>' + thumbs_up + '&nbsp;&nbsp;' + thumbs_down + '<br><a style="font-size:0.9em;" href="#" onclick="requestNewAnswer(&quot;' + str(message_count) + '&quot;);return false;">[신규답변 학습 및 등록 요청]</a>'
    return html

def get_select_answer_from_list():
    return '<img class="question-mark" src="static/res/question_mark.png" />&nbsp;&nbsp;<a style="font-weight: 700;">아래 질문중 해당하는 번호를 입력하세요.</a><br><br>'

def get_select_question_from_list():
    return '<img class="question-mark" src="static/res/question_mark.png" />&nbsp;&nbsp;<a style="font-weight: 700;">아래 내용 중 해당하는 질문을 직접입력 또는 마우스로 클릭하세요.</a><br><br>'

def get_not_trained_message():
    return '<img class="exclamation-mark" src="static/res/exclamation_mark.png" />&nbsp;&nbsp;<a>해당 질문에 대한 답변이 학습되지 않았습니다.</a>'

def get_reserve_question(message):
    return '<div class="reserve-question-div" onclick="setMessageInput(\'' + message.replace('"', '') + '\')"><img class="check-mark" src="static/res/blue_check_mark.png" />&nbsp;&nbsp;<a class="reserve-question-message">' + message + '</a></div><br>'

def get_last_mdfc_date(last_mdfc_date):
    d = last_mdfc_date[0 : 4] + '-' + last_mdfc_date[4 : 6] + '-' + last_mdfc_date[6 : 8]
    return '<br><br><a style="font-weight:700; font-size:0.85em">- 답변의 최종변경일자 : ' + d + "</a>"
