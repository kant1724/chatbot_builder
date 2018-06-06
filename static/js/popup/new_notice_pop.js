$(document).ready(function() {
	$("#submit_notice").click(function() {
		alert("제한된 기능입니다.");
		return;
		submit_notice();
	});
	$("#notice_start_date").datepicker({
		dateFormat: "yy-mm-dd"
	});
	$("#notice_end_date").datepicker({
		dateFormat: "yy-mm-dd"
	});
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
            if (gubun == "submit_notice") {
            	submit_notice_callback();
            }
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}

function submit_notice() {
	if ($("#notice_subject").val() == "") {
		alert("공지제목을 작성하세요.");
		return;
	}
	if ($("#notice_content").val() == "") {
		alert("공지내용을 작성하세요.");
		return;
	}
	if ($("#notice_start_date").val() == "") {
		alert("공지시작일을 입력하세요.");
		return;
	}
	if ($("#notice_end_date").val() == "") {
		alert("공지종료일을 입력하세요.");
		return;
	}
	if ($("#notice_start_date").val() > $("#notice_end_date").val()) {
		alert("공지시작일은 공지종료일 보다 클 수 없습니다.");
		return;
	}
	if (!confirm("전송 하시겠습니까?")) {
		return;
	}
	var user = $("#user").val();
	var project = $("#project").val();
	var gubun = $("#gubun").val();
	var notice_num = $("#notice_num").val();
	var notice_subject = $("#notice_subject").val();
	var notice_content = $("#notice_content").val();
	var notice_start_date = $("#notice_start_date").val();
	var notice_end_date = $("#notice_end_date").val();;
	
	var input_data = {"user" : user, "project" : project, "gubun" : gubun, "notice_num" : notice_num, "notice_subject" : notice_subject, "notice_content" : notice_content, "notice_start_date" : notice_start_date, "notice_end_date" : notice_end_date};
	
	ajax('/submit_notice', input_data, 'submit_notice', 'POST');
}

function submit_notice_callback() {
	alert("전송이 완료되었습니다.");
	opener.search_notice();
	window.close();
}
