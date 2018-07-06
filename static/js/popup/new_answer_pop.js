$(document).ready(function() {
	$("#submit_answer").click(function() {
		submit_answer();
	});
	$("#put_emphasis").click(function() {
		put_emphasis();
	});
	search_category();
	if ($('#rq_num').val() != '') {
		search_new_request_by_rq_num();
	}	
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
            if (gubun == "submit_answer") {
            	submit_answer_callback();
            } else if (gubun == "search_category") {
        		search_category_callback(data['results']);
            } else if (gubun == "search_new_request_by_rq_num") {
            	search_new_request_by_rq_num_callback(data['results']);
            }
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}

function submit_answer() {
	if ($("#question_input").val() == "") {
		alert("질문을 작성하세요");
		return;
	}
	if ($("#answer_input").val() == "") {
		alert("답변을 작성하세요");
		return;
	}
	if (!confirm("전송 하시겠습니까?")) {
		return;
	}
	var user = $("#user").val();
	var project = $("#project").val();
	var question_input = $("#question_input").val();
	var question_tag_input = '';
	var answer_input = $("#answer_input").val();
	var category_num = $("#category_num").val();
	var rq_num = $("#rq_num").val();
	var input_data = {"user" : user, "project" : project, "question" : question_input, "question_tag" : question_tag_input, "answer" : answer_input, "category_num" : category_num, "rq_num" : rq_num};
	
	ajax('/submit_answer', input_data, 'submit_answer', 'POST');
}

function submit_answer_callback() {
	alert("전송이 완료되었습니다.");
	if (opener.search_answer != null) {
		opener.search_answer();
	}
	window.close();
}

function search_new_request_by_rq_num() {
	var user = $("#user").val();
	var project = $("#project").val();
	var rq_num = $("#rq_num").val();
	var input_data = {"user" : user, "project" : project, "rq_num" : rq_num};
	ajax('/search_new_request_by_rq_num', input_data, 'search_new_request_by_rq_num', 'POST');
}

function search_new_request_by_rq_num_callback(ret_data) {
	$('#question_input').val(ret_data["question"]);
}

function put_emphasis() {
	replaceSelectedText($("#answer_input"));
}
