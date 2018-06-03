$(document).ready(function() {
	$("#submit_synonym").click(function() {
		submit_synonym();
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
        	if (gubun == "submit_synonym") {
        		submit_synonym_callback();
            } 
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}

function submit_synonym() {
	if ($("#synonym_nm").val() == "") {
		alert("동의어를 작성하세요");
		return;
	}
	if (!confirm("전송 하시겠습니까?")) {
		return;
	}
	var synonym_num = "";
	var synonym_nm = $("#synonym_nm").val();
	var synonym_tag = $("#synonym_tag").val();
	var data_type = "new";
	var input_data = [{"synonym_num" : synonym_num, "synonym_nm" : synonym_nm, "synonym_tag" : synonym_tag, "data_type" : data_type}];
	
	ajax('/submit_synonym', input_data, 'submit_synonym', 'POST');
}

function submit_synonym_callback() {
	alert("전송이 완료되었습니다.");
	window.close();
}
