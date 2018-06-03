var grid_data1 = [];
var grid_demo_id1 = "myGrid1";

var dsOption1= {
	fields :[
		{name : 'num'  },
		{name : 'voca_nm'  },
		{name : 'appearance_count'  },
		{name : 'voca_weight'  }
		
	],
	recordType : 'array',
	data : grid_data1
}

var colsOption1 = [
	 {id: 'num' , header: "순번" , width :60 },
	 {id: 'voca_nm' , header: "단어명" , width :400 },
	 {id: 'appearance_count' , header: "출현빈도" , width :200 },
	 {id: 'voca_weight' , header: "가중치" , width :200 }
];

var gridOption1={
	id : grid_demo_id1,
	width: "900",
	height: "534",
	container : 'voca_grid', 
	replaceContainer : true, 
	dataset : dsOption1 ,
	columns : colsOption1,
	pageSize: 22,
	toolbarContent : 'nav goto | pagesize | reload | print filter chart | state',
	pageSizeList : [22,44,70,100],
	skin : "mac"
};

var mygrid1 = new Sigma.Grid(gridOption1);
Sigma.Util.onLoad(Sigma.Grid.render(mygrid1));

$(document).ready(function() {
	get_updating_info();
	var is_updating = $("#is_updating").val();
	if (is_updating == 'Y') {
		$("#start_updating").text('업데이트중단');
		start_interval();
	}	
	$("#start_updating").click(function() {
		var updating_status = $("#start_updating").text();
		if (updating_status == "업데이트시작") {
			start_updating();
		} else {
			stop_updating();
		}
	});
	$("#search_voca_and_appearance").click(function() {
		search_voca_and_appearance();
	});
	$("#update_voca_synonym").click(function() {
		update_voca_synonym();
	});
	$("#subject").keydown(function (key) {
        if (key.keyCode == 13) {
        	search_voca_and_appearance();
        }
    });
	search_voca_and_appearance();
});
	
function ajax(url, input_data, gubun, method) {
	var as = false;
	if (gubun == 'start_updating') {
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
            if (gubun == "start_updating") {
            	start_updating_callback();
            } else if (gubun == "stop_updating") {
            	stop_updating_callback();
            } else if (gubun == "get_updating_info") {
            	get_updating_info_callback(data['updating_info'], data['end_yn']);
            } else if (gubun == "search_voca_and_appearance") {
            	search_voca_and_appearance_callback(data['results']);
            } else if (gubun == "update_voca_synonym") {
            	update_voca_synonym_callback();
            }
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}

function update_voca_synonym() {
	if (!confirm("동의어를 업데이트 하시겠습니까?")) {
		return;
	}
	var input_data = {};
	ajax('/update_voca_synonym', input_data, 'update_voca_synonym', 'POST');
}

function start_updating() {
	if (!confirm("업데이트를 시작 하시겠습니까?")) {
		return;
	}
	$("#start_updating").text("업데이트중단");
	var input_data = {};
	var user = $("#user").val();
	var project = $("#project").val();
	ajax('/start_updating?user=' + user + '&project=' + project, input_data, 'start_updating', 'GET');
}

function stop_updating() {
	if (!confirm("업데이트를 중단 하시겠습니까?")) {
		return;
	}
	$("#start_updating").text("업데이트시작");
	var input_data = {};
	var user = $("#user").val();
	var project = $("#project").val();
	ajax('/stop_updating?user=' + user + '&project=' + project, input_data, 'stop_updating', 'GET');
}

function get_updating_info() {
	var input_data = {};
	var user = $("#user").val();
	var project = $("#project").val();
	var input_data = {};
	ajax('/get_updating_info?user=' + user + '&project=' + project, input_data, 'get_updating_info', 'POST');
}

function get_updating_info_callback(updating_info, end_yn) {
	$('#updating_info').text(updating_info);
	if (end_yn == "Y") {
		$("#start_updating").text("업데이트시작");
	}
}

function start_updating_callback() {
	alert("업데이트가 시작되었습니다.");
	$('#updating_info').text('업데이트 중입니다.');
	start_interval();
}

function stop_updating_callback() {
	alert("업데이트가 중단되었습니다.");
	get_updating_info();
	stop_interval();
}

function update_voca_synonym_callback() {
	alert("업데이트 작업이 완료되었습니다.");
	search_voca();
}

var interval_name = ''

function start_interval() {
	interval_name = setInterval(function() {get_updating_info();}, 1000);
}

function stop_interval() {
	clearInterval(interval_name);
}

function search_voca_and_appearance() {
	var user = $("#user").val();
	var project = $("#project").val();
	var gubun = $("#gubun option:selected").val();
	var subject = $("#subject").val();
	var weight_parameter = $("#weight_parameter").val();
	var input_data = {"user" : user, "project" : project, "gubun" : gubun, "subject" : subject, "weight_parameter" : weight_parameter};
	ajax('/search_voca_and_appearance', input_data, 'search_voca_and_appearance', 'POST');
}

function search_voca_and_appearance_callback(ret_data) {
	grid_data1 = [];
	for (var i = 0; i < ret_data.length; i++) {
		var a = [];
		a.push(i + 1);
		a.push(ret_data[i]["voca_nm"]);
		a.push(ret_data[i]["appearance_count"]);
		a.push(ret_data[i]["voca_weight"]);
		grid_data1.push(a);
	}
	mygrid1.refresh(grid_data1);
	mygrid1.gotoPage(1);
}
