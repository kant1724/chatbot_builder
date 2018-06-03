var grid_data1 = [[]];
var grid_data2 = [[]];
var grid_demo_id1 = "myGrid1";
var grid_demo_id2 = "myGrid2";

var dsOption1= {
	fields :[
		{name : 'num'  },
		{name : 'synonym_nm'  },
		{name : 'synonym_tag'  },
		{name : 'data_type'  }
	],
	recordType : 'array',
	data : grid_data1
}

var dsOption2= {
		fields :[
			{name : 'num'  },
			{name : 'synonym_num'  },
			{name : 'synonym_nm'  },
			{name : 'synonym_tag'  },
			{name : 'data_type'  }
		],
		recordType : 'array',
		data : grid_data2
	}

var colsOption1 = [
	 {id: 'num' , header: "순번" , width :60 },
	 {id: 'synonym_nm' , header: "동의어" , width :600 },
	 {id: 'synonym_tag' , header: "태그명" , width :200 }
];

var colsOption2 = [
	 {id: 'num' , header: "순번" , width :60 },
	 {id: 'synonym_nm' , header: "동의어" , width :800 , editor: {  type :"text"  }}
];

var gridOption1={
	id : grid_demo_id1,
	width: "900",
	height: "320",
	container : 'synonym_master_grid', 
	replaceContainer : true, 
	dataset : dsOption1 ,
	columns : colsOption1,
	pageSize: 30,
	toolbarContent : 'nav goto | pagesize | reload | print filter chart | state',
	pageSizeList : [30,40,60,80,100],
	skin : "mac",
	onRowClick:function(value, record, cell, row, colNO, rowNO, columnObj, grid) {
		var synonym_tag = record[2];
		$("#synonym_tag").val(synonym_tag);
		search_synonym_by_synonym_tag(synonym_tag);
	}
};

var gridOption2={
	id : grid_demo_id2,
	width: "900",
	height: "340",
	container : 'synonym_detail_grid', 
	replaceContainer : true, 
	dataset : dsOption2 ,
	columns : colsOption2,
	pageSize:20000,
	toolbarContent : 'nav goto | pagesize | reload | print filter chart | state',
	pageSizeList : [20000],
	skin : "mac",
	onRowClick:function(value, record, cell, row, colNO, rowNO, columnObj, grid) {
		var synonym_num = record[1];
		$("#synonym_num").val(synonym_num);
		$("#synonym_detail_cur_row").val(rowNO);
	},
	afterEdit:function(value, oldValue, record, col, grid) {
		if (value != oldValue && record[4] == "default") {
			record[4] = "modified";
		}
	}
};

var mygrid1 = new Sigma.Grid(gridOption1);
var mygrid2 = new Sigma.Grid(gridOption2);
Sigma.Util.onLoad(Sigma.Grid.render(mygrid1));
Sigma.Util.onLoad(Sigma.Grid.render(mygrid2));

$(document).ready(function() {
	$("#search_synonym").click(function() {
		search_synonym();
	});
	$("#new_master").click(function() {
		new_master();
	});
	$("#new_detail").click(function() {
		new_detail();
	});
	$("#submit_synonym_detail").click(function() {
		submit_synonym_detail();
	});
	$("#delete_synonym_master").click(function() {
		delete_synonym_master();
	});
	$("#delete_synonym_detail").click(function() {
		delete_synonym_detail();
	});
	$("#subject").keydown(function (key) {
        if (key.keyCode == 13) {
        	search_synonym();
        }
    });
	search_synonym();
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
        	if (gubun == "search_synonym") {
        		search_synonym_callback(data['results']);
            } else if (gubun == 'submit_synonym_detail') {
            	submit_synonym_detail_callback();
            } else if (gubun == "search_synonym_by_synonym_tag") {
            	search_synonym_by_synonym_tag_callback(data['results']);
            } else if (gubun == "delete_synonym_master") {
            	delete_synonym_master_callback();
            } else if (gubun == "delete_synonym_detail") {
            	delete_synonym_detail_callback()
            }
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}

function search_synonym() {
	var input_data = {"synonym_nm" : $('#subject').val()};
	ajax('/search_synonym', input_data, 'search_synonym', 'POST');
}

function search_synonym_by_synonym_tag(synonym_tag) {
	var input_data = {"synonym_tag" : synonym_tag};
	ajax('/search_synonym_by_synonym_tag', input_data, 'search_synonym_by_synonym_tag', 'POST');
}

function search_synonym_callback(ret_data) {
	mygrid2.endEdit();
	var synonym_dict = {};
	for (var i = 0; i < ret_data.length; i++) {
		var tag = ret_data[i]["synonym_tag"];
		if (synonym_dict[tag] != null) {
			synonym_dict[tag] += "'" + ret_data[i]["synonym_nm"] + "'";
		} else {
			synonym_dict[tag] = "'" + ret_data[i]["synonym_nm"] + "'";
		}
		if (i < ret_data.length - 1) {
			synonym_dict[tag] += ",";
		}
	}
	var cnt = 0;
	grid_data1 = [];
	for (name in synonym_dict) {
		var a = [];
		a.push(cnt + 1);
		a.push(synonym_dict[name]);
		a.push(name);
		a.push("default");
		grid_data1.push(a);
		cnt += 1;
	}
	mygrid1.refresh(grid_data1);
	mygrid1.gotoPage(1);
	$("#synonym_tag").val('');
}

function search_synonym_by_synonym_tag_callback(ret_data) {
	mygrid2.endEdit();
	grid_data2 = [];
	for (var i = 0; i < ret_data.length; i++) {
		var a = [];
		a.push(i + 1);
		a.push(ret_data[i]["synonym_num"]);
		a.push(ret_data[i]["synonym_nm"]);
		a.push(ret_data[i]["synonym_tag"]);
		a.push("default");
		grid_data2.push(a);
	}
	mygrid2.refresh(grid_data2);
	mygrid2.gotoPage(1);
	$("#synonym_num").val('');
	$("#synonym_detail_cur_row").val('');
}

function new_detail() {
	var a = [];
	a.push(grid_data2.length + 1);
	a.push("");
	a.push("");
	a.push($("#synonym_tag").val());
	a.push("new");
	grid_data2.push(a);
	mygrid2.refresh(grid_data2);
}

function submit_synonym_detail() {
	mygrid2.endEdit();
	if (!confirm("저장 하시겠습니까?")) {
		return;
	}
	var input_data = get_input_data();
	if (input_data.length == 0) {
		alert("변경된 데이터가 없습니다.");
		return;
	}
	ajax('/submit_synonym', input_data, 'submit_synonym_detail', 'POST');
}

function delete_synonym_master() {
	if ($("#synonym_tag").val() == '') {
		alert("삭제할 열을 선택하세요.");
		return;
	}
	if (!confirm("삭제 하시겠습니까?")) {
		return;
	}
	var input_data = {"synonym_tag" : $("#synonym_tag").val()};
	ajax('/delete_synonym_master', input_data, 'delete_synonym_master', 'POST');
}

function delete_synonym_detail() {
	if ($("#synonym_detail_cur_row").val() == '') {
		alert("삭제할 열을 선택하세요.");
		return;
	}
	var cur_row = $("#synonym_detail_cur_row").val(); 
	if ($("#synonym_num").val() == '' && cur_row != '') {
		grid_data2.splice(cur_row, 1);
		mygrid2.refresh(grid_data2);
		return;
	}
	if (!confirm("삭제 하시겠습니까?")) {
		return;
	}
	var input_data = {"synonym_num" : $("#synonym_num").val()};
	ajax('/delete_synonym_detail', input_data, 'delete_synonym_detail', 'POST');
}

function submit_synonym_detail_callback() {
	alert("전송이 완료되었습니다.");
	search_synonym();
}

function delete_synonym_master_callback() {
	alert("삭제가 완료되었습니다.");
	mygrid2.refresh([]);
	search_synonym();
}

function delete_synonym_detail_callback() {
	alert("삭제가 완료되었습니다.");
	search_synonym_by_synonym_tag($("#synonym_tag").val());
	search_synonym();
}

function get_input_data() {
	res = [];
	for (var i = 0; i < grid_data2.length; ++i) {
		if (grid_data2[i][4] != "new" && grid_data2[i][4] != "modified") continue; 
		var input_data = {"synonym_num" : grid_data2[i][1], "synonym_nm" : grid_data2[i][2], "synonym_tag" : grid_data2[i][3], "data_type" : grid_data2[i][4]};
		res.push(input_data);
	}
	return res;
}

function new_master() {
	var w = NEW_SYNONYM_POPUP_WIDTH;
	var h = NEW_SYNONYM_POPUP_HEIGHT;
	var y = window.top.outerHeight / 2 + window.top.screenY - ( h / 2);
	var x = window.top.outerWidth / 2 + window.top.screenX - ( w / 2);
	window.open('/new_synonym_pop', '_blank', 'width=' + w + ', height=' + h + ', left=' + x + ', top=' + y);
	search_synonym();
}
