var grid_data1 = [];
var grid_data2 = [];
var grid_data3 = [];
var grid_demo_id1 = "myGrid1";
var grid_demo_id2 = "myGrid2";
var grid_demo_id3 = "myGrid3";

var dsOption1= {
	fields :[
		{name : 'question'  },
		{name : 'answer_num'  },
		{name : 'rgsn_date'  },
		{name : 'rgsn_time'  }
	],
	recordType : 'array',
	data : grid_data1
}

var dsOption2= {
	fields :[
		{name : 'rpsn_question'  },
		{name : 'answer'  },
		{name : 'answer_num'  },
	],
	recordType : 'array',
	data : grid_data2
}

var dsOption3= {
	fields :[
		{name : 'num'  },
		{name : 'answer_num'  },
		{name : 'question'  }
	],
	recordType : 'array',
	data : grid_data3
}

var colsOption1 = [
	 {id: 'chk' ,isCheckColumn : true}, 
	 {id: 'question' , header: "요청질문" , width :530 },
	 {id: 'answer_num' , header: "답변번호" , width :80 },
	 {id: 'rgsn_date' , header: "등록일자" , width :120 },
	 {id: 'rgsn_time' , header: "등록시간" , width :120 },
];

var colsOption2 = [
     {id: 'chk' ,isCheckColumn : true}, 
	 {id: 'rpsn_question' , header: "대표질문" , width :370 },
	 {id: 'answer' , header: "답변" , width :400 },
	 {id: 'answer_num' , header: "답변번호" , width :80 }
];

var colsOption3 = [
	 {id: 'num' , header: "순번" , width :60 }, 
	 {id: 'answer_num' , header: "답변번호" , width :80 },
	 {id: 'question' , header: "질문" , width :750 }
];

var gridOption1={
	id : grid_demo_id1,
	width: "900",
	height: "226",
	container : 'wrong_answer_grid', 
	replaceContainer : true, 
	dataset : dsOption1 ,
	columns : colsOption1,
	pageSize: 8,
	toolbarContent : 'nav goto | pagesize | reload | print filter chart | state',
	pageSizeList : [8,20,40,80,100],
	skin : "mac",
	onRowClick:function(value, record, cell, row, colNO, rowNO, columnObj, grid) {
	},
	onCellDblClick:function(value,  record,  cell,  row,  colNo,  columnObj,  grid) {
		if (colNo == 2) {
			search_answer_by_answer_num(record[1]);
		} else {
			var voca = getSelectedText().trim();
			if (voca != '') {
				$('#answer_subject').val(voca);
				search_answer();
			}
		}
	}
};

var gridOption2={
	id : grid_demo_id2,
	width: "900",
	height: "226",
	container : 'answer_list_grid', 
	replaceContainer : true, 
	dataset : dsOption2 ,
	columns : colsOption2,
	pageSize: 8,
	toolbarContent : 'nav goto | pagesize | reload | print filter chart | state',
	pageSizeList : [8,20,40,80,100],
	skin : "mac",
	onRowClick:function(value, record, cell, row, colNO, rowNO, columnObj, grid) {
		var answer_num = record[2];
		$("#answer_num").val(answer_num);
		search_question();
	}
};

var gridOption3={
	id : grid_demo_id3,
	width: "900",
	height: "204",
	container : 'question_list_grid', 
	replaceContainer : true, 
	dataset : dsOption3 ,
	columns : colsOption3,
	pageSize: 7,
	toolbarContent : 'nav goto | pagesize | reload | print filter chart | state',
	pageSizeList : [7,15,30,60,100],
	skin : "mac",
	onRowClick:function(value, record, cell, row, colNO, rowNO, columnObj, grid) {
	}
};

var mygrid1 = new Sigma.Grid(gridOption1);
var mygrid2 = new Sigma.Grid(gridOption2);
var mygrid3 = new Sigma.Grid(gridOption3);
Sigma.Util.onLoad(Sigma.Grid.render(mygrid1));
Sigma.Util.onLoad(Sigma.Grid.render(mygrid2));
Sigma.Util.onLoad(Sigma.Grid.render(mygrid3));

$(document).ready(function() {
	$("#search_wrong_answer").click(function() {
		search_wrong_answer();
	});
	$("#search_answer").click(function() {
		search_answer();
	});
	$("#mapping_new_question_answer").click(function() {
		mapping_new_question_answer();
	});
	$("#wrong_answer_subject").keydown(function (key) {
        if (key.keyCode == 13) {
        	search_wrong_answer();
        }
    });
	$("#answer_subject").keydown(function (key) {
        if (key.keyCode == 13) {
        	search_answer();
        }
    });	
	search_wrong_answer();
	search_answer();
});

function drop_answer_subject(e) {
	e.preventDefault();
	var text = event.dataTransfer.getData("Text");
	$('#answer_subject').val(text);
	search_answer();	
}

function ajax(url, input_data, gubun, method) {
	$.ajax(url, {
		type: method, 
        data: JSON.stringify(input_data),
        async: false,
        contentType: 'application/json',
        dataType: 'json',
        processData: false,
        success: function (data, status, xhr) {
        	if (gubun == "search_wrong_answer") {
        		search_wrong_answer_callback(data);
            } else if (gubun == "search_answer") {
            	search_answer_callback(data);
            } else if (gubun == "search_question") {
            	search_question_callback(data);
            } else if (gubun == "submit_question") {
            	submit_question_callback();
            }
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}

function search_wrong_answer() {
	var subject = $("#wrong_answer_subject").val();
	var user = $("#user").val();
	var project = $("#project").val();
	var input_data = {"subject" : subject, "user" : user, "project" : project};
	ajax('/search_wrong_answer', input_data, 'search_wrong_answer', 'POST');
}

function search_wrong_answer_callback(retData) {
	grid_data1 = [];
	var retList = retData['results'];
	for (var i = 0; i < retList.length; ++i) {
		var a = [];
		a.push(retList[i]['question']);
		a.push(retList[i]['answer_num']);
		a.push(retList[i]['rgsn_date']);
		a.push(retList[i]['rgsn_time']);
		grid_data1.push(a);
	}
	mygrid1.refresh(grid_data1);
	mygrid1.gotoPage(1);
}

function search_answer() {
	var gubun = $("#gubun option:selected").val();
	var subject = $("#answer_subject").val();
	var user = $("#user").val();
	var project = $("#project").val();
	var input_data = {"gubun" : gubun, "subject" : subject, "user" : user, "project" : project};
	
	ajax('/search_answer', input_data, 'search_answer', 'POST');
}

function search_answer_by_answer_num(answer_num) {
	var user = $("#user").val();
	var project = $("#project").val();
	var input_data = {"answer_num" : answer_num, "user" : user, "project" : project};
	
	ajax('/search_answer_by_answer_num', input_data, 'search_answer', 'POST');
}

function search_answer_callback(retData) {
	grid_data2 = [];
	var retList = retData['results'];
	for (var i = 0; i < retList.length; ++i) {
		var a = [];
		a.push(retList[i]['rpsn_question']);
		a.push(retList[i]['answer']);
		a.push(retList[i]['answer_num']);
		grid_data2.push(a);
	}
	mygrid2.refresh(grid_data2);
	mygrid2.gotoPage(1);
	$("#answer_num").val('');
}

function search_question(answer_num) {
	var user = $("#user").val();
	var project = $("#project").val();
	var answer_num = $("#answer_num").val();	
	var input_data = {"answer_num" : answer_num, "user" : user, "project" : project};
	ajax('/search_question', input_data, 'search_question', 'POST');
}

function search_question_callback(retData) {
	grid_data3 = [];
	var retList = retData['results'];
	for (var i = 0; i < retList.length; ++i) {
		var a = [];
		a.push(i + 1);
		a.push(retList[i]['answer_num']);
		if (retList[i]['question_voca'] == null) {
			retList[i]['question_voca'] = '';
		}
		var question_voca_arr = retList[i]['question_voca'].replace(/\^/g, ";").split(";");
		var question = highlight(retList[i]['question'], question_voca_arr, "text-highlight");
		a.push(question);
		grid_data3.push(a);
	}
	mygrid3.refresh(grid_data3);
	mygrid3.gotoPage(1);
}

function mapping_new_question_answer() {
	var end_row_num = mygrid1.getPageInfo()["endRowNum"];
	var question_arr = [];
	var answer_num_arr = [];
	for (var i = 0; i < end_row_num; ++i) {
		var cell = mygrid1.getCell(i, "chk");
		if (is_grid_checked(cell)) {
			var question = $(mygrid1.getCell(i, "question")).text();
			question_arr.push(question);
		}
	}
	end_row_num = mygrid2.getPageInfo()["endRowNum"];
	for (var i = 0; i < end_row_num; ++i) {
		var cell = mygrid2.getCell(i, "chk");
		if (is_grid_checked(cell)) {
			var answer_num = $(mygrid2.getCell(i, "answer_num")).text();
			answer_num_arr.push(answer_num);
		}
	}
	if (question_arr.length == 0 || answer_num_arr.length == 0) {
		alert("매핑할 질문 또는 답변 체크박스를 체크하세요.");
		return;
	}
	
	if (question_arr.length > 1 || answer_num_arr.length > 1) {
		alert("질문과 답변 매핑은 1:1이어야 합니다.");
		return;
	}
	
	submit_question(question_arr[0], answer_num_arr[0]);
}

function submit_question(question, answer_num) {
	if (!confirm("전송 하시겠습니까?")) {
		return;
	}
	var input_data = [];
	var user = $("#user").val();
	var project = $("#project").val();
	var question_tag = "";
	input_data.push({"user" : user, "project" : project, "question" : question, "question_tag" : question_tag, "answer_num" : answer_num});

	ajax('/submit_question', input_data, 'submit_question', 'POST');
}

function submit_question_callback() {
	alert("전송이 완료되었습니다.");
	search_question();
}
