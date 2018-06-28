$(document).ready(function() {
	$('#add_image').click(function() {
		add_image();
	});
	$('#modify_image').click(function() {
		modify_image();
	});
	$('#delete_image').click(function() {
		delete_image();
	});
	$("#image_file").change(function() {
		if ($('#image_file').val() != '') {
			if ($('#gubun').val() == 'add') { 
				image_cnt++;
			}
			update_image_cnt();
		}
	});
	get_all_image_list();
});

var image_cnt = 0;
function add_image() {
	$('#gubun').val('add');
	$('#image_file').click();
}

function modify_image() {
	$('#gubun').val('modify');
	$('#image_file').click();
}

function delete_image() {
	if (!confirm("해당 이미지를 삭제 하시겠습니까?")) {
		return;
	}
	$('#gubun').val('delete');
	image_cnt--;
	update_image_cnt();
}

function update_image_cnt() {
	$('#image_cnt').val(image_cnt);
	var url = '/submit_image';
	var form = document.querySelector('#send_file_form');
	var form_data = new FormData(form);
	ajax(url, form_data, '1');
}

function upload_to_file_server(data) {
	var file_ip = $('#file_ip').val();
	var url = "http://" + file_ip + "/upload_file";
	var image_path = data['image_path'];
	$('#image_path').val(image_path);
	var image_file_name = '';
	if ($('#gubun').val() == 'add') {
		image_file_name = 'image' + image_cnt;
	} else {
		image_file_name = 'image' + $('.slidesjs-pagination-item .active').text();
	}
	$('#image_file_name').val(image_file_name);
	$('#image_file').attr('name', image_file_name);
	var form = document.querySelector('#send_file_form');
	var form_data = new FormData(form);
	ajax(url, form_data, '2');
}

function delete_image_file(data) {
	var file_ip = $('#file_ip').val();
	var url = "http://" + file_ip + "/delete_image_file";
	var image_path = data['image_path'];
	$('#image_path').val(image_path);
	var image_file_name = 'image' + $('.slidesjs-pagination-item .active').text();
	$('#image_file_name').val(image_file_name);
	$('#image_file').attr('name', image_file_name);
	var form = document.querySelector('#send_file_form');
	var form_data = new FormData(form);
	
	ajax(url, form_data, '4');
}

function get_all_image_list() {
	var url = "http://" + $('#file_ip').val() + "/get_all_image_list";
	var form = document.querySelector('#send_file_form');
	var form_data = new FormData(form);
	ajax(url, form_data, '3');
}

function load_all_images(data) {
	var image_list = eval(data);
	image_cnt = image_list.length;
	var root = "http://" + $('#file_ip').val() + "/";
	$('.container').empty();
	$('<div id="slides"></div>').appendTo($('.container'));
	for (var i = 0; i < image_list.length; ++i) {
		var addr = root + image_list[i] + "?timestamp=" + new Date().getTime();
		$('<img src="' + addr + '">').appendTo($('#slides'));
	}
	$('#slides').slidesjs({});
}

function ajax(url, form_data, gubun) {
	$.ajax({
		url: url,
		type: 'POST',
		data: form_data,
		async: false,
		cache: false,
		contentType: false,
		processData: false,
		success: function(data) {
			if (gubun == '1') {
				if ($('#gubun').val() == 'delete') {
					delete_image_file(data);
				} else {
					upload_to_file_server(data);
				}
			} else if (gubun == '2') {
				$('#image_file').val('');
				get_all_image_list();
			} else if (gubun == '3') {
				load_all_images(data);
			} else if (gubun == '4') {
				get_all_image_list();
			}
		}
    });
}
