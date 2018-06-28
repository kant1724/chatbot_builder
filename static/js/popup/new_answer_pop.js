var grid_data1 = [];
var grid_demo_id1 = "myGrid1";

var dsOption1= {
	fields :[
		{name : 'num'  },
		{name : 'category_num' },
		{name : 'big_category'  },
		{name : 'middle_category'  },
		{name : 'small_category_lv1'  },
		{name : 'small_category_lv2'  },
		{name : 'small_category_lv3'  },
		{name : 'data_type'  }
	],
	recordType : 'array',
	data : grid_data1
}

var colsOption1 = [
	 {id: 'num' , header: "순번" , width :60 },
	 {id: 'big_category' , header: "대분류" , width :80 },
	 {id: 'middle_category' , header: "중분류" , width :80},
	 {id: 'small_category_lv1' , header: "소분류 lv1" , width :80},
	 {id: 'small_category_lv2' , header: "소분류 lv2" , width :80 },
	 {id: 'small_category_lv3' , header: "소분류 lv3" , width :80 }
];

var gridOption1={
	id : grid_demo_id1,
	width: "500",
	height: "200",
	container : 'category_grid', 
	replaceContainer : true, 
	dataset : dsOption1 ,
	columns : colsOption1,
	pageSize: 30,
	toolbarContent : 'nav goto | pagesize | reload | print filter chart | state',
	pageSizeList : [30,40,60,80,100],
	skin : "mac",
	onRowClick:function(value, record, cell, row, colNO, rowNO, columnObj, grid) {
		var category_num = record[1];
		$("#category_num").val(category_num);
	},
	afterEdit:function(value, oldValue, record, col, grid) {
		if (value != oldValue && record[7] == "default") {
			record[7] = "modified";
		}
	}
};

var mygrid1 = new Sigma.Grid(gridOption1);
Sigma.Util.onLoad(Sigma.Grid.render(mygrid1));

$(document).ready(function() {
	$("#submit_answer").click(function() {
		submit_answer();
	});
	$("#put_emphasis").click(function() {
		put_emphasis();
	});
	search_category();
	if ($('#rq_num').val() != '') {
		search_new_request_by_rq_num();
	}	
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
            if (gubun == "submit_answer") {
            	submit_answer_callback();
            } else if (gubun == "search_category") {
        		search_category_callback(data['results']);
            } else if (gubun == "search_new_request_by_rq_num") {
            	search_new_request_by_rq_num_callback(data['results']);
            }
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}

function submit_answer() {
	if ($("#question_input").val() == "") {
		alert("질문을 작성하세요");
		return;
	}
	if ($("#answer_input").val() == "") {
		alert("답변을 작성하세요");
		return;
	}
	if (!confirm("전송 하시겠습니까?")) {
		return;
	}
	var user = $("#user").val();
	var project = $("#project").val();
	var question_input = $("#question_input").val();
	var question_tag_input = '';
	var answer_input = $("#answer_input").val();
	var category_num = $("#category_num").val();
	var rq_num = $("#rq_num").val();
	var input_data = {"user" : user, "project" : project, "question" : question_input, "question_tag" : question_tag_input, "answer" : answer_input, "category_num" : category_num, "rq_num" : rq_num};
	
	ajax('/submit_answer', input_data, 'submit_answer', 'POST');
}

function submit_answer_callback() {
	alert("전송이 완료되었습니다.");
	if (opener.search_answer != null) {
		opener.search_answer();
	}
	window.close();
}

function search_category() {
	var input_data = {"category_nm" : $('#subject').val()};
	ajax('/search_category', input_data, 'search_category', 'POST');
}

function search_category_callback(ret_data) {	
	grid_data1 = [];
	for (var i = 0; i < ret_data.length; i++) {
		var a = [];
		a.push(i + 1);
		a.push(ret_data[i]["category_num"]);
		a.push(ret_data[i]["big_category"]);
		a.push(ret_data[i]["middle_category"]);
		a.push(ret_data[i]["small_category_lv1"]);
		a.push(ret_data[i]["small_category_lv2"]);
		a.push(ret_data[i]["small_category_lv3"]);
		a.push("default");
		grid_data1.push(a);
	}
	mygrid1.refresh(grid_data1);
	mygrid1.gotoPage(1);
}

function search_new_request_by_rq_num() {
	var user = $("#user").val();
	var project = $("#project").val();
	var rq_num = $("#rq_num").val();
	var input_data = {"user" : user, "project" : project, "rq_num" : rq_num};
	ajax('/search_new_request_by_rq_num', input_data, 'search_new_request_by_rq_num', 'POST');
}

function search_new_request_by_rq_num_callback(ret_data) {
	$('#question_input').val(ret_data["question"]);
}

function put_emphasis() {
	replaceSelectedText($("#answer_input"));
}
