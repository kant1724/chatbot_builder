$(document).ready(function() {
	$("#voca_synonym").mouseover(function() {
		$('.dropdown-content').hide();
		$('#voca_synonym_dropdown').show();
	});
	$("#data_collection").mouseover(function() {
		$('.dropdown-content').hide();
		$('#data_collection_dropdown').show();
	});
	$(".direct_btn").mouseover(function() {
		$('.dropdown-content').hide();
	});
	$(".info-bar").mouseover(function() {
		$('.dropdown-content').hide();
	});
	$(".div-main").mouseover(function() {
		$('.dropdown-content').hide();
	});
	$("#my_page").click(function() {
		my_page_main();
	});
	$("#qna").click(function() {
		if ($('#qna_main_open_menu').text() == '' && !check_can_open_menu()) return;
		qna_main();
	});
	$("#bucket_manager").click(function() {
		if ($('#bucket_manager_main_open_menu').text() == '' && !check_can_open_menu()) return;
		bucket_manager_main();
	});
	$("#compression_tag").click(function() {
		if ($('#compression_tag_main_open_menu').text() == '' && !check_can_open_menu()) return;
		compression_tag_main();
	});
	$("#notice_manager").click(function() {
		if ($('#notice_manager_main_open_menu').text() == '' && !check_can_open_menu()) return;
		notice_manager_main();
	});
	$("#synonym_manager").click(function() {
		if ($('#synonym_manager_main_open_menu').text() == '' && !check_can_open_menu()) return;
		synonym_manager_main();
	});
	$("#voca_manager").click(function() {
		if ($('#voca_manager_main_open_menu').text() == '' && !check_can_open_menu()) return;
		voca_manager_main();
	});
	$("#category_manager").click(function() {
		if ($('#category_manager_main_open_menu').text() == '' && !check_can_open_menu()) return;
		category_manager_main();
	});
	$("#error_detection").click(function() {
		if ($('#error_detection_main_open_menu').text() == '' && !check_can_open_menu()) return;
		error_detection_main();
	});
	$("#new_request").click(function() {
		if ($('#new_request_main_open_menu').text() == '' && !check_can_open_menu()) return;
		new_request_main();
	});
	$("#error_statistics").click(function() {
		if ($('#error_statistics_main_open_menu').text() == '' && !check_can_open_menu()) return;
		error_statistics_main();
	});
	$("#chatbot_config").click(function() {
		if ($('#chatbot_config_main_open_menu').text() == '' && !check_can_open_menu()) return;
		chatbot_config_main();
	});
	$("#update_question_voca").click(function() {
		if ($('#update_question_voca_main_open_menu').text() == '' && !check_can_open_menu()) return;
		update_question_voca_main();
	});
	$("#hide_testing").click(function() {
		hide_testing();
	});
	$("#run_chatbot").click(function() {
		run_chatbot();
	});
	$("#group_chat").click(function() {
		group_chat_start();
	});
	$("#create_new_room").click(function() {
		var room_name = $('#chat_room_name').val();
		var room_password = $('#chat_room_password').val();
		create_new_room(room_name, room_password);
	});
	$("#enter_room").click(function() {
		var room_name = $('#chat_room_name').val();
		var room_password = $('#chat_room_password').val();
		enter_room(room_name, room_password);
	});
	$("#action_principle").click(function() {
		action_principle();
	});
	left_window();
	qna_main();
	training_test_main();
});

function left_window() {
	var user = $("#user").val();
	var project = $("#project").val();
	$('.left-content').append('<iframe class="content" id="train_main" frameBorder="0" src="/train_main?user=' + user + '&project=' + project + '"></iframe>');
}

var current_window = null;

function run_chatbot() {
	var user = $("#user").val();
	var project = $("#project").val();
	$.post("/get_is_training", {
			user : user,
			project : project
		}).done(function(reply) {
			if (reply['is_training'] == 'Y') {
				alert("훈련을 중단 후 실행해 주세요.");
				return;
			} else {
				var w = RUN_CHAT_POPUP_WIDTH;
				var h = RUN_CHAT_POPUP_HEIGHT;
				var x = (screen.width - w) / 2;
			    var y = (screen.height - h) / 3;
				if (current_window != null) {
					current_window.close();
				}
				current_window = window.open('', 'loading_page', 'scrollbars=yes, resizable=yes, width=' + w + ', height=' + h + ', left=' + x + ', top=' + y);
				$("#gubun").val('1');
				$("#loading").submit();
			}
		}).fail(function() {
	});
}

function group_chat(room_name, room_password) {
	var w = GROUP_CHAT_POPUP_WIDTH;
	var h = GROUP_CHAT_POPUP_HEIGHT;
	var x = (screen.width - w) / 2;
    var y = (screen.height - h) / 3;
	if (current_window != null) {
    	current_window.close();
    }
	$('#room_name').val(room_name);
    current_window = window.open('', 'loading_page', 'scrollbars=yes, resizable=yes, width=' + w + ', height=' + h + ', left=' + x + ', top=' + y);
	$("#gubun").val('2');
	$("#loading").submit();
}

function group_chat_start() {
	var user = $("#user").val();
	var project = $("#project").val();
	$.post("/get_is_training", {
		user : user,
		project : project
	}).done(function(reply) {
		if (reply['is_training'] == 'Y') {
			alert("훈련을 중단 후 실행해 주세요.");
			return;
		} else {
			$('#create_chat').modal({});
		}
	}).fail(function() {
	});
}

function create_new_room(room_name, room_password) {
	$.post("/create_new_chat_room", {
		emno : $('#emno').val(),
		room_name : room_name,
		room_password : room_password
	}).done(function(reply) {
		if (reply['already'] == 'Y') {
			alert("동일한 대화방명이 이미 존재합니다.");
			return;
		} else {
			$('#modal_close').click();
			group_chat(room_name, room_password);
		}
	}).fail(function() {
	});
}

function enter_room(room_name, room_password) {
	$.post("/enter_chat_room", {
		emno : $('#emno').val(),
		room_name : room_name,
		room_password : room_password
	}).done(function(reply) {
		if (reply['has_room_name'] == 'N') {
			alert("해당 대화방이 존재하지 않습니다.");
			return;
		} else if (reply['right_password'] == 'N') {
			alert("패스워드가 잘못되었습니다.");
			return;
		} else {
			$('#modal_close').click();
			group_chat(room_name, room_password);
		}
	}).fail(function() {
	});
}

function action_principle() {
	var user = $("#user").val();
	var project = $("#project").val();
	$.post("/get_is_training", { user : user, project : project}).done(function(reply) {
		if (reply['is_training'] == 'Y') {
			alert("훈련을 중단 후 실행해 주세요.");
			return;
		} else {
			var w = ACTION_PRINCIPLE_POPUP_WIDTH;
			var h = ACTION_PRINCIPLE_POPUP_HEIGHT;
			var x = (screen.width - w) / 2;
		    var y = (screen.height - h) / 3;
		    if (current_window != null) {
		    	current_window.close();
		    }
		    current_window = window.open('', 'loading_page', 'scrollbars=yes, width=' + w + ', height=' + h + ', left=' + x + ', top=' + y);
			$("#gubun").val('3');
			$("#loading").submit();
		}
	}).fail(function() {
	});
}

function hide_all() {
	$('.div-main').children().hide();
	$('.topnav').children().attr('class', '');
}

function check_can_open_menu() {
	if ($('.open-menu').size() + $('.open-menu-active').size() >= 7) {
		alert("7개이상 메뉴를 동시에 열 수 없습니다.\n다른메뉴를 닫고 다시 열어 주세요.");
		return false;
	}
	return true;
}

function add_open_menu(id, id_x_mark, iframe_id, text) {
	var first_id = $('.info-bar').find("div[class*='open-menu']").first().prop('id');
	var ele = $('<div id="' + id + '" class="open-menu"><span>' + text + '</span><span id="' + id_x_mark + '" class="x-mark">&#x2715;</span></div>');
	if (first_id == null) {
		ele.appendTo('.info-bar');
	} else {
		ele.insertBefore('#' + first_id);
	}
	$("#" + id).click(function() {
		eval(iframe_id + "()");
	});
	$("#" + id).dblclick(function() {
		$("#" + id).remove();
		$("#" + iframe_id).remove();
	});
	$("#" + id_x_mark).click(function() {
		$("#" + id).remove();
		$("#" + iframe_id).remove();
	});
}

function my_page_main() {
	var user = $("#user").val();
	var project = $("#project").val();
	var emno = $("#emno").val();
	$('.menu-name').text('> ' + $('#my_page').text());
	hide_all();
	$('.div-main').append('<iframe class="content" id="my_page_main" frameBorder="0" src="/my_page_main?user=' + user + '&project=' + project + '&emno=' + emno + '"></iframe>');
	$("#my_page").attr('class', 'active');
}

function qna_main() {
	var user = $("#user").val();
	var project = $("#project").val();
	$('.menu-name').text('> ' + $('#qna').text());
	if ($('#qna_main').length == 0) { 
		hide_all();
		$('.div-main').append('<iframe class="content" id="qna_main" frameBorder="0" src="/qna_main?user=' + user + '&project=' + project + '"></iframe>');
		add_open_menu('qna_main_open_menu', 'qna_main_open_menu_x_mark', 'qna_main', $('#qna').text());
	} else {
		hide_all();
		$("#qna_main").show();
	}
	$('.info-bar').find('.open-menu-active').first().attr('class', 'open-menu');
	$("#qna_main_open_menu").attr('class', 'open-menu-active');
	$("#qna").attr('class', 'active');
}

function bucket_manager_main() {
	var user = $("#user").val();
	var project = $("#project").val();
	$('.menu-name').text('> ' + $('#bucket_manager').text());
	if ($('#bucket_manager_main').length == 0) {
		hide_all();
		$('.div-main').append('<iframe class="content" id="bucket_manager_main" frameBorder="0" src="/bucket_manager_main?user=' + user + '&project=' + project + '"></iframe>');
		add_open_menu('bucket_manager_main_open_menu', 'bucket_manager_main_open_menu_x_mark', 'bucket_manager_main', $('#bucket_manager').text());
	} else {
		hide_all();
		$("#bucket_manager_main").show();
	}
	$('.info-bar').find('.open-menu-active').first().attr('class', 'open-menu');
	$("#bucket_manager_main_open_menu").attr('class', 'open-menu-active');
	$("#bucket_manager").attr('class', 'active');
}

function compression_tag_main() {
	var user = $("#user").val();
	var project = $("#project").val();
	$('.menu-name').text('> ' + $('#compression_tag').text());
	if ($('#compression_tag_main').length == 0) {
		hide_all();
		$('.div-main').append('<iframe class="content" id="compression_tag_main" frameBorder="0" src="/compression_tag_main?user=' + user + '&project=' + project + '"></iframe>');
		add_open_menu('compression_tag_main_open_menu', 'compression_tag_main_open_menu_x_mark', 'compression_tag_main', $('#compression_tag').text());
	} else {
		hide_all();
		$("#compression_tag_main").show();
	}
	$('.info-bar').find('.open-menu-active').first().attr('class', 'open-menu');
	$("#compression_tag_main_open_menu").attr('class', 'open-menu-active');
	$("#compression_tag").attr('class', 'active');
}

function notice_manager_main() {
	var user = $("#user").val();
	var project = $("#project").val();
	$('.menu-name').text('> ' + $('#notice_manager').text());
	if ($('#notice_manager_main').length == 0) {
		hide_all();
		$('.div-main').append('<iframe class="content" id="notice_manager_main" frameBorder="0" src="/notice_manager_main?user=' + user + '&project=' + project + '"></iframe>');
		add_open_menu('notice_manager_main_open_menu', 'notice_manager_main_open_menu_x_mark', 'notice_manager_main', $('#notice_manager').text());
	} else {
		hide_all();
		$("#notice_manager_main").show();
	}
	$('.info-bar').find('.open-menu-active').first().attr('class', 'open-menu');
	$("#notice_manager_main_open_menu").attr('class', 'open-menu-active');
	$("#notice_manager").attr('class', 'active');
}

function update_question_voca_main() {
	var user = $("#user").val();
	var project = $("#project").val();
	$('.menu-name').text('> ' + $('#update_question_voca').text());
	if ($('#update_question_voca_main').length == 0) {
		hide_all();
		$('.div-main').append('<iframe class="content" id="update_question_voca_main" frameBorder="0" src="/update_question_voca_main?user=' + user + '&project=' + project + '"></iframe>');
		add_open_menu('update_question_voca_main_open_menu', 'update_question_voca_main_open_menu_x_mark', 'update_question_voca_main', $('#update_question_voca').text());
	} else {
		hide_all();
		$("#update_question_voca_main").show();
	}
	$('.info-bar').find('.open-menu-active').first().attr('class', 'open-menu');
	$("#update_question_voca_main_open_menu").attr('class', 'open-menu-active');
	$("#voca_synonym").attr('class', 'active');
}

function synonym_manager_main() {
	var user = $("#user").val();
	var project = $("#project").val();
	$('.menu-name').text('> ' + $('#synonym_manager').text());
	if ($('#synonym_manager_main').length == 0) {
		hide_all();
		$('.div-main').append('<iframe class="content" id="synonym_manager_main" frameBorder="0" src="/synonym_manager_main?user=' + user + '&project=' + project + '"></iframe>');
		add_open_menu('synonym_manager_main_open_menu', 'synonym_manager_main_open_menu_x_mark', 'synonym_manager_main', $('#synonym_manager').text());
	} else {
		hide_all();
		$("#synonym_manager_main").show();
	}
	$('.info-bar').find('.open-menu-active').first().attr('class', 'open-menu');
	$("#synonym_manager_main_open_menu").attr('class', 'open-menu-active');
	$("#voca_synonym").attr('class', 'active');
}

function voca_manager_main() {
	var user = $("#user").val();
	var project = $("#project").val();
	$('.menu-name').text('> ' + $('#voca_manager').text());
	if ($('#voca_manager_main').length == 0) {
		hide_all();
		$('.div-main').append('<iframe class="content" id="voca_manager_main" frameBorder="0" src="/voca_manager_main?user=' + user + '&project=' + project + '"></iframe>');
		add_open_menu('voca_manager_main_open_menu', 'voca_manager_main_open_menu_x_mark', 'voca_manager_main', $('#voca_manager').text());
	} else {
		hide_all();
		$("#voca_manager_main").show();
	}
	$('.info-bar').find('.open-menu-active').first().attr('class', 'open-menu');
	$("#voca_manager_main_open_menu").attr('class', 'open-menu-active');
	$("#voca_synonym").attr('class', 'active');
}

function category_manager_main() {
	var user = $("#user").val();
	var project = $("#project").val();
	$('.menu-name').text('> ' + $('#category_manager').text());
	if ($('#category_manager_main').length == 0) {
		hide_all();
		$('.div-main').append('<iframe class="content" id="category_manager_main" frameBorder="0" src="/category_manager_main?user=' + user + '&project=' + project + '"></iframe>');
		add_open_menu('category_manager_main_open_menu', 'category_manager_main_open_menu_x_mark', 'category_manager_main', $('#category_manager').text());
	} else {
		hide_all();
		$("#category_manager_main").show();
	}
	$('.info-bar').find('.open-menu-active').first().attr('class', 'open-menu');
	$("#category_manager_main_open_menu").attr('class', 'open-menu-active');
	$("#category_manager").attr('class', 'active');
}

function error_detection_main() {
	var user = $("#user").val();
	var project = $("#project").val();
	$('.menu-name').text('> ' + $('#error_detection').text());
	if ($('#error_detection_main').length == 0) {
		hide_all();
		$('.div-main').append('<iframe class="content" id="error_detection_main" frameBorder="0" src="/error_detection_main?user=' + user + '&project=' + project + '"></iframe>');
		add_open_menu('error_detection_main_open_menu', 'error_detection_main_open_menu_x_mark', 'error_detection_main', $('#error_detection').text());
	} else {
		hide_all();
		$("#error_detection_main").show();
	}
	$('.info-bar').find('.open-menu-active').first().attr('class', 'open-menu');
	$("#error_detection_main_open_menu").attr('class', 'open-menu-active');
	$("#error_detection").attr('class', 'active');
}

function new_request_main() {
	var user = $("#user").val();
	var project = $("#project").val();
	$('.menu-name').text('> ' + $('#new_request').text());
	if ($('#new_request_main').length == 0) {
		hide_all();
		$('.div-main').append('<iframe class="content" id="new_request_main" frameBorder="0" src="/new_request_main?user=' + user + '&project=' + project + '"></iframe>');
		add_open_menu('new_request_main_open_menu', 'new_request_main_open_menu_x_mark', 'new_request_main', $('#new_request').text());
	} else {
		hide_all();
		$("#new_request_main").show();
	}
	$('.info-bar').find('.open-menu-active').first().attr('class', 'open-menu');
	$("#new_request_main_open_menu").attr('class', 'open-menu-active');
	$("#data_collection").attr('class', 'active');
}

function error_statistics_main() {
	var user = $("#user").val();
	var project = $("#project").val();
	$('.menu-name').text('> ' + $('#error_statistics').text());
	if ($('#error_statistics_main').length == 0) {
		hide_all();
		$('.div-main').append('<iframe class="content" id="error_statistics_main" frameBorder="0" src="/error_statistics_main?user=' + user + '&project=' + project + '"></iframe>');
		add_open_menu('error_statistics_main_open_menu', 'error_statistics_main_open_menu_x_mark', 'error_statistics_main', $('#error_statistics').text());
	} else {
		hide_all();
		$("#error_statistics_main").show();
	}
	$('.info-bar').find('.open-menu-active').first().attr('class', 'open-menu');
	$("#error_statistics_main_open_menu").attr('class', 'open-menu-active');
	$("#data_collection").attr('class', 'active');
}

function chatbot_config_main() {
	var user = $("#user").val();
	var project = $("#project").val();
	$('.menu-name').text('> ' + $('#chatbot_config').text());
	if ($('#chatbot_config_main').length == 0) {
		hide_all();
		$('.div-main').append('<iframe class="content" id="chatbot_config_main" frameBorder="0" src="/chatbot_config_main?user=' + user + '&project=' + project + '"></iframe>');
		add_open_menu('chatbot_config_main_open_menu', 'chatbot_config_main_open_menu_x_mark', 'chatbot_config_main', $('#chatbot_config').text());
	} else {
		hide_all();
		$("#chatbot_config_main").show();
	}
	$('.info-bar').find('.open-menu-active').first().attr('class', 'open-menu');
	$("#chatbot_config_main_open_menu").attr('class', 'open-menu-active');
	$("#chatbot_config").attr('class', 'active');
}

function hide_testing() {
	$('.bottom-nav').children().hide();
	$('.bottom-nav').hide(1000);
}

function training_test_main() {
	var user = $("#user").val();
	var project = $("#project").val();
	$('.div-bottom').append('<iframe class="bottom-content" id="training_test_main" frameBorder="0" src="/training_test_main?user=' + user + '&project=' + project + '"></iframe>');
}
