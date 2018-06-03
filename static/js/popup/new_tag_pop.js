$(document).ready(function() {
	$("#submit_tag").click(function() {
		submit_tag();
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
        	if (gubun == "submit_tag") {
        		submit_tag_callback();
            } 
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}

function submit_tag() {
	var tag_nm = $("#tag_nm").val();
	var kor_nm = $("#kor_nm").val();
	var gubun = $("#gubun option:selected").val();
	if (tag_nm == '') {
		alert("태그명을 선택 하세요.");
		return;
	} else if (kor_nm == '') {
		alert("한글명을 선택 하세요.");
		return;
	} else if (gubun == '') {
		alert("구분을 선택 하세요.");
		return;
	}
	
	if (!confirm("전송 하시겠습니까?")) {
		return;
	}

	var input_data = {"tag_nm" : tag_nm, "kor_nm" : kor_nm, "gubun" : gubun};
	
	ajax('/submit_tag', input_data, 'submit_tag', 'POST');
}

function submit_tag_callback() {
	alert("전송이 완료되었습니다.");
	$("#tag_nm").val('');
	$("#kor_nm").val('');
}
