$(document).ready(function() {	
	$("#get_action_principle").click(function() {
		get_action_principle();
	});
});

function get_action_principle() {
	if ($("#my_question").val() == '') {
		alert("질문을 입력하세요.");
		return;
	}
	var input_data = {"user" : $("#user").val(), "project" : $("#project").val(), "question" : $("#my_question").val()};
	$.post('/get_action_principle', input_data).done(function(reply) {
		$("#enc_token_words").val(reply['enc_token_words']);
		$("#enc_token_ids").val(reply['enc_token_ids']);
		$("#dec_token_ids").val(reply['dec_token_ids']);
		$("#dec_token_words").val(reply['dec_token_words']);
		$("#answer").val(reply['answer']);
	}).fail(function() {
	});
}
