var $messages = $('.messages-content'),
    d, h, m,
    i = 0;

$(window).load(function() {
	$messages.mCustomScrollbar();
	var text = "저는 i-Learning이라고 해요<br>펀드에 관하여 무엇이던지 물어보세요 ^^<br>아직 많이 부족하지만 많은 관심이 저를 더욱더 성장하게 만든답니다.";
	reply_answer(text);
	var notice_list = eval($('#notice_list').val());
	for (var i = 0; i < notice_list.length; ++i) {
		var notice = notice_list[i].replace('\n', '<br>');
		reply_answer(notice);
	}
	setMySchedule();
});

function updateScrollbar() {
	$('#scroll-down').mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
	    scrollInertia: 1,
	    timeout: 0
	});
	$('#scroll-top').mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'top', {
	    scrollInertia: 1,
	    timeout: 0
	});
}

function setDate(){
  d = new Date()
  if (m != d.getMinutes()) {
    m = d.getMinutes();
    $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
  }
}

function insertMessage() {
  msg = $('.message-input').val();
  if ($.trim(msg) == '') {
    return false;
  }
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('#left-board .mCSB_container')).addClass('new');
  setDate();
  $('.message-input').val(null);
  updateScrollbar();
  interact(msg);
  setTimeout(function() {
    //fakeMessage();
  }, 1000 + (Math.random() * 20) * 100);
}

$('.message-submit').click(function() {
  insertMessage();
});
var len_list = [2, 3, 4, 6, 7, 8, 10, 15, 20, 25, 30, 35, 42, 50, 70];
var iindex = 0;

function getMenuRadioValue() {
	return $('input[name="msg2_radio"]:checked').val();
}

function getMessage3RadioValue() {
	return $('input[name="msg3_radio"]:checked').val();
}

$(".message-input").on('input', function() {
	if (getMenuRadioValue() == '2') return;
	if (iindex < 0) iindex = 0;
	msg = $('.message-input').val();
	var re = "[ㄱ-ㅎ]";
	last = msg.substring(msg.length - 1);
	a = last.match(re);
	if (a != null) return;
	if (msg.length == 0) {
		iindex = 0;
		$('#message2 .mCSB_container').empty();
	} else {
		if (msg.length > len_list[iindex]) {
			for (var i = 0; i < len_list.length; ++i) {
				if (msg.length < len_list[i]) {
					iindex = i - 1;
					break;
				}
			}
			if (msg.length == len_list[iindex]) {
				getReserveList(msg);
			}
		} else if (msg.length == len_list[iindex]) {			
			getReserveList(msg);
		} else if (iindex >= 0 && msg.length < len_list[iindex]) {
			for (var i = 0; i < len_list.length; ++i) {
				if (msg.length < len_list[i]) {
					iindex = i - 1;
					break;
				}
			}
			getReserveList(msg);
		}
	}
});

$('input:radio[name="msg2_radio"]').filter('[value="1"]').attr('checked', true);
$('input:radio[name="msg3_radio"]').filter('[value="1"]').attr('checked', true);

$('#radio1 input:radio').click(function() {
	$('#message2 .mCSB_container').empty();
	if (getMenuRadioValue() == '2') {
		getMyQuestion();
	}
});

$('#radio2 input:radio').click(function() {
	$('#message3 .mCSB_container').empty();
	var val = getMessage3RadioValue();
	if (val == '1') {
		setMySchedule();
	}
	if (val == '2') {
		alert("투표");
	}
	if (val == '3' || val == '4') {
		var text = '<img class="exclamation-mark" src="static/res/exclamation_mark.png" />&nbsp;&nbsp;신규등록 요청한 질문들을 보여줍니다.<br>추천수가 많으면 많을수록 신규질문으로 채택될 가능성이 높아져요!<br>학습시키고 싶은 질문이 있으면 추천버튼을 클릭 부탁드려요^^';
		reply_answer(text);
		getRequestQuestion();	
	} else if (val == '5') {
		getNewQuestion();
	}
});

function reply_answer(text) {
	$('<div class="message new"><figure class="avatar"><img src="/static/res/ai_image2.png" /></figure>' + text + '</div>').appendTo($('#left-board .mCSB_container')).addClass('new');
}

$(window).on('keydown', function(e) {
	if (e.which == 13) {
		insertMessage();
		return false;
	}
});

$(function () {
     var obj = $("#left-board");

     obj.on('dragenter', function (e) {
          e.stopPropagation();
          e.preventDefault();
     });

     obj.on('dragleave', function (e) {
          e.stopPropagation();
          e.preventDefault();
     });

     obj.on('dragover', function (e) {
          e.stopPropagation();
          e.preventDefault();
     });

     obj.on('drop', function (e) {
          e.preventDefault();
          var files = e.originalEvent.dataTransfer.files;
          if (files.length < 1) {
               return;
          }
          if (files.length > 1) {
        	  alert("하나의 파일만 드랍 하세요.");
          }
          //sendFile(files);
     });
});

function sendFile(send_file) {
	var data = new FormData();
    for (var i = 0; i < send_file.length; i++) {
       data.append('file', send_file[i]);
    }
    msg = '이미지 인식 요청'
    $('<div class="message message-personal">' + msg + '</div>').appendTo($('#left-board .mCSB_container')).addClass('new');
    $.ajax({
        url: '/send_file',
        method: 'post',
        data: send_file[0],
        dataType: 'json',
        async: false,
        processData: false,
        contentType: 'application/json',
        success: function(res) {
        	$('<div class="message new"><figure class="avatar"><img src="/static/res/ai_image2.png" /></figure>' + res['text'] + '</div>').appendTo($('#left-board .mCSB_container')).addClass('new');
        	updateScrollbar();
        }
     });
}

function getReserveList(message) {
	$.post('/reserve_list', {
		user : $('#user').val(),
		project : $('#project').val(),
		msg : message
	}).done(function(reply) {
		if (getMenuRadioValue() == '2') return;
		if (Number(reply['num']) > 0) {
			$('#message2 .mCSB_container').empty();
		}
		var bucket_id = reply['bucket_id'];
		var bucket_range = reply['bucket_range'];
		$('<div class="bucket-info">- 버킷: [ID: ' + bucket_id + ', 토큰길이: ' + bucket_range + '] 탐색 결과 -</div>').appendTo($('#message2 .mCSB_container')).addClass('new');
		for (var i = 0; i < Number(reply['num']); ++i) {
			var text = reply['text' + (i + 1)];
			var html = '<div id="reserve_msg" class="reserve-msg" onclick="setMessageInput(\'' + text.replace(/\"/g, '') + '\')">';
				html += '<img class="check-mark" src="static/res/green_check_mark.png" />&nbsp;&nbsp;' + text + '</div>';
			$(html).appendTo($('#message2 .mCSB_container')).addClass('new');
		}
		updateScrollbar();
		}).fail(function() {
		});
}

function getMyQuestion() {
	$.post('/my_question', {
	}).done(function(reply) {
		if (Number(reply['num']) > 0) {
			$('#message2 .mCSB_container').empty();
		}
		var text = '- 채팅창에 "자주하는질문"을 입력하여 나의 질문을 등록하세요 -';
		$('<div class="my-question-msg">' + text + '</div>').appendTo($('#message2 .mCSB_container')).addClass('new');
		for (var i = 0; i < Number(reply['num']); ++i) {
			var text = reply['text' + (i + 1)];
			var html = '<div id="reserve_msg" class="reserve-msg" onclick="setMessageInput(\'' + text.replace(/\"/g, '') + '\')">';
				html += '<img class="check-mark" src="static/res/green_check_mark.png" />&nbsp;&nbsp;' + text + '</div>';
			$(html).appendTo($('#message2 .mCSB_container')).addClass('new');
		}
		updateScrollbar();
		}).fail(function() {
		});
}

var pc_status_code = {'01' : '요청중', '02' : '처리완료'};
function getRequestQuestion() {
	var val = getMessage3RadioValue();
	if (val == "3") {
		gubun = 'my';
	} else if (val == "4") {
		gubun = 'all';
	}
	$.post('/get_request_question', {
		user : $('#user').val(),
		project : $('#project').val(),
		gubun : gubun
	}).done(function(reply) {
		if (Number(reply['num']) > 0) {
			$('#message3 .mCSB_container').empty();
		}
		for (var i = 0; i < Number(reply['num']); ++i) {
			var rq_num = reply['rq_num' + (i + 1)];
			var text = reply['question' + (i + 1)];
			var recommend_cnt = reply['recommend_cnt' + (i + 1)];
			var pc_status = reply['pc_status' + (i + 1)];
			var html_tag = '<div id="request_question" class="request-question">' + text;
				html_tag += '<figure class="recommend-image"><img onclick="recommendRequest(' + rq_num + ')" id="' + rq_num + '" src="/static/res/recommend.png" /></figure>';
				html_tag += '<div class="recommend-cnt">' + recommend_cnt + '회 추천됨</div>';
				html_tag += '<div class="pc-status">(상태 : ' + pc_status_code[pc_status] + ')</div>';
				html_tag += '</div>';
			$(html_tag).appendTo($('#message3 .mCSB_container')).addClass('new');
		}
		updateScrollbar();
		}).fail(function() {
		});
}

function setMySchedule() {
	$.post('/get_all_schedule', {
	}).done(function(reply) {
		$('#message3 .mCSB_container').empty();
		var text = '채팅창에 "내 일정"이라고 입력하여 나의 일정을 등록 해 주세요.';
		$('<div class="schedule-msg">' + text + '</div>').appendTo($('#right-down-board .mCSB_container')).addClass('new');
		for (var i = 0; i < reply.length; ++i) {
			var message = reply[i]['message'];
			var html = '<div class="schedule-list">' + message + '</div>';
			if (i < reply.length - 1) {
				html += '<a class="schedule-go-down">▼</a>'; 
			}
			$(html).appendTo($('#right-down-board .mCSB_container')).addClass('new');
		}
		updateScrollbar();
		}).fail(function() {
		});
}

function recommendRequest(rq_num) {
	$.post('/recommend_request', {
		user : $('#user').val(),
		project : $('#project').val(),
		rq_num : rq_num
	}).done(function(reply) {
		alert("추천 하였습니다.");
		getRequestQuestion();
	}).fail(function() {
	});
}

function getNewQuestion() {
	$.post('/latest_new_question', {
		user : $('#user').val(),
		project : $('#project').val()
	}).done(function(reply) {
		if (Number(reply['num']) > 0) {
			$('#message3 .mCSB_container').empty();			
		}
		var text = '- 최근 한달간 신규등록된 질문목록 입니다 -';
		$('<div class="new-question-msg">' + text + '</div>').appendTo($('#right-down-board .mCSB_container')).addClass('new');
		for (var i = 0; i < Number(reply['num']); ++i) {
			var text = reply['text' + (i + 1)];
			var html = '<div id="latest_new_question" class="latest-new-question" onclick="setMessageInput(\'' + text.replace(/\"/g, '') + '\')">';
				html += '<img class="check-mark" src="static/res/green_check_mark.png" />&nbsp;&nbsp;' + text + '</div>';
			$(html).appendTo($('#right-down-board .mCSB_container')).addClass('new');
		}
		updateScrollbar();
		}).fail(function() {
				});
}

function setMessageInput(text) {
	$('.message-input').val(text);
}

var question = [];
var answer_num = [];
var div_id = [];
var temp = "";
var param_holder_dict = {};
var multiple_answer_num = "";
var page = 1;
function rightAnswer(msg_count){
	var q = "";
	var a = "";
	for (var i = 0; i < div_id.length; ++i) {
		if (msg_count != "" && div_id[i] == msg_count) {
			q = question[i];
			a = answer_num[i];
			break;
		}
	}
	$.post('/right_answer', {
		qst : q,
		ans_num : a
	}).done(function(reply) {
		$('#' + msg_count).remove();
		alert('예를 선택하였습니다.');
	}).fail(function() {
		alert('error calling function');
	});
}

function wrongAnswer(msg_count) {
	var q = "";
	var a = "";
	for (var i = 0; i < div_id.length; ++i) {
		if (msg_count != "" && div_id[i] == msg_count) {
			q = question[i];
			a = answer_num[i];
			break;
		}
	}
	$.post('/wrong_answer', {
		qst : q,
		ans_num : a
	}).done(function(reply) {
		$('#' + msg_count).remove();
		alert('아니오를 선택하였습니다.');
	}).fail(function() {
		alert('error calling function');
	});
}

function requestNewAnswer(msg_count) {
	var q = "";
	var a = "";
	for (var i = 0; i < div_id.length; ++i) {
		if (msg_count != "" && div_id[i] == msg_count) {
			q = question[i];
			a = answer_num[i];
			break;
		}
	}
	$.post('/request_new_answer', {
		user : $('#user').val(),
		project : $('#project').val(),
		qst : q
	}).done(function(reply) {
		$('#' + msg_count).remove();
		alert('전송되었습니다. 우측 [신규요청(MY)] 또는 [신규요청(ALL)] 에서 확인 가능합니다.');
		getRequestQuestion();
	}).fail(function() {
		alert('error calling function');
	});
}

function noRequestNewAnswer(msg_count) {
	$('#' + msg_count).remove();
}

function interact(message){
	$('<div class="message loading new"><figure class="avatar"><img src="/static/res/ai_image2.png" /></figure><span></span></div>').appendTo($('#left-board .mCSB_container'));
	$.post('/message', {
		user : $('#user').val(),
		project : $('#project').val(),
		msg: message,
		tmp: temp,
		pge: page,
		multiple_answer_num : multiple_answer_num		
	}).done(function(reply) {
	    $('.message.loading').remove();
	    reserve_answer_list = eval(reply['reserve_answer_list']);
	    multiple_answer_num = reply['multiple_answer_num'];
	    message_count = reply['message_count'];
	    temp = reply['temp'];
	    param_holder_dict[message_count] = reply['param_holder'];;
	    page = reply['page'];
	    for (var i = 0; i < Number(reply['num']); ++i) {
	    	var answer = reply['text' + (i + 1)];
	    	if (reply['function_yn'] == 'N' && reply['rpsn_question'] != '' && multiple_answer_num == '') {
	    		q = '<a class="message_question">Q: ' + reply['rpsn_question'] + '<a><br><br>A: ';
	    		answer = q + answer;
	    	}
	    	reply_answer(answer);
	    }
	    image_path_list = eval(reply['image_path']);
	    if (image_path_list != null && image_path_list != '') {
		    for (var i = 0; i < image_path_list.length; ++i) {
		    	$('<div class="message new"><img class="answer-image" src="' + image_path_list[i] + '" /><a href="' + image_path_list[i] + '" target="_blank");">이미지확대</a></div>').appendTo($('#left-board .mCSB_container')).addClass('new');
		    }
	    }
	    if (reply['right_yn'] != '') {
	    	$('<div id=' + message_count + ' class="message new"><figure class="avatar"><img src="/static/res/ai_image2.png" /></figure>' + reply['right_yn'] + '</div>').appendTo($('#left-board .mCSB_container')).addClass('new');
	    }
	    if (reply['right_yn'] != '' && Number(reply['num']) == 1) {
	    	question.push(reply['qst']);
	    	answer_num.push(reply['ans_num']);
	    	div_id.push(message_count);
	    }
	    if (reply['schedule_updated'] == 'Y') {
	    	setMySchedule();
	    }
	    setDate();
	    updateScrollbar();
	    if (getMessage3RadioValue() == '5') {
	    	getLatestQuestion();
	    }
	}).fail(function() {
		$('.message.loading').remove();
		reply_answer("학습되지 않은 질문입니다. 다른 질문으로 부탁드려요!.");
	});
}

function call_img() {
	window.open("./img")
}

function call_excel(output_file) {
	file = output_file.substring(1)
	window.open(file, null);
}

setInterval(function() {
	get_schedule()
}, 60000);

function lpad(s, len, padding) {
	while (s.length < len) {
		s = padding + s;
	}
	return s;
}

function get_schedule() {
	var currentdate = new Date();
	var t = currentdate.getTime() + (1000 * 60 * 5);
	var five_min_after = new Date(t);
	t = lpad("" + currentdate.getHours(), 2, '0') + lpad("" + currentdate.getMinutes(), 2, '0');
	$.post('/get_schedule', {
		 time : t
	}).done(function(reply) {
		for (var i = 0; i < reply.length; ++i) {
			var msg = "아래 일정의 예약시간이 되었습니다.<br>" + reply[i]['message'];
			$('<div class="message schedule"><figure class="avatar"><img src="/static/res/ai_image2.png" /></figure>' + msg + '</div>').appendTo($('#left-board .mCSB_container')).addClass('new');
			setMySchedule();
		}
	}).fail(function() {
	});
}

get_schedule();

function change_background() {
	var bg = $(".bg").css("background-image");
	if (bg.indexOf("background1.jpg") != -1) {
		$(".bg").css("background-image", bg.replace("background1.jpg", "background2.jpg"));
	} else if (bg.indexOf("background2.jpg") != -1) {
		$(".bg").css("background-image", bg.replace("background2.jpg", "background3.jpg"));
	} else if (bg.indexOf("background3.jpg") != -1) {
		$(".bg").css("background-image", bg.replace("background3.jpg", "background4.jpg"));
	} else if (bg.indexOf("background4.jpg") != -1) {
		$(".bg").css("background-image", bg.replace("background4.jpg", "background5.jpg"));
	} else if (bg.indexOf("background5.jpg") != -1) {
		$(".bg").css("background-image", bg.replace("background5.jpg", "background6.jpg"));
	} else if (bg.indexOf("background6.jpg") != -1) {
		$(".bg").css("background-image", bg.replace("background6.jpg", "background7.jpg"));
	} else if (bg.indexOf("background7.jpg") != -1) {
		$(".bg").css("background-image", bg.replace("background7.jpg", "background8.jpg"));
	} else if (bg.indexOf("background8.jpg") != -1) {
		$(".bg").css("background-image", bg.replace("background8.jpg", "background9.jpg"));
	} else if (bg.indexOf("background9.jpg") != -1) {
		$(".bg").css("background-image", bg.replace("background9.jpg", "background10.jpg"));
	} else if (bg.indexOf("background10.jpg") != -1) {
		$(".bg").css("background-image", bg.replace("background10.jpg", "background1.jpg"));
	}
}

function call_main_frame() {
	var user = $('#user').val();
	var project = $('#project').val();
	var w = QNA_MAIN_POPUP_WIDTH;
	var h = QNA_MAIN_POPUP_HEIGHT;
	var y = window.top.outerHeight / 2 + window.top.screenY - ( h / 2) - 50;
	var x = window.top.outerWidth / 2 + window.top.screenX - ( w / 2);
	var strWindowFeatures = 'location=no ,height='+h+',width='+w+',left='+x+',top='+y+',scrollbars=yes, menubar=no, status=no, toolbar=no, titlebar=no';
	window.open('/frame?user=' + user + '&project=' + project, '_blank', strWindowFeatures);
}

function dynamic_grid_pop(message_count, title, column_info, content) {
	var w = 0;
	var c_info = eval(column_info);
	for (var i = 0; i < c_info.length; ++i) {
		w += Number(c_info[i][2]);
	}
	w += 50;
	w = Math.min(w, 950);
	var h = DYNAMIC_GRID_POPUP_HEIGHT;
	var x = (screen.width - w) / 2;
    var y = (screen.height - h) / 3;
    $("#dynamic_grid_user").val($('#user').val());
	$("#dynamic_grid_project").val($('#project').val());
	$("#dynamic_grid_param_holder").val(param_holder_dict[message_count]);
	$("#dynamic_grid_title").val(title);
    $("#dynamic_grid_column_info").val(column_info);
	$("#dynamic_grid_content").val(content);
	
    window.open('', 'dynamic_grid_popup', 'scrollbars=yes, width=' + w + ', height=' + h + ', left=' + x + ', top=' + y);
	$("#form_dynamic_grid_pop").submit();
}

function dynamic_info_pop(message_count, title, column_info, content) {
	var w = DYNAMIC_INFO_POPUP_WIDTH;
	var h = DYNAMIC_INFO_POPUP_HEIGHT;
	var x = (screen.width - w) / 2;
    var y = (screen.height - h) / 3;
    $("#dynamic_info_user").val($('#user').val());
	$("#dynamic_info_project").val($('#project').val());
	$("#dynamic_info_param_holder").val(temp);
	$("#dynamic_info_title").val(title);
	$("#dynamic_info_column_info").val(column_info);
	$("#dynamic_info_content").val(content);
	
	window.open('', 'dynamic_info_popup', 'scrollbars=yes, width=' + w + ', height=' + h + ', left=' + x + ', top=' + y);
	$("#form_dynamic_info_pop").submit();
}

function hwp_report_pop(message_count, title, file_path) {
	var w = HWP_REPORT_POPUP_WIDTH;
	var h = HWP_REPORT_POPUP_HEIGHT;
	var x = (screen.width - w) / 2;
    var y = (screen.height - h) / 3;
    $("#hwp_report_user").val($('#user').val());
	$("#hwp_report_project").val($('#project').val());
	$("#hwp_report_param_holder").val(temp);
	$("#hwp_report_title").val(title);
	$("#hwp_report_file_path").val(file_path);
    
	window.open('', 'hwp_report_popup', 'scrollbars=yes, width=' + w + ', height=' + h + ', left=' + x + ', top=' + y);
	$("#form_hwp_report_pop").submit();
}
