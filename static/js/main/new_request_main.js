var grid_data1 = [];
var grid_demo_id1 = "myGrid1";

var dsOption1= {
	fields :[
		{name : 'num'  },
		{name : 'rq_num'  },
		{name : 'user_ip'  },
		{name : 'question'  },
		{name : 'rgsn_date'  },
		{name : 'rgsn_time'  },
		{name : 'recommend_cnt'  },
		{name : 'answer'  },
		{name : 'pc_status'  }
	],
	recordType : 'array',
	data : grid_data1
}

var colsOption1 = [
	 {id: 'num' , header: "순번" , width :40 }, 
	 {id: 'question' , header: "요청질문" , width :300 },
	 {id: 'rgsn_date' , header: "요청일자" , width :70 },
	 {id: 'rgsn_time' , header: "요청시간" , width :60 },
	 {id: 'recommend_cnt' , header: "추천수" , width :40 },
	 {id: 'answer' , header: "등록답변" , width :300 }, 
	 {id: 'pc_status' , header: "처리상태" , width :70 }
];

var gridOption1={
	id : grid_demo_id1,
	width: "900",
	height: "710",
	container : 'new_request_grid', 
	replaceContainer : true, 
	dataset : dsOption1 ,
	columns : colsOption1,
	pageSize: 30,
	toolbarContent : 'nav goto | pagesize | reload | print filter chart | state',
	pageSizeList : [30,40,60,80,100],
	skin : "mac",
	onRowClick:function(value, record, cell, row, colNO, rowNO, columnObj, grid) {
		var rq_num = record[1];
		$("#rq_num").val(rq_num);
	}
};

var mygrid1 = new Sigma.Grid(gridOption1);
Sigma.Util.onLoad(Sigma.Grid.render(mygrid1));

$(document).ready(function() {
	$("#search_new_request").click(function() {
		search_new_request();
	});
	$("#new_answer_pop").click(function() {
		new_answer_pop();
	});
	$("#submit_complete_request").click(function() {
		submit_complete_request();
	});
	$("#subject").keydown(function (key) {
        if (key.keyCode == 13) {
        	search_new_request();
        }
    });
	search_new_request();
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
        	if (gubun == "search_new_request") {
        		search_new_request_callback(data);
            } else if (gubun == "submit_complete_request") {
            	submit_complete_request_callback();
            }
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}

function search_new_request() {
	var subject = $("#subject").val();
	var pc_status = $("#pc_status").val();
	var user = $("#user").val();
	var project = $("#project").val();
	var input_data = {"pc_status" : pc_status, "subject" : subject, "user" : user, "project" : project};
	ajax('/search_new_request', input_data, 'search_new_request', 'POST');
}

function new_answer_pop() {
	if ($("#rq_num").val() == '') {
		alert("답변등록할 열을 선택하세요.");
		return;
	}
	var user = $("#user").val();
	var project = $("#project").val();
	var rq_num = $("#rq_num").val();
	var w = NEW_ANSWER_POPUP_WIDTH;
	var h = NEW_ANSWER_POPUP_HEIGHT;
	var x = (screen.width - w) / 2;
    var y = (screen.height - h) / 3;
	window.open('/new_answer_pop?user=' + user + '&project=' + project + '&rq_num=' + rq_num, '_blank', 'scrollbars=yes, width=' + w + ', height=' + h + ', left=' + x + ', top=' + y);
}

function submit_complete_request() {
	if ($("#rq_num").val() == '') {
		alert("처리완료할 열을 선택하세요.");
		return;
	}
	if (!confirm("처리완료 하시겠습니까?")) {
		return;
	}
	var subject = "";
	var user = $("#user").val();
	var project = $("#project").val();
	var rq_num = $("#rq_num").val();
	var input_data = {"user" : user, "project" : project, "rq_num" : rq_num};
	ajax('/submit_complete_request', input_data, 'submit_complete_request', 'POST');
}

function search_new_request_callback(retData) {
	dataArr = [];
	var retList = retData['results'];
	for (var i = 0; i < retList.length; ++i) {
		var a = [];
		a.push(i + 1);
		a.push(retList[i]['rq_num']);
		a.push(retList[i]['user_ip']);
		a.push(retList[i]['question']);
		a.push(retList[i]['rgsn_date']);
		a.push(retList[i]['rgsn_time']);
		a.push(retList[i]['recommend_cnt']);
		a.push(retList[i]['answer']);
		if (retList[i]['pc_status'] == "01") {
			a.push("요청");
		} else {
			a.push("처리완료");
		}
		dataArr.push(a);
	}
	mygrid1.refresh(dataArr);
	mygrid1.gotoPage(1);
	$("#rq_num").val('');
}

function submit_complete_request_callback() {
	alert("처리가 완료되었습니다.");
	search_new_request();
}
