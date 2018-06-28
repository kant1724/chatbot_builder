$(document).ready(function() {
	$("#search_answer").click(function() {
		search_answer();
	});
	$("#subject").keydown(function (key) {
        if (key.keyCode == 13) {
        	search_answer();
        }
    });
	search_answer();
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
            if (gubun == "search_answer") {
            	search_answer_callback(data);
            } else if (gubun == "modify_answer") {
            	modify_answer_callback();
            }
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}

function search_answer() {
	var gubun = $("#gubun option:selected").val();
	var subject = $("#subject").val();
	var user = $("#user").val();
	var project = $("#project").val();
	var input_data = {"gubun" : gubun, "subject" : subject, "user" : user, "project" : project};
	
	ajax('/search_answer', input_data, 'search_answer', 'POST');
}

function modify_answer(div_id) {
	var div = $('#' + div_id);
	var answer_num = div.find("#answer_num").val();
	var category_num = div.find("#category_num").val();
	var question = div.find("#question").val();
	var answer = div.find("#answer").val();
	if (!confirm("전송 하시겠습니까?")) {
		return;
	}
	var user = $("#user").val();
	var project = $("#project").val();
	var input_data = {"user" : user, "project" : project, "answer_num" : answer_num, "rpsn_question" : question, "answer" : answer, "category_num" : category_num};
	
	ajax('/modify_answer', input_data, 'modify_answer', 'POST');
}

function search_answer_callback(retData) {
	var retList = retData['results'];
	$('#container').children().remove();
	for (var i = 0; i < retList.length; ++i) {
		var num = i + 1;
		var div_id = "div_no" + num 
		$('#container').append('<div id="' + div_id + '"><div class="upper"><a>[' + num + ']</a><button class="btn" id="btn' + num + '">저장</button></div>');
		$('#' + div_id).append('<p><div class="each" id="' + div_id + '_each">');
		$('#' + div_id + "_each").append('<input id="answer_num" type="hidden" value="' + retList[i]['answer_num'] + '">');
		$('#' + div_id + "_each").append('<input id="category_num" type="hidden" value="' + retList[i]['category_num'] + '">');
		$('#' + div_id + "_each").append('<textarea class="question" id="question" rows="8" cols="80">' + retList[i]['rpsn_question'] + '</textarea>');
		$('#' + div_id + "_each").append('<textarea class="answer" id="answer" rows="8" cols="80">' + retList[i]['answer'] + '</textarea>');
		$('#' + div_id + "_each").append('<button id="put_emphasis" class="put_emphasis">강조</button>');
		$('#container').append('</div></div>');
	}
	$(".btn").click(function() {
		var div_id = $(this).parent().parent().prop('id');
		$("#cur_div_id").val(div_id);
		modify_answer(div_id);
	});
	$(".put_emphasis").click(function() {
		put_emphasis($(this).parent().find('#answer'));
	});
}

function modify_answer_callback() {
	alert("전송되었습니다.");
}

function put_emphasis(txtarea) {
	replaceSelectedText(txtarea);
}
