var grid_data1 = [];
var grid_demo_id1 = "myGrid1";

var dsOption1= {
	fields :[
		{name : 'num'  },
		{name : 'question' },
		{name : 'answer' }
	],
	recordType : 'array',
	data : grid_data1
}

var colsOption1 = [
	 {id: 'num' , header: "순번" , width :60 },
	 {id: 'question' , header: "질문" , width :300 },
	 {id: 'answer' , header: "답변" , width :300 },
];

var gridOption1={
	id : grid_demo_id1,
	width: "680",
	height: "250",
	container : 'multiple_answer_grid', 
	replaceContainer : true, 
	dataset : dsOption1 ,
	columns : colsOption1,
	pageSize: 20000,
	remoteSort: true,
	toolbarContent : 'nav goto | pagesize | reload | print filter chart | state',
	pageSizeList : [20000],
	skin : "mac",
	onRowClick:function(value, record, cell, row, colNO, rowNO, columnObj, grid) {
		var num = record[0];
		var question = record[1];
		var answer = record[2];
		$("#num").val(num);
		$("#question_input").val(question);
		$("#answer_input").val(answer);
	}
};

var mygrid1 = new Sigma.Grid(gridOption1);
Sigma.Util.onLoad(Sigma.Grid.render(mygrid1));

$(document).ready(function() {
	$("#add_row").click(function() {
		add_row();
	});
	$("#del_row").click(function() {
		del_row();
	});
	$("#submit_multiple_answer").click(function() {
		submit_multiple_answer();
	});
	$("#question_input").on('input', function() {
		change_question();
	});
	$("#answer_input").on('input', function() {
		change_answer();
	});
	search_multiple_answer();
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
        	if (gubun == "search_multiple_answer") {
        		search_multiple_answer_callback(data['results']);
        	} else if (gubun == "submit_multiple_answer") {
        		submit_multiple_answer_callback();
            }
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}

function search_multiple_answer() {
	var user = $("#user").val();
	var project = $("#project").val();
	var answer_num = $("#answer_num").val();
	input_data = {"user" : user, "project" : project, "answer_num" : answer_num};

	ajax('/search_multiple_answer', input_data, 'search_multiple_answer', 'POST');
}

function submit_multiple_answer() {
	if (!confirm("전송 하시겠습니까?")) {
		return;
	}
	var input_data = [];
	var user = $("#user").val();
	var project = $("#project").val();
	var answer_num = $("#answer_num").val();
	for (var i = 0; i < grid_data1.length; ++i) {
		var question = grid_data1[i][1];
		var answer = grid_data1[i][2];
		input_data.push({"user" : user, "project" : project, "question" : question, "answer" : answer, "answer_num" : answer_num});
	}
	if (input_data.length == 0) {
		input_data.push({"user" : user, "project" : project, "question" : "", "answer" : "", "answer_num" : answer_num});
	}
	ajax('/submit_multiple_answer', input_data, 'submit_multiple_answer', 'POST');
}

function search_multiple_answer_callback(ret_data) {
	grid_data1 = [];
	for (var i = 0; i < ret_data.length; i++) {
		var a = [];
		a.push(i + 1);
		a.push(ret_data[i]["question"]);
		a.push(ret_data[i]["answer"]);
		grid_data1.push(a);
	}
	mygrid1.refresh(grid_data1);
	mygrid1.gotoPage(1);
}

function submit_multiple_answer_callback() {
	alert("전송이 완료되었습니다.");
}

function add_row() {
	var a = [];
	a.push(grid_data1.length + 1);
	a.push('');
	a.push('');
	grid_data1.push(a);
	mygrid1.refresh(grid_data1);
}

function del_row() {
	var num = $("#num").val();
	for (var i = 0; i < grid_data1.length; ++i) {
		if (grid_data1[i][0] == num) {
			grid_data1.splice(i, 1);
			break;
		}
	}
	for (var i = 0; i < grid_data1.length; ++i) {
		grid_data1[i][0] = i + 1;
	}
	mygrid1.refresh(grid_data1);
}

function change_question() {
	var num = $("#num").val();
	for (var i = 0; i < grid_data1.length; ++i) {
		if (grid_data1[i][0] == num) {
			grid_data1[i][1] = $("#question_input").val();
			break;
		}
	}
	mygrid1.refresh(grid_data1);
}

function change_answer() {
	var num = $("#num").val();
	for (var i = 0; i < grid_data1.length; ++i) {
		if (grid_data1[i][0] == num) {
			grid_data1[i][2] = $("#answer_input").val();
			break;
		}
	}
	mygrid1.refresh(grid_data1);
}
