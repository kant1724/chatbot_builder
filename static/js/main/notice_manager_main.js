var grid_data1 = [];
var grid_demo_id1 = "myGrid1";

var dsOption1= {
	fields :[
		{name : 'num'  },
		{name : 'notice_num'  },
		{name : 'notice_subject'  },
		{name : 'notice_content'  },
		{name : 'image_cnt'  },
		{name : 'rgsn_date'  },
		{name : 'notice_start_date'  },
		{name : 'notice_end_date'  },
		{name : 'complete_yn'  }
	],
	recordType : 'array',
	data : grid_data1
}

var colsOption1 = [
	 {id: 'num' , header: "순번" , width :60 },
	 {id: 'notice_num' , header: "공지번호" , width :60 },
	 {id: 'notice_subject' , header: "공지제목" , width :200 },
	 {id: 'notice_content' , header: "공지내용" , width :340 },
	 {id: 'notice_start_date' , header: "공지시작일" , width :80 },
	 {id: 'notice_end_date' , header: "공지종료일" , width :80 },
	 {id: 'complete_yn' , header: "완료여부" , width :60 }
];

var gridOption1={
	id : grid_demo_id1,
	width: "900",
	height: "690",
	container : 'new_request_grid', 
	replaceContainer : true, 
	dataset : dsOption1 ,
	columns : colsOption1,
	pageSize: 30,
	toolbarContent : 'nav goto | pagesize | reload | print filter chart | state',
	pageSizeList : [30,40,60,80,100],
	skin : "mac",
	onRowClick:function(value, record, cell, row, colNO, rowNO, columnObj, grid) {
		var notice_num = record[1];
		$("#notice_num").val(notice_num);
	}
};

var mygrid1 = new Sigma.Grid(gridOption1);
Sigma.Util.onLoad(Sigma.Grid.render(mygrid1));

$(document).ready(function() {
	$("#search_notice").click(function() {
		search_notice();
	});
	$("#add_new_notice").click(function() {
		add_new_notice();
	});
	$("#modify_notice").click(function() {
		modify_notice();
	});
	$("#delete_notice").click(function() {
		delete_notice();
	});
	$("#submit_notice_complete").click(function() {
		submit_notice_complete();
	});
	$("#subject").keydown(function (key) {
        if (key.keyCode == 13) {
        	search_notice();
        }
    });
	search_notice();
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
        	if (gubun == "search_notice") {
        		search_notice_callback(data);
            } else if (gubun == "submit_notice_complete") {
            	submit_notice_complete_callback();
            } else if (gubun == "delete_notice") {
            	delete_notice_callback();
            }
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}

function add_new_notice() {
	var user = $("#user").val();
	var project = $("#project").val();
	var notice_num = $("#notice_num").val();
	var w = NEW_NOTICE_POPUP_WIDTH;
	var h = NEW_NOTICE_POPUP_HEIGHT;
	var x = (screen.width - w) / 2;
    var y = (screen.height - h) / 3;
	window.open('/new_notice_pop?user=' + user + '&project=' + project + '&gubun=new' + '&notice_num=' + notice_num, '_blank', 'scrollbars=yes, width=' + w + ', height=' + h + ', left=' + x + ', top=' + y);
}

function modify_notice() {
	if ($('#notice_num').val() == '') {
		alert("변경할 열을 선택하세요.");
		return;
	}
	var user = $("#user").val();
	var project = $("#project").val();
	var notice_num = $("#notice_num").val();
	var w = NEW_NOTICE_POPUP_WIDTH;
	var h = NEW_NOTICE_POPUP_HEIGHT;
	var x = (screen.width - w) / 2;
    var y = (screen.height - h) / 3;
	window.open('/new_notice_pop?user=' + user + '&project=' + project + '&gubun=modify' + '&notice_num=' + notice_num, '_blank', 'scrollbars=yes, width=' + w + ', height=' + h + ', left=' + x + ', top=' + y);
}

function search_notice() {
	var subject = $("#subject").val();
	var complete_yn = $("#complete_yn option:selected").val();
	var user = $("#user").val();
	var project = $("#project").val();
	var input_data = {"complete_yn" : complete_yn, "subject" : subject, "user" : user, "project" : project};
	ajax('/search_notice', input_data, 'search_notice', 'POST');
}

function delete_notice() {
	if ($('#notice_num').val() == '') {
		alert("삭제할 열을 선택하세요.");
		return;
	}
	if (!confirm("삭제 하시겠습니까?")) {
		return;
	}
	var user = $("#user").val();
	var project = $("#project").val();
	var notice_num = $("#notice_num").val();
	var input_data = {"user" : user, "project" : project, "notice_num" : notice_num};
	ajax('/delete_notice', input_data, 'delete_notice', 'POST');
}

function submit_notice_complete() {
	if ($('#notice_num').val() == '') {
		alert("공지완료할 열을 선택하세요.");
		return;
	}
	if (!confirm("공지완료 하시겠습니까?")) {
		return;
	}
	var user = $("#user").val();
	var project = $("#project").val();
	var notice_num = $("#notice_num").val();
	var input_data = {"user" : user, "project" : project, "notice_num" : notice_num};
	ajax('/submit_notice_complete', input_data, 'submit_notice_complete', 'POST');
}

function search_notice_callback(retData) {
	dataArr = [];
	var retList = retData['results'];
	for (var i = 0; i < retList.length; ++i) {
		var a = [];
		a.push(i + 1);
		a.push(retList[i]['notice_num']);
		a.push(retList[i]['notice_subject']);
		a.push(retList[i]['notice_content']);
		a.push(retList[i]['image_cnt']);
		a.push(retList[i]['rgsn_date']);
		a.push(retList[i]['notice_start_date']);
		a.push(retList[i]['notice_end_date']);
		if (retList[i]['complete_yn'] == "Y") {
			a.push("공지완료");
		} else {
			a.push("공지중");
		}
		dataArr.push(a);
	}
	mygrid1.refresh(dataArr);
	mygrid1.gotoPage(1);
	$('#notice_num').val('');
}

function submit_notice_complete_callback() {
	alert("공지완료 처리되었습니다.");
	search_notice();
}

function delete_notice_callback() {
	alert("삭제완료 처리되었습니다.");
	search_notice();
}
