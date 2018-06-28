$(document).ready(function() {
	$("#submit_training_config").click(function() {
		submit_training_config();
		submit_chatbot_config();
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
        	if (gubun == "search_training_config") {
        		search_training_config_callback(data['results']);
        	} else if (gubun == "search_chatbot_config") {
        		search_chatbot_config_callback(data['results']);
        	} else if (gubun == "submit_training_config") {
        		submit_training_config_callback();
            } 
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}

function submit_training_config() {
	grid1.navigateDown();
	var user = $("#user").val();
	var project = $("#project").val();
	var input_data = [];
	for (var i = 0; i < data1.length; ++i) {
		var d = {};
		d['user'] = user;
		d['project'] = project;
		d['config_name'] = data1[i]['config_name'];
		d['config_value'] = data1[i]['config_value'];
		input_data.push(d);
	}
	ajax('/submit_training_config', input_data, 'submit_training_config', 'POST');
}

function submit_chatbot_config() {
	grid2.navigateDown();
	var user = $("#user").val();
	var project = $("#project").val();
	var input_data = [];
	for (var i = 0; i < data2.length; ++i) {
		var d = {};
		d['user'] = user;
		d['project'] = project;
		d['config_name'] = data2[i]['config_name'];
		d['config_value'] = data2[i]['config_value'];
		input_data.push(d);
	}
	ajax('/submit_chatbot_config', input_data, 'submit_chatbot_config', 'POST');
}

function submit_training_config_callback() {
	alert("전송이 완료되었습니다.");
}

function submit_chatbot_config_callback() {
	alert("전송이 완료되었습니다.");
}

function search_training_config() {
	var user = $("#user").val();
	var project = $("#project").val();
	var input_data = {"user" : user, "project" : project};
	ajax('/search_training_config', input_data, 'search_training_config', 'POST');
}

function search_chatbot_config() {
	var user = $("#user").val();
	var project = $("#project").val();
	var input_data = {"user" : user, "project" : project};
	ajax('/search_chatbot_config', input_data, 'search_chatbot_config', 'POST');
}

function search_training_config_callback(ret_data) {
	data1 = [];
	for (var i = 0; i < ret_data.length; i++) {
		var d = {};
		d["id"]= "id_" + (i + 1);
		d["num"]= i + 1;
		d["config_name"] = ret_data[i]['config_name'];
		d["config_value"] = ret_data[i]['config_value'];
		data1.push(d);
	}
	grid1.resetActiveCell();
	grid1.setData(data1);	
	grid1.render();
}

function search_chatbot_config_callback(ret_data) {
	data2 = [];
	for (var i = 0; i < ret_data.length; i++) {
		var d = {};
		d["id"]= "id_" + (i + 1);
		d["num"]= i + 1;
		d["config_name"] = ret_data[i]['config_name'];
		d["config_value"] = ret_data[i]['config_value'];
		data2.push(d);
	}
	grid2.resetActiveCell();
	grid2.setData(data2);	
	grid2.render();
}

var grid1;
var grid2;
var data1 = [];
var data2 = [];
var columns1 = [
	{id: "num", name: "순번", field: "num", behavior: "select", cssClass: "cell-selection", width: 40, cannotTriggerInsert: true, resizable: false, selectable: false},
	{id: "config_name", name: "설정명", field: "config_name", width: 450, cssClass: "cell-title", resizable: true, selectable: false},
	{id: "config_value", name: "설정값", field: "config_value", width: 100, cssClass: "cell-title", editor: Slick.Editors.Text, resizable: true}
];

var columns2 = [
	{id: "num", name: "순번", field: "num", behavior: "select", cssClass: "cell-selection", width: 40, cannotTriggerInsert: true, resizable: false, selectable: false},
	{id: "config_name", name: "설정명", field: "config_name", width: 450, cssClass: "cell-title", resizable: true, selectable: false},
	{id: "config_value", name: "설정값", field: "config_value", width: 100, cssClass: "cell-title", editor: Slick.Editors.Text, resizable: true}
];

var options1 = {
	editable: true,
	enableAddRow: false,
	enableCellNavigation: true,
	asyncEditorLoading: false
};

var options2 = {
	editable: true,
	enableAddRow: false,
	enableCellNavigation: true,
	asyncEditorLoading: false
};

$(function () {
	grid1 = new Slick.Grid("#training_config_grid", data1, columns1, options1);
	grid1.setSelectionModel(new Slick.RowSelectionModel());
	grid2 = new Slick.Grid("#chatbot_config_grid", data2, columns2, options2);
	grid2.setSelectionModel(new Slick.RowSelectionModel());
	search_training_config();
	search_chatbot_config();
});
