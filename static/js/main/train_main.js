$(document).ready(function() {	
	start_interval_is_training();
	get_is_training();
	$("#start_training").click(function() {
		var training_status = $("#start_training").text();
		if (training_status == "훈련시작") {
			start_training();
		} else {
			stop_training();
		}
	});
	$("#delete_ckpt_file").click(function() {
		alert("제한된 기능입니다.");
		return;
		delete_ckpt_file();
	});
	$("#update_voca_and_question").click(function() {
		update_voca_and_question();
	});
	$("#create_fragment").click(function() {
		create_fragment();
	});
	$("#show_testing").click(function() {
		show_testing();
	});
});
	
function ajax(url, input_data, gubun, method) {
	var as = false;
	if (gubun == 'start_training') {
		as = true
	}
	$.ajax(url, {
		type: method, 
        data: JSON.stringify(input_data),
        async: as,
        contentType: 'application/json',
        dataType: 'json',
        processData: false,
        success: function (data, status, xhr) {
            if (gubun == "get_training_info") {
            	get_training_info_callback(data['training_info'], data['saving_step']);
            } else if (gubun == "delete_ckpt_file") {
            	delete_ckpt_file_callback();
            }
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}

function start_training() {
	if (!confirm("훈련을 시작 하시겠습니까?")) {
		return;
	}
	$("#start_training").text("훈련중단");
	var user = $("#user").val();
	var project = $("#project").val();
	var saving_step = $("#saving_step").val();
	var input_data = {"user" : user, "project" : project, "saving_step" : saving_step};

	$.post('/start_training', input_data).done(function(reply) {
		alert("훈련이 시작되었습니다.");
		$('#training_info').text('훈련을 준비중입니다..');
		start_interval();
	}).fail(function() {
	});
}

function stop_training() {
	if (!confirm("훈련을 종료 하시겠습니까?")) {
		return;
	}
	$("#start_training").text("훈련시작");	
	var user = $("#user").val();
	var project = $("#project").val();
	var input_data = {"user" : user, "project" : project};
	
	$.post('/stop_training', input_data).done(function(reply) {
		alert("훈련이 중단되었습니다.");
		$('#training_info').text('');
		$('#show_testing').hide();
		stop_interval();
	}).fail(function() {
	});
}

function delete_ckpt_file() {
	if (!confirm("훈련모델을 삭제하시겠습니까?")) {
		return;
	}
	var user = $("#user").val();
	var project = $("#project").val();
	var input_data = {"user" : user, "project" : project};
	ajax('/delete_ckpt_file', input_data, 'delete_ckpt_file', 'POST');	
}

function get_training_info() {
	var user = $("#user").val();
	var project = $("#project").val();
	var input_data = {"user" : user, "project" : project};
	ajax('/get_training_info', input_data, 'get_training_info', 'POST');
}

function get_is_training() {
	var user = $("#user").val();
	var project = $("#project").val();
	$.post("/get_is_training", { user : user, project : project}).done(function(reply) {
		if (reply['is_training'] == 'Y') {
			$("#start_training").text('훈련중단');
			start_interval();
		} else {
			$("#start_training").text('훈련시작');
			stop_interval();
			$('#training_info').text('');
			$('#show_testing').hide();
		}
	}).fail(function() {
	});
}

function get_training_info_callback(training_info, saving_step) {
	if (training_info.indexOf("현재스텝") != -1) {
		$('#show_testing').show();
	} else {
		$('#show_testing').hide();
	}
	$('#training_info').html(training_info.replace(/,/gi, '<br>'))
	$('#saving_step').val(saving_step)
}

function delete_ckpt_file_callback() {
	alert("훈련모델이 삭제되었습니다.");
}

var interval_name = '';
var interval_name_is_training = '';

function start_interval() {
	if (interval_name == '') {
		interval_name = setInterval(function() {get_training_info();}, 2000);
	}
}

function start_interval_is_training() {
	interval_name_is_training = setInterval(function() {get_is_training();}, 5000);
}

function stop_interval() {
	clearInterval(interval_name);
	interval_name = '';
}

function stop_interval_is_training() {
	clearInterval(interval_name_is_training);
}

function update_voca_and_question() {
	var w = UPDATE_QUESTION_VOCA_MAIN_POPUP_WIDTH;
	var h = UPDATE_QUESTION_VOCA_MAIN_POPUP_HEIGHT;
	var x = (screen.width - w) / 2;
    var y = (screen.height - h) / 3;
	var user = $("#user").val();
	var project = $("#project").val();
	
	window.open('/update_question_voca_main?user=' + user + '&project=' + project, '_blank', 'scrollbars=yes, width=' + w + ', height=' + h + ', left=' + x + ', top=' + y);
}

function create_fragment() {
	var w = QUESTION_GENERATOR_MAIN_POPUP_WIDTH;
	var h = QUESTION_GENERATOR_MAIN_POPUP_HEIGHT;
	var x = (screen.width - w) / 2;
    var y = (screen.height - h) / 3;
	var user = $("#user").val();
	var project = $("#project").val();
	window.open('/question_generator_main?user=' + user + '&project=' + project, '_blank', 'scrollbars=yes, width=' + w + ', height=' + h + ', left=' + x + ', top=' + y);
}

function show_testing() {
	window.parent.$('.bottom-nav').children().show();
	window.parent.$('.bottom-nav').show(1000);
}
