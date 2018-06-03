$(document).ready(function() {
	$("#submit_function").click(function() {
		submit_function();
	});
	$("#create_function").click(function() {
		create_function();
	});
	$("#new_tag_pop").click(function() {
		new_tag_pop();
	});
	
	search_tag();
});
	
function ajax(url, input_data, gubun, method) {
	$.ajax(url, {
		type: method, 
        data: JSON.stringify(input_data),
        async: false,
        contentType: 'application/json',
        dataType: 'json',
        processData: false,
        success: function (data, status, xhr) {
            if (gubun == "submit_function") {
            	submit_function_callback();
            }
            if (gubun == "search_tag") {
            	search_tag_callback(data['results']);
            }
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}

function submit_function() {
	if ($("#function_input").val() == "") {
		alert("답변을 작성하세요");
		return;
	}
	if (!confirm("전송 하시겠습니까?")) {
		return;
	}
	var user = $("#user").val();
	var project = $("#project").val();
	var answer = $("#answer").val();
	var question = $("#text_input").val();
	var question_tag = $("#tag_input").val();
	var input_data = {"user" : user, "project" : project, "answer" : answer, "question" : question, "question_tag" : question_tag};
	
	ajax('/submit_answer', input_data, 'submit_function', 'POST');
}

function create_function() {
	var from = $("#from option:selected").text();
	var select = $("#select option:selected").text();
	var where = $("#where option:selected").text();
	var action = $("#action option:selected").text();
	var f = where + "의 " + select + "을 " + from + "에서 " + action;
	
	$("#text_input").val(f);
	
	var from = $("#from option:selected").val();
	var select = $("#select option:selected").val();
	var where = $("#where option:selected").val();
	var action = $("#action option:selected").val();
	var f = where + " 의 " + select + " 을 " + from + " 에서 " + action;
	
	$("#tag_input").val(f);
	
	$('#answer').val("$CALL get_" + select.split(":")[1] + "_from_" + from.split(":")[1] + "_by_" + where.split(":")[1] + "_for_" + action.split(":")[1] + "()");
}

function new_tag_pop() {
	var w = NEW_TAG_POPUP_WIDTH;
	var h = NEW_TAG_POPUP_HEIGHT;
	var y = window.top.outerHeight / 2 + window.top.screenY - ( h / 2);
	var x = window.top.outerWidth / 2 + window.top.screenX - ( w / 2);
	
	window.open('/new_tag_pop', '_blank', 'width=' + w + ', height=' + h + ', left=' + x + ', top=' + y);
}

function submit_function_callback() {
	alert("전송이 완료되었습니다.");
	window.close();
}

function search_tag() {
	var gubun = ['select', 'from', 'where', 'action'];
	for (var i = 0; i < gubun.length; ++i) {
		var input_data = {"gubun" : gubun[i]};
		ajax('/search_tag', input_data, 'search_tag', 'POST');
	}
}

function search_tag_callback(res) {
	for (var i = 0; i < res.length; ++i) {
		var ele = '<option value="' + res[i]['tag_nm'] + '">' + res[i]['kor_nm'] + '</option>';
		$("#" + res[i]['gubun']).append(ele);
	}
}
