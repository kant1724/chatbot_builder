var grid_data1 = [];
var grid_demo_id1 = "myGrid1";

var dsOption1= {
	fields :[
		{name : 'num'  },
		{name : 'new_question' },
		{name : 'bucket' }
	],
	recordType : 'array',
	data : grid_data1
}

var colsOption1 = [
	 {id: 'num' , header: "순번" , width :60 },
	 {id: 'new_question' , header: "질문" , width :400 },
	 {id: 'bucket' , header: "버킷" , width :80 },
];

var gridOption1={
	id : grid_demo_id1,
	width: "550",
	height: "250",
	container : 'new_question_grid', 
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
		$("#num").val(num);
		$("#question_input").val(question);
	}
};

var mygrid1 = new Sigma.Grid(gridOption1);
Sigma.Util.onLoad(Sigma.Grid.render(mygrid1));

$(document).ready(function() {
	$("#add_row").click(function() {
		add_row('', 0);
	});
	$("#del_row").click(function() {
		del_row();
	});
	$("#auto_add_row").click(function() {
		auto_add_row();
	});
	$("#submit_question").click(function() {
		submit_question();
	});
	$("#set_highlight").click(function() {
		set_highlight();
	});
	$("#reset_highlight").click(function() {
		reset_highlight();
	});
	$("#clear_all").click(function() {
		clear_all();
	});
	$("#question_input").on('input', function() {
		var question = $("#question_input").val();
		get_bucket_id_by_sentence(question);
	});
	search_bucket_id();
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
        	if (gubun == "submit_question") {
            	submit_question_callback();
            } else if (gubun == "get_compression_tag") {
            	get_compression_tag_callback(data);
            } else if (gubun == "search_bucket_id") {
            	search_bucket_id_callback(data['results']);
        	}
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}

var last_question_length = 0;
var bucket_id = 0;
function get_bucket_id_by_sentence(question) {
	if (last_question_length != question.length) {
		last_question_length = question.length; 
		bucket_id = get_bucket_id(question);
	}
	var num = $("#num").val();
	for (var i = 0; i < grid_data1.length; ++i) {
		if (grid_data1[i][0] == num) {
			grid_data1[i][1] = question;
			grid_data1[i][2] = bucket_id; 
			break;
		}
	}
	mygrid1.refresh(grid_data1);
}

function submit_question() {
	if (grid_data1.length == 0) {
		alert("질문을 작성하세요");
		return;
	}
	if (!confirm("전송 하시겠습니까?")) {
		return;
	}
	var input_data = [];
	for (var i = 0; i < grid_data1.length; ++i) {
		var user = $("#user").val();
		var project = $("#project").val();
		var question = grid_data1[i][1];
		var question_tag = "";
		var answer_num = $("#answer_num").val();
		input_data.push({"user" : user, "project" : project, "question" : question, "question_tag" : question_tag, "answer_num" : answer_num});
	}
	ajax('/submit_question', input_data, 'submit_question', 'POST');
}

function submit_question_callback() {
	alert("전송이 완료되었습니다.");
	opener.search_question();
	window.close();
}

function search_bucket_id() {
	var input_data = {"user" : $('#user').val(), "project" : $('#project').val()};
	ajax('/search_bucket_id', input_data, 'search_bucket_id', 'POST');
}

var buckets = [];
var exception = [];
function search_bucket_id_callback(ret_data) {
	buckets = ret_data["buckets"].split(",");
	exception = eval(ret_data["exception"]);
}

function add_row(question, bucket_id) {
	var a = [];
	a.push(grid_data1.length + 1);
	a.push(question);
	a.push(bucket_id);
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

function clear_all() {
	grid_data1 = [];
	mygrid1.refresh(grid_data1);
}

var highlight_arr = [];
var expression_dict = {};
function make_highlight_arr(range) {
	for (var i = 0; i < highlight_arr.length; ++i) {
		var highlight = highlight_arr[i];
		if (range[0] == highlight[0] && range[1] == highlight[1]) continue;
		if (check_intersect(range, highlight) || check_intersect(highlight, range)) {
			highlight_arr[i] = merge(range, highlight);
			make_highlight_arr(highlight);
			return true;
		}
	}
	return false;
}

function check_intersect(a, b) {
	if (a[0] >= b[0] && a[0] < b[1]) {
		return true;
	}
	return false;
}

function merge(a, b) {
	var c = [];
	c[0] = Math.min(a[0], b[0]);
	c[1] = Math.max(a[1], b[1]);
	return c;
}

function make_set_array(arr) {
	var ret = [];
	for (var i = 0; i < arr.length; ++i) {
		var has = false;
		for (var j = 0; j < ret.length; ++j) {
			if (arr[i][0] == ret[j][0] && arr[i][1] == ret[j][1]) {
				has = true;
				break;
			}
		}
		if (!has) {
			ret.push(arr[i]);
		}
	}
	return ret;
}

$("#question_input").mouseup(function() {
	var range = getSelectedRange();
	if (range[0] == range[1]) return;
	if (range != '') {
		var text = $('#question_input').val().substring(range[0], range[1]);
		$("#expression").val(text);
		$("#fragment_range").val(range[0] + "," + range[1]);
		get_compression_tag();
    }
});

$("#question_input").keyup(function(e) {
	if (e.which == 27) {
    	reset_highlight();
    }
	if (e.which < 37 || e.which > 40) {
		return;
	}
	var range = getSelectedRange();
	if (range[0] == range[1]) return;
	if (range != '') {
		var text = $('#question_input').val().substring(range[0], range[1]);
		$("#expression").val(text);
		$("#fragment_range").val(range[0] + "," + range[1]);
		get_compression_tag();
    }
});

function set_highlight() {
	var range = $("#fragment_range").val();
	var fr = range.split(",");
	$('#question_input').selectRange(Number(fr[0]), Number(fr[1]));
	var range = getSelectedRange();
	if (!make_highlight_arr(range)) {
		highlight_arr.push(range);
	}
	highlight_arr = make_set_array(highlight_arr);
	$('#question_input').highlightWithinTextarea({
		highlight: highlight_arr
	});
}

function get_compression_tag() {
	var user = $("#user").val();
	var project = $("#project").val();
	var expression = $("#expression").val();
	var input_data = {"user" : user, "project" : project, "expression" : expression};
	ajax('/get_compression_tag', input_data, 'get_compression_tag', 'POST');
}

function get_compression_tag_callback(data) {
	var num = data['num'];
	var t = "";
	var expression_arr = [];
	for (var i = 0; i < num; ++i) {
		t += data['text' + (i + 1)] + "\n";
		expression_arr.push(data['text' + (i + 1)]);
	}
	expression_dict[$("#expression").val()] = expression_arr; 
	$("#realtime_reserve").text(t);
}

function reset_highlight() {
	highlight_arr = [];
	$('#question_input').highlightWithinTextarea({
		highlight: highlight_arr
	});
}

function auto_add_row() {
	if (highlight_arr.length == 0) {
		alert("마우스를 드래그 하여 자동생성하고자 하는 부분을 선택해 주세요.");
		return;
	}
	if (highlight_arr.length > 2) {
		alert("현재 2개까지만 지원합니다.");
		return;
	}
	if (highlight_arr.length == 1) {
		add_length_1();
	} else if (highlight_arr.length == 2) {
		add_length_2();
	}
}

function get_bucket_id(question) {
	var token = char_tokenizer(question, exception);
	var bucket_id = 0;
	for (var i = 0; i < buckets.length; ++i) {
		if (token.length < buckets[i]) {
			bucket_id = Math.max(i - 1, 0);
			break;
		}
	}
	return bucket_id;
}

function add_length_1() {
	var range1 = highlight_arr[0];
	var full = $('#question_input').val();
	var expression = full.substring(range1[0], range1[1]);
	var arr1 = expression_dict[expression];
	for (var i = 0; i < arr1.length; ++i) {
		var a = arr1[i];
		var new_question = full.replace(expression, a, "g");
		add_row(new_question, get_bucket_id(new_question));
	}
}

function add_length_2() {
	var range1 = highlight_arr[0];
	var range2 = highlight_arr[1];
	var full = $('#question_input').val();
	var expression_1 = full.substring(range1[0], range1[1]);
	var expression_2 = full.substring(range2[0], range2[1]);
	var arr1 = expression_dict[expression_1];
	var arr2 = expression_dict[expression_2];
	for (var i = 0; i < Math.max(arr1.length, arr2.length); ++i) {
		var a = arr1[Math.min(arr1.length - 1, i)];
		var b = arr2[Math.min(arr2.length - 1, i)];
		var new_question = full.replace(expression_1, a, "g").replace(expression_2, b, "g");		
		add_row(new_question, get_bucket_id(new_question));
	}
}

function add_data1(new_question) {
	var d = {};
	d["id"]= "id_" + (data1.length + 1);
	d["num"]= data1.length + 1;
	d["question"] = new_question;
	data1.push(d);
}

$.fn.selectRange = function(start, end) {
	return this.each(function() {
		if (this.setSelectionRange) {
			this.focus();
			this.setSelectionRange(start, end);
	    } else if (this.createTextRange) {
	    	var range = this.createTextRange();
	    	range.collapse(true);
	    	range.moveEnd('character', end);
	    	range.moveStart('character', start);
	    	range.select();
	    }
	});
};
