$(document).ready(function() {	
	$("#start_training").click(function() {
		var training_status = $("#start_training").text();
		if (training_status == "훈련시작") {
			start_training();
		} else {
			stop_training();
		}
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

function get_training_info_callback(training_info, saving_step) {
	if (training_info.indexOf("현재스텝") != -1) {
		$('#show_testing').show();
	} else {
		$('#show_testing').hide();
	}
	$('#training_info').html(training_info.replace(/,/gi, '<br>'))
	$('#saving_step').val(saving_step)
}

