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
	 {id: 'big_category' , header: "대분류" , width :160 , editor: {  type :"text"  }},
	 {id: 'middle_category' , header: "중분류" , width :160 , editor: {  type :"text"  }},
	 {id: 'small_category_lv1' , header: "소분류 lv1" , width :160 , editor: {  type :"text"  }},
	 {id: 'small_category_lv2' , header: "소분류 lv2" , width :160 , editor: {  type :"text"  }},
	 {id: 'small_category_lv3' , header: "소분류 lv3" , width :160 , editor: {  type :"text"  }}
];

var gridOption1={
	id : grid_demo_id1,
	width: "900",
	height: "690",
	container : 'category_grid', 
	replaceContainer : true, 
	dataset : dsOption1 ,
	columns : colsOption1,
	pageSize: 20000,
	toolbarContent : 'nav goto | pagesize | reload | print filter chart | state',
	pageSizeList : [20000],
	skin : "mac",
	onRowClick:function(value, record, cell, row, colNO, rowNO, columnObj, grid) {
		var category_num = record[1];
		$("#category_num").val(category_num);
		$("#cur_row").val(rowNO);
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
	$("#search_category").click(function() {
		search_category();
	});
	$("#add_category").click(function() {
		add_category();
	});
	$("#submit_category").click(function() {
		submit_category();
	});
	$("#delete_category").click(function() {
		delete_category();
	});
	$("#subject").keydown(function (key) {
        if (key.keyCode == 13) {
        	search_category();
        }
    });
	search_category();
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
        	if (gubun == "search_category") {
        		search_category_callback(data['results']);
            } else if (gubun == "submit_category") {
            	submit_category_callback();
            } else if (gubun == "delete_category") {
            	delete_category_callback();
            }
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}

function search_category() {
	var input_data = {"category_nm" : $('#subject').val()};
	ajax('/search_category', input_data, 'search_category', 'POST');
}

function search_category_callback(ret_data) {
	mygrid1.endEdit();
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

function submit_category() {
	mygrid1.endEdit();
	if (!confirm("저장 하시겠습니까?")) {
		return;
	}
	var input_data = [];
	for (var i = 0; i < grid_data1.length; ++i) {
		if (grid_data1[i][7] == "default")
			continue;
		var input = {};
		input["category_num"] = grid_data1[i][1];
		input["big_category"] = grid_data1[i][2]; 
		input["middle_category"] = grid_data1[i][3];
		input["small_category_lv1"] = grid_data1[i][4];
		input["small_category_lv2"] = grid_data1[i][5];
		input["small_category_lv3"] = grid_data1[i][6];
		input["data_type"] = grid_data1[i][7];
		input_data.push(input);
	}
	ajax('/submit_category', input_data, 'submit_category', 'POST');
}

function delete_category() {
	var cur_row = $("#cur_row").val();
	if ($("#category_num").val() == '' && cur_row != '') {
		grid_data1.splice(cur_row, 1);
		mygrid1.refresh(grid_data1);
		return;
	}
	if (!confirm("삭제 하시겠습니까?")) {
		return;
	}
	var input_data = {"category_num" : $("#category_num").val()};
	ajax('/delete_category', input_data, 'delete_category', 'POST');
}

function update_category() {
	if (!confirm("분류를 업데이트 하시겠습니까?")) {
		return;
	}
	var input_data = {};
	ajax('/update_category', input_data, 'update_category', 'POST');
}

function submit_category_callback() {
	alert("저장이 완료되었습니다.");
	search_category();
}

function delete_category_callback() {
	alert("삭제가 완료되었습니다.");
	search_category();
}

function add_category() {
	var a = [];
	a.push(grid_data1.length + 1);
	a.push("");
	a.push("");
	a.push("");
	a.push("");
	a.push("");
	a.push("");
	a.push("new");
	grid_data1.push(a);
	mygrid1.refresh(grid_data1);
}
