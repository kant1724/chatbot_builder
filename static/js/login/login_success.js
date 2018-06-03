$(document).ready(function() {
	$("#logout").click(function() {
		logout();
	});
});

function logout() {
	var user = $('#user').val();
	var project = $('#project').val();
	window.location.href = '/logout?user=' + user + '&project=' + project;
}
