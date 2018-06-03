$(document).ready(function() {
	get_generating_all_fragment_info();
	var is_generating_all_fragment = $("#is_generating_all_fragment").val();
	if (is_generating_all_fragment == 'Y') {
		$("#start_generating_all_fragment").text('질문조각 생성중단');
		start_interval();
	}	
	$("#start_generating_all_fragment").click(function() {
		var generating_status = $("#start_generating_all_fragment").text();
		if (generating_status == "질문조각 생성시작") {
			start_generating_all_fragment();
		} else {
			stop_generating_all_fragment();
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
        	if (gubun == "start_generating_all_fragment") {
        		start_generating_all_fragment_callback();
            } else if (gubun == "stop_generating_all_fragment") {
            	stop_generating_all_fragment_callback();
            } else if (gubun == "get_generating_all_fragment_info") {
            	get_generating_all_fragment_info_callback(data['generating_all_fragment_info'], data['end_yn']);
            }
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}

function start_generating_all_fragment() {
	if (!confirm("질문조각 생성을 시작 하시겠습니까?")) {
		return;
	}
	$("#start_generating_all_fragment").text("질문조각 생성중단");
	var input_data = {};
	var user = $("#user").val();
	var project = $("#project").val();
	ajax('/start_generating_all_fragment?user=' + user + '&project=' + project, input_data, 'start_generating_all_fragment', 'GET');
}

function stop_generating_all_fragment() {
	if (!confirm("질문조각 생성을 중단 하시겠습니까?")) {
		return;
	}
	$("#start_generating_all_fragment").text("질문조각 생성시작");
	var input_data = {};
	var user = $("#user").val();
	var project = $("#project").val();
	ajax('/stop_generating_all_fragment?user=' + user + '&project=' + project, input_data, 'stop_generating_all_fragment', 'GET');
}

function get_generating_all_fragment_info() {
	var input_data = {};
	var user = $("#user").val();
	var project = $("#project").val();
	var input_data = {};
	ajax('/get_generating_all_fragment_info?user=' + user + '&project=' + project, input_data, 'get_generating_all_fragment_info', 'POST');
}

function get_generating_all_fragment_info_callback(generating_all_fragment_info, end_yn) {
	$('#generating_all_fragment_info').text(generating_all_fragment_info);
	if (end_yn == "Y") {
		$("#start_generating_all_fragment").text("질문조각 생성시작");
	}
}

function start_generating_all_fragment_callback() {
	alert("질문조각 생성이 시작되었습니다.");
	$('#generating_all_fragment_info').text('생성 중입니다.');
	start_interval();
}

function stop_generating_all_fragment_callback() {
	alert("질문조각 생성이 중단되었습니다.");
	get_generating_all_fragment_info();
	stop_interval();
}

var interval_name = ''

function start_interval() {
	interval_name = setInterval(function() {get_generating_all_fragment_info();}, 1000);
}

function stop_interval() {
	clearInterval(interval_name);
}
