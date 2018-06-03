$(document).ready(function() {	
	$("#send_training_test_question").click(function() {
		send_training_test_question();
	});
});

function send_training_test_question() {
	var input_data = {"user" : $("#user").val(), "project" : $("#project").val(), "question" : $("#my_question").val()};
	$.post('/send_training_test_question', input_data).done(function(reply) {
		$("#answer").val(reply['answer']);
	}).fail(function() {
	});
}
