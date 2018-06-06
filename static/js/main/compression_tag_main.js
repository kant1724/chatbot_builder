var grid_data1 = [];
var grid_demo_id1 = "myGrid1";

var dsOption1= {
	fields :[
		{name : 'num'  },
		{name : 'compression_num'  },
		{name : 'expression'  },
		{name : 'tag_name'  },
		{name : 'data_type'  }
	],
	recordType : 'array',
	data : grid_data1
}

var colsOption1 = [
	 {id: 'num' , header: "순번" , width :60 },
	 {id: 'expression' , header: "부분문장" , width :620, editor: {  type :"text"  } },
	 {id: 'tag_name' , header: "태그명" , width :200, editor: {  type :"text"  } }
];

var gridOption1={
	id : grid_demo_id1,
	width: "900",
	height: "622",
	container : 'compression_tag_grid', 
	replaceContainer : true, 
	dataset : dsOption1 ,
	columns : colsOption1,
	pageSize: 20000,
	toolbarContent : 'nav goto | pagesize | reload | print filter chart | state',
	pageSizeList : [20000],
	skin : "mac",
	onRowClick:function(value, record, cell, row, colNO, rowNO, columnObj, grid) {
		var compression_num = record[1];
		$("#compression_num").val(compression_num);
		$("#cur_row").val(rowNO);
	},
	afterEdit:function(value, oldValue, record, col, grid) {
		if (value != oldValue && record[4] == "default") {
			record[4] = "modified";
		}
	}
};

var mygrid1 = new Sigma.Grid(gridOption1);
Sigma.Util.onLoad(Sigma.Grid.render(mygrid1));

$(document).ready(function() {
	$("#search_compression_tag").click(function() {
		search_compression_tag();
	});
	$("#add_row").click(function() {
		alert("제한된 기능입니다.");
		return;
		add_row();
	});
	$("#del_row").click(function() {
		alert("제한된 기능입니다.");
		return;
		del_row();
	});
	$("#submit_compression_tag").click(function() {
		alert("제한된 기능입니다.");
		return;
		submit_compression_tag();
	});
	$("#delete_ckpt_file").click(function() {
		alert("제한된 기능입니다.");
		return;
		delete_ckpt_file();
	});
	start_interval_is_training();
	get_is_training();
	$("#start_training").click(function() {
		var training_status = $("#start_training").text();
		if (training_status == "훈련시작") {
			start_training();
		} else {
			stop_training();
		}
	});
	$("#subject").keydown(function (key) {
        if (key.keyCode == 13) {
        	search_compression_tag();
        }
    });
	search_compression_tag();
});
	
function ajax(url, input_data, gubun, method) {
	var as = false;
	if (gubun == 'start_training') {
		as = true
	}
	$.ajax(url, {
		type: method, 
        data: JSON.stringify(input_data),
        async: as,
        contentType: 'application/json',
        dataType: 'json',
        processData: false,
        success: function (data, status, xhr) {
        	if (gubun == "search_compression_tag") {
        		search_compression_tag_callback(data);
            } else if (gubun == "submit_compression_tag") {
            	submit_compression_tag_callback();
            } else if (gubun == "delete_compression_tag") {
            	delete_compression_tag_callback();
            } else if (gubun == "get_training_info") {
            	get_training_info_callback(data['training_info'], data['saving_step']);
            } else if (gubun == "delete_ckpt_file") {
            	delete_ckpt_file_callback();
            }
        	
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}

function search_compression_tag() {
	var subject = $("#subject").val();
	var user = $("#user").val();
	var project = $("#project").val();
	var input_data = {"subject" : subject, "user" : user, "project" : project};
	ajax('/search_compression_tag', input_data, 'search_compression_tag', 'POST');
}

function add_row() {
	var a = [];
	a.push(grid_data1.length + 1);
	a.push("");
	a.push("");
	a.push("");
	a.push("new");
	grid_data1.push(a);
	mygrid1.refresh(grid_data1);
}

function del_row() {
	var cur_row = $("#cur_row").val();
	if (cur_row == '') {
		alert("삭제할 열을 선택해 주세요.");
		return;
	}
	if ($("#compression_num").val() == '') {
		grid_data1.splice(cur_row, 1);
		mygrid1.refresh(grid_data1);
		return;
	}
	if (!confirm("삭제 하시겠습니까?")) {
		return;
	}
	var input_data = {"compression_num" : $("#compression_num").val(), "user" : $("#user").val(), "project" : $("#project").val()};
	ajax('/delete_compression_tag', input_data, 'delete_compression_tag', 'POST');
}

function submit_compression_tag() {
	mygrid1.endEdit();
	if (!confirm("저장 하시겠습니까?")) {
		return;
	}
	var input_data = [];
	for (var i = 0; i < grid_data1.length; ++i) {
		if (grid_data1[i][4] == "default")
			continue;
		var input = {};
		input["user"] = $("#user").val();
		input["project"] = $("#project").val();
		input["compression_num"] = grid_data1[i][1];
		input["expression"] = grid_data1[i][2]; 
		input["tag_name"] = grid_data1[i][3];
		input["data_type"] = grid_data1[i][4];
		input_data.push(input);
	}
	ajax('/submit_compression_tag', input_data, 'submit_compression_tag', 'POST');
}

function search_compression_tag_callback(retData) {
	grid_data1 = [];
	var retList = retData['results'];
	for (var i = 0; i < retList.length; ++i) {
		var a = [];
		a.push(i + 1);
		a.push(retList[i]['compression_num']);
		a.push(retList[i]['expression']);
		a.push(retList[i]['tag_name']);
		a.push("default");
		grid_data1.push(a);
	}
	mygrid1.refresh(grid_data1);
	mygrid1.gotoPage(1);
	$("#cur_row").val('');
	$('#compression_tag_num').val('');
}

function submit_compression_tag_callback() {
	alert("저장 되었습니다.");
	search_compression_tag();
}

function delete_compression_tag_callback() {
	alert("삭제완료 처리되었습니다.");
	search_compression_tag();
}

function delete_ckpt_file() {
	if (!confirm("훈련모델을 삭제하시겠습니까?")) {
		return;
	}
	var user = $("#user").val();
	var project = $("#project").val();
	var input_data = {"user" : user, "project" : project};
	ajax('/delete_compression_tag_ckpt_file', input_data, 'delete_ckpt_file', 'POST');	
}

function start_training() {
	if (!confirm("훈련을 시작 하시겠습니까?")) {
		return;
	}
	$("#start_training").text("훈련중단");
	var user = $("#user").val();
	var project = $("#project").val();
	var saving_step = $("#saving_step").val();
	var input_data = {"user" : user, "project" : project, "saving_step" : saving_step};

	$.post('/start_compression_tag_training', input_data).done(function(reply) {
		alert("훈련이 시작되었습니다.");
		$('#training_info').text('훈련을 준비중입니다..');
		start_interval();
	}).fail(function() {
	});
}

function stop_training() {
	if (!confirm("훈련을 종료 하시겠습니까?")) {
		return;
	}
	$("#start_training").text("훈련시작");	
	var user = $("#user").val();
	var project = $("#project").val();
	var input_data = {"user" : user, "project" : project};
	
	$.post('/stop_compression_tag_training', input_data).done(function(reply) {
		alert("훈련이 중단되었습니다.");
		$('#training_info').text('');
		$('#show_testing').hide();
		stop_interval();
	}).fail(function() {
	});
}

function get_is_training() {
	var user = $("#user").val();
	var project = $("#project").val();
	$.post("/get_is_compression_tag_training", { user : user, project : project}).done(function(reply) {
		if (reply['is_training'] == 'Y') {
			$("#start_training").text('훈련중단');
			start_interval();
		} else {
			$("#start_training").text('훈련시작');
			stop_interval();
			$('#training_info').text('');
		}
	}).fail(function() {
	});
}

function get_training_info() {
	var user = $("#user").val();
	var project = $("#project").val();
	var input_data = {"user" : user, "project" : project};
	ajax('/get_compression_tag_training_info', input_data, 'get_training_info', 'POST');
}

function get_training_info_callback(training_info, saving_step) {
	if (training_info.indexOf("현재스텝") != -1) {
		$('#show_testing').show();
	} else {
		$('#show_testing').hide();
	}
	$('#training_info').html(training_info.replace(/,/gi, '<br>'))
	$('#saving_step').val(saving_step)
}

function delete_ckpt_file_callback() {
	alert("훈련모델이 삭제되었습니다.");
}

var interval_name = '';
var interval_name_is_training = '';

function start_interval() {
	if (interval_name == '') {
		interval_name = setInterval(function() {get_training_info();}, 2000);
	}
}

function start_interval_is_training() {
	interval_name_is_training = setInterval(function() {get_is_training();}, 5000);
}

function stop_interval() {
	clearInterval(interval_name);
	interval_name = '';
}

function stop_interval_is_training() {
	clearInterval(interval_name_is_training);
}
