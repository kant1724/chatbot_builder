var grid_data1 = [];
var grid_data2 = [];
var grid_demo_id1 = "myGrid1";
var grid_demo_id2 = "myGrid2";

var dsOption1 = {
	fields :[
		{name : 'num'  },
		{name : 'answer_num' },
		{name : 'rpsn_question' }
	],
	recordType : 'array',
	data : grid_data1
}

var dsOption2 = {
	fields :[
		{name : 'num'  },
		{name : 'answer_num' },
		{name : 'bucket_id'  },
		{name : 'question'  }
	],
	recordType : 'array',
	data : grid_data2
}

var colsOption1 = [
	 {id: 'num' , header: "순번" , width :40 },
	 {id: 'answer_num' , header: "답변번호" , width :60 },
	 {id: 'rpsn_question' , header: "최대길이질문" , width :340 }
];

var colsOption2 = [
	 {id: 'num' , header: "순번" , width :40 },
	 {id: 'answer_num' , header: "답변번호" , width :60 },
	 {id: 'bucket_id' , header: "버킷ID" , width :60 },
	 {id: 'question' , header: "질문" , width :720 }
];

var gridOption1={
	id : grid_demo_id1,
	width: "900",
	height: "336",
	container : 'bucket_grid', 
	replaceContainer : true, 
	dataset : dsOption1,
	columns : colsOption1,
	pageSize: 13,
	toolbarContent : 'nav goto | pagesize | reload | print filter chart | state',
	pageSizeList : [13,30,48,60,100],
	skin : "mac",
	onRowClick:function(value, record, cell, row, colNO, rowNO, columnObj, grid) {
		var static_col_cnt = 3; 
		var answer_num = record[1];
		$('#answer_num').val(answer_num);
		if (colNO >= static_col_cnt) {
			var bucket_id = colNO - static_col_cnt;
			search_question_and_bucket_id(bucket_id);
		} else {
			search_question_and_bucket_id('');
		}
	}
};

var gridOption2={
	id : grid_demo_id2,
	width: "900",
	height: "314",
	container : 'question_grid', 
	replaceContainer : true, 
	dataset : dsOption2,
	columns : colsOption2,
	pageSize: 12,
	toolbarContent : 'nav goto | pagesize | reload | print filter chart | state',
	pageSizeList : [12,24,36,48,100],
	skin : "mac",
	onRowClick:function(value, record, cell, row, colNO, rowNO, columnObj, grid) {
	}
};

var mygrid1 = null;
var mygrid2 = new Sigma.Grid(gridOption2);
Sigma.Util.onLoad(Sigma.Grid.render(mygrid2));

$(document).ready(function() {
	$("#search_question_and_bucket_id").click(function() {
		grid_data1 = [];
		$('#answer_num').val('');
		search_question_and_bucket_id('');
	});
	$("#subject").keydown(function (key) {
        if (key.keyCode == 13) {
        	grid_data1 = [];
        	$('#answer_num').val('');
        	search_question_and_bucket_id('');
        }
    });
	search_bucket_id();
	search_question_and_bucket_id('');
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
        	if (gubun == "search_bucket_id") {
        		search_bucket_id_callback(data['results']);
        	} else if (gubun == "search_question_and_bucket_id") {
        		search_question_and_bucket_id_callback(data['results']);
            }
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}

function search_bucket_id() {
	var input_data = {"user" : $('#user').val(), "project" : $('#project').val()};
	ajax('/search_bucket_id', input_data, 'search_bucket_id', 'POST');
}

function search_question_and_bucket_id(bucket_id) {
	var input_data = {"user" : $('#user').val(), "project" : $('#project').val(), "question_nm" : $('#subject').val(), "answer_num" : $('#answer_num').val(), "bucket_id" : bucket_id};
	ajax('/search_question_and_bucket_id', input_data, 'search_question_and_bucket_id', 'POST');
}

function count_question_in_buckets(ret_data) {
	grid_data1 = [];
	var answer_and_question_cnt = {};
	var answer_and_question = {};
	for (var i = 0; i < ret_data.length; ++i) {
		var answer_num_arr = ret_data[i]["answer_num"].split(";");
		var bucket_id = ret_data[i]["bucket_id"];
		for (var k = 0; k < answer_num_arr.length; ++k) {
			var answer_num = answer_num_arr[k];
			if (answer_and_question_cnt[answer_num] == null) {
				var d = {};
				for (var j = 0; j < buckets.length; ++j) {
					if (j == Number(bucket_id)) {
						d['bucket_' + j] = 1;
					} else {
						d['bucket_' + j] = 0;
					}
				}
				answer_and_question_cnt[answer_num] = d;
			} else {
				answer_and_question_cnt[answer_num]['bucket_' + Number(bucket_id)] += 1; 
			}
			var question = ret_data[i]["question"];
			if (answer_and_question[answer_num] == null) {
				answer_and_question[answer_num] = question;
			} else {
				if (question.length > answer_and_question[answer_num].length) {
					answer_and_question[answer_num] = question;
				}
			}
		}
	}
	var cnt = 0;
	for (var key in answer_and_question_cnt) {
		if (key.split(";").length > 1) {
			continue;
		}
		var a = [];
		a.push(cnt + 1);
		a.push(key);
		a.push(answer_and_question[key]);
		var d = answer_and_question_cnt[key];
		for (var k in d) {
			a.push(d[k])
		}
		grid_data1.push(a);
		cnt += 1;
	}
	mygrid1.refresh(grid_data1);
	mygrid1.gotoPage(1);	
}

var buckets = [];
function search_bucket_id_callback(ret_data) {
	buckets = ret_data["buckets"].split(",");
	for (var i = 0; i < buckets.length; ++i) {
		dsOption1['fields'].push({name : "bucket_" + i});
		var header = "";
		if (i < buckets.length - 1) {
			header = "[" + buckets[i] + "~" + (buckets[i + 1] - 1) + "]";
		} else {
			header = "[" + buckets[i] + "~∞]";
		}
		colsOption1.push({id: "bucket_" + i, header: header, width :55 });
	}
	mygrid1 = new Sigma.Grid(gridOption1);
	Sigma.Util.onLoad(Sigma.Grid.render(mygrid1));
}

function highlight(content, what, spanClass) {
	var replaceWith = '<span ' + ( spanClass ? 'class="' + spanClass + '"' : '' ) + '">' + what + '</span>';
	var highlighted = content.replace(what, replaceWith);
    
    return highlighted;
}

function search_question_and_bucket_id_callback(ret_data) {
	grid_data2 = [];
	for (var i = 0; i < ret_data.length; i++) {
		var a = [];
		a.push(i + 1);
		a.push(ret_data[i]["answer_num"]);
		a.push(ret_data[i]["bucket_id"]);
		if (ret_data[i]['question_voca'] == null) {
			ret_data[i]['question_voca'] = '';
		}
		var question_voca_arr = ret_data[i]['question_voca'].replace(/\^/g, ";").split(";");
		var question = highlight(ret_data[i]["question"], question_voca_arr, "text-highlight");
		a.push(question);
		grid_data2.push(a);		
	}
	mygrid2.refresh(grid_data2);
	mygrid2.gotoPage(1);
	
	if (grid_data1.length == 0) {
		count_question_in_buckets(ret_data);
	}
}
