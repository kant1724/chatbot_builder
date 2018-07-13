$(document).ready(function() {	
	$("#question").keydown(function (key) {
        if (key.keyCode == 13) {
        	get_answer();
        }
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
            if (gubun == "run_main_get_answer") {
            	run_main_get_answer_callback(data);
            }
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}

function get_answer() {
	var user = $("#user").val();
	var project = $("#project").val();
	var msg = $("#question").val();
	var input_data = {"user" : user, "project" : project, "msg" : msg};
	ajax('/run_main_get_answer', input_data, 'run_main_get_answer', 'POST');
}

function run_main_get_answer_callback(data) {
	var answer = data['answer'];
	var point = data['point'];
	var word = data['word'];
	$('#my_question_text').html($("#question").val());
	$('#answer_text').html(answer);
	$('#right_point_text').html(point);
	$('#extracted_word_text').html(word);
	$("#question").val('');
}
