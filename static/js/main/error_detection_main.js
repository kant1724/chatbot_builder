var grid_data1 = [];
var grid_data2 = [];
var grid_demo_id1 = "myGrid1";
var grid_demo_id2 = "myGrid2";

var dsOption1= {
	fields :[
		{name : 'num'  },
		{name : 'answer_num'  },
		{name : 'question_voca'  }
	],
	recordType : 'array',
	data : grid_data1
}

var dsOption2= {
	fields :[
		{name : 'num'  },
		{name : 'question'  }
	],
	recordType : 'array',
	data : grid_data2
}

var colsOption1 = [
	 {id: 'num' , header: "순번" , width :60 },
	 {id: 'answer_num' , header: "답변번호" , width :120 },
	 {id: 'question_voca' , header: "추출단어" , width :400 }
];

var colsOption2 = [
	 {id: 'num' , header: "순번" , width :60 },
	 {id: 'question' , header: "질문" , width :520 }
];

var gridOption1={
	id : grid_demo_id1,
	width: "600",
	height: "270",
	container : 'answer_num_and_question_voca_grid', 
	replaceContainer : true, 
	dataset : dsOption1 ,
	columns : colsOption1,
	pageSize: 10,
	toolbarContent : 'nav goto | pagesize | reload | print filter chart | state',
	pageSizeList : [10,20,40,80],
	skin : "mac",
	onRowClick:function(value, record, cell, row, colNO, rowNO, columnObj, grid) {
		var answer_num = record[1];
		var question_voca = record[2];
		$("#answer_num").val(answer_num);
		$("#question_voca").val(question_voca);
		
		search_question();
	}
};

var gridOption2={
	id : grid_demo_id2,
	width: "600",
	height: "270",
	container : 'question_grid', 
	replaceContainer : true, 
	dataset : dsOption2 ,
	columns : colsOption2,
	pageSize: 10,
	toolbarContent : 'nav goto | pagesize | reload | print filter chart | state',
	pageSizeList : [10,20,40,80],
	skin : "mac"
};

var mygrid1 = new Sigma.Grid(gridOption1);
var mygrid2 = new Sigma.Grid(gridOption2);
Sigma.Util.onLoad(Sigma.Grid.render(mygrid1));
Sigma.Util.onLoad(Sigma.Grid.render(mygrid2));

$(document).ready(function() {
	$("#search_answer_num_and_question_voca").click(function() {
		search_answer_num_and_question_voca();
	});
	$("#compare_my_question_and_right_question").click(function() {
		compare_my_question_and_right_question();
	});
	$("#subject").keydown(function (key) {
        if (key.keyCode == 13) {
        	search_answer_num_and_question_voca();
        }
    });
	search_answer_num_and_question_voca();
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
        	if (gubun == "search_answer_num_and_question_voca") {
        		search_answer_num_and_question_voca_callback(data['results']);
            } else if (gubun == "compare_my_question_and_right_question") {
            	compare_my_question_and_right_question_callback(data['results']);
            } else if (gubun == "search_question") {
            	search_question_callback(data['results']);
            }
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}

function search_answer_num_and_question_voca() {
	var subject = $("#subject").val();
	var user = $("#user").val();
	var project = $("#project").val();
	var gubun = "1";
	var input_data = {"subject" : subject, "user" : user, "project" : project, "gubun" : gubun};
	ajax('/search_answer_num_and_question_voca', input_data, 'search_answer_num_and_question_voca', 'POST');
}

function search_question() {
	var user = $("#user").val();
	var project = $("#project").val();
	var answer_num = $("#answer_num").val();
	var input_data = {"user" : user, "project" : project, "answer_num" : answer_num};
	ajax('/search_question', input_data, 'search_question', 'POST');
}

function compare_my_question_and_right_question() {
	var subject = "";
	var user = $("#user").val();
	var project = $("#project").val();
	var gubun = "1";
	var base = $("#base").val();
	var my_question = $("#my_question").val();
	var right_question_voca = $("#question_voca").val(); 
	var input_data = {"subject" : subject, "user" : user, "project" : project, "gubun" : gubun, "base" : base, "my_question" : my_question, "right_question_voca" : right_question_voca};
	ajax('/compare_my_question_and_right_question', input_data, 'compare_my_question_and_right_question', 'POST');
}

function search_answer_num_and_question_voca_callback(ret_data) {
	grid_data1 = [];
	for (var i = 0; i < ret_data.length; i++) {
		var a = [];
		a.push(i + 1);
		a.push(ret_data[i]["answer_num"]);
		a.push(ret_data[i]["question_voca"]);
		grid_data1.push(a);
	}
	mygrid1.refresh(grid_data1);
	mygrid1.gotoPage(1);
}

function search_question_callback(ret_data) {
	grid_data2 = [];
	for (var i = 0; i < ret_data.length; ++i) {
		var a = [];
		var question_voca_arr = ret_data[i]['question_voca'].replace(/\^/g, ";").split(";");
		var question = highlight(ret_data[i]['question'], question_voca_arr, "text-highlight");
		a.push(i + 1);
		a.push(question);
		grid_data2.push(a);
	}
	mygrid2.refresh(grid_data2);
	mygrid2.gotoPage(1);
}

function compare_my_question_and_right_question_callback(ret_data) {
	$("#compare_result").html(ret_data);
}
