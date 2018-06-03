$(document).ready(function() {
	if ($('#logout').val() == 'N') {
		if (confirm("자동 로그인 하시겠습니까?")) {
			$('#user').val('chatbot_tft');
			$('#password').val('1111');
			$('#project').val('fund');
			login();
			return;
		}
	}
	$("#login").click(function() {
		login();
	});
	$(window).on('keydown', function(e) {
		if (e.which == 13) {
			login();
		}
	});
});

function login() {
	$.post('/login_try', {
			user : $('#user').val().toLowerCase(),
			password : $('#password').val(),
			project : $('#project').val().toLowerCase()
		}).done(function(reply) {
			if (reply['success'] == 'N') {
				$("#msg").text(reply['msg']);				
			} else {
				var user = $('#user').val().toLowerCase();
				var project = $('#project').val().toLowerCase();
				var emno = reply['emno']; 
				if ($('#run_chat').val() == 'Y') {
					var w = RUN_CHAT_POPUP_WIDTH;
					var h = RUN_CHAT_POPUP_HEIGHT;
					var x = (screen.width - w) / 2;
				    var y = (screen.height - h) / 3;
				    window.open('', 'loading_page', 'scrollbars=yes, resizable=yes, width=' + w + ', height=' + h + ', left=' + x + ', top=' + y);
				    $('#chat_user').val(user);
				    $('#chat_project').val(project);
				    $("#gubun").val('1');
					$("#loading").submit();
				} else {
					var w = QNA_MAIN_POPUP_WIDTH;
					var h = QNA_MAIN_POPUP_HEIGHT;
					var y = window.top.outerHeight / 2 + window.top.screenY - ( h / 2) - 50;
					var x = window.top.outerWidth / 2 + window.top.screenX - ( w / 2);
					var strWindowFeatures = 'location=no ,height='+h+',width='+w+',left='+x+',top='+y+',scrollbars=yes, menubar=no, status=no, toolbar=no, titlebar=no';
					var pop = window.open('/frame?user=' + user + '&project=' + project + '&emno=' + emno, '_blank', strWindowFeatures);
					if (pop == null) {
						return;
					}
				}
				var success = window.open('/login_success?user=' + user + '&project=' + project, '_self', '');
				success.close();
			}
		}).fail(function() {
				});
}
