var grid_data1 = [[]];
var grid_data2 = [[]];
var grid_demo_id1 = "myGrid1";
var grid_demo_id2 = "myGrid2";

var dsOption1= {
	fields :[
		{name : 'num'  },
		{name : 'rpsn_question'  },
		{name : 'answer'  },
		{name : 'answer_num'  },
		{name : 'category_nm'  },
		{name : 'image_cnt'  },
		{name : 'rgsn_user'  }
	],
	recordType : 'array',
	data : grid_data1
}

var dsOption2= {
	fields :[
		{name : 'answer_num'  },
		{name : 'question_srno'  },
		{name : 'question'  },
		{name : 'bucket_id'  },
		{name : 'question_voca'  }
	],
	recordType : 'array',
	data : grid_data2
}

var colsOption1 = [
	 {id: 'num' , header: "순번" , width :30 }, 
	 {id: 'rpsn_question' , header: "대표질문" , width :370 },
	 {id: 'answer' , header: "답변" , width :380, toolTip : true, toolTipWidth : 350},
	 {id: 'answer_num' , header: "답변번호" , width :55 },
	 {id: 'category_nm' , header: "분류명" , width :100 },
	 {id: 'image_cnt' , header: "이미지" , width :50 },
	 {id: 'rgsn_user' , header: "등록자" , width :70 }
];

var colsOption2 = [
	 {id: 'answer_num' , header: "답변번호" , width :55 },
	 {id: 'question_srno' , header: "질문번호" , width :55 },
	 {id: 'question' , header: "질문" , width :410 },
	 {id: 'bucket_id' , header: "버킷ID" , width :80 },
	 {id: 'question_voca' , header: "추출단어목록" , width :400 }
];

var gridOption1={
	id : grid_demo_id1,
	width: "900",
	height: "331",
	container : 'container', 
	replaceContainer : true, 
	dataset : dsOption1 ,
	columns : colsOption1,
	pageSize: 12,
	toolbarContent : 'nav goto | pagesize | reload | print filter chart | state',
	pageSizeList : [12,24,36,48,100],
	skin : "mac",
	onRowClick:function(value, record, cell, row, colNO, rowNO, columnObj, grid) {
		var rpsn_question = record[1];
		$("#rpsn_question").val(rpsn_question);
		var answer = record[2];
		$("#answer").val(answer);
		var answer_num = record[3];
		$("#answer_num").val(answer_num);
		search_question(answer_num);
	},
	onMouseOver:function(value, record, cell, row, colNo, rowNo, columnObj, grid) {
		if (columnObj && columnObj.toolTip) {
			grid.showCellToolTip(cell,columnObj.toolTipWidth);
		} else {
			grid.hideCellToolTip();
		}
	}
};

var gridOption2={
	id : grid_demo_id2,
	width: "900",
	height: "331",
	container : 'container2', 
	replaceContainer : true, 
	dataset : dsOption2 ,
	columns : colsOption2,
	pageSize: 12,
	toolbarContent : 'nav goto | pagesize | reload | print filter chart | state',
	pageSizeList : [12,24,36,48,100],
	skin : "mac",
	onRowClick:function(value, record , cell, row, colNO, rowNO, columnObj, grid){
		var question_srno = record[1];
		$("#question_srno").val(question_srno);
	}
};

var mygrid1 = new Sigma.Grid(gridOption1);
var mygrid2 = new Sigma.Grid(gridOption2);
Sigma.Util.onLoad(Sigma.Grid.render(mygrid1));
Sigma.Util.onLoad(Sigma.Grid.render(mygrid2));
$(document).ready(function() {
	$("#easy_manager_pop").click(function() {
		easy_manager_pop();
	});
	$("#search_answer").click(function() {
		search_answer();
	});
	$("#search_question").click(function() {
		search_question();
	});
	$("#new_answer_pop").click(function() {
		new_answer_pop();
	});
	$("#new_function_pop").click(function() {
		new_function_pop();
	});
	$("#new_question_pop").click(function() {
		new_question_pop();
	});
	$("#add_image_pop").click(function() {
		add_image_pop();
	});
	$("#multiple_answer_pop").click(function() {
		multiple_answer_pop();
	});
	$("#modify_answer_pop").click(function() {
		modify_answer_pop();
	});
	$("#delete_answer").click(function() {
		delete_answer();
	});
	$("#subject").keydown(function (key) {
        if (key.keyCode == 13) {
        	search_answer();
        }
    });
	$("#delete_question").click(function() {
		delete_question();
	});
	$("#update_question_voca_pop").click(function() {
		update_question_voca_pop();
	});
	$("#submit_voca").click(function() {
		submit_voca();
	});
	$("#update_question_voca").click(function() {
		update_question_voca();
	});
	
	search_answer();
});

function search_answer() {
	var gubun = $("#gubun option:selected").val();
	var subject = $("#subject").val();
	var user = $("#user").val();
	var project = $("#project").val();
	var input_data = {"gubun" : gubun, "subject" : subject, "user" : user, "project" : project};
	
	ajax('/search_answer', input_data, 'search_answer', 'POST');
}

function search_question(answer_num) {
	var user = $("#user").val();
	var project = $("#project").val();
	var answer_num = $("#answer_num").val();
	var input_data = {"answer_num" : answer_num, "user" : user, "project" : project};
	
	ajax('/search_question', input_data, 'search_question', 'POST');
}

function search_answer_callback(retData) {
	dataArr = [];
	var retList = retData['results'];
	for (var i = 0; i < retList.length; ++i) {
		var a = [];
		a.push(i + 1);
		a.push(retList[i]['rpsn_question']);
		a.push(retList[i]['answer']);
		a.push(retList[i]['answer_num']);
		a.push(retList[i]['category_nm']);
		a.push(retList[i]['image_cnt']);
		a.push(retList[i]['rgsn_user']);
		dataArr.push(a);
	}
	mygrid1.refresh(dataArr);
	mygrid1.gotoPage(1);
	$("#rpsn_question").val('');
	$("#answer").val('');
	$("#answer_num").val('');
}

function search_question_callback(retData) {
	dataArr = [];
	var retList = retData['results'];
	for (var i = 0; i < retList.length; ++i) {
		var a = [];
		a.push(retList[i]['answer_num']);
		a.push(retList[i]['question_srno']);
		if (retList[i]['question_voca'] == null) {
			retList[i]['question_voca'] = '';
		}
		var question_voca_arr = retList[i]['question_voca'].replace(/\^/g, ";").split(";");
		var question = highlight(retList[i]['question'], question_voca_arr, "text-highlight");
		a.push(question);
		a.push(retList[i]['bucket_id']);
		a.push(retList[i]['question_voca']);
		dataArr.push(a);
	}
	mygrid2.refresh(dataArr);
	mygrid2.gotoPage(1);
	$("#question_srno").val('');
}

function delete_answer_callback() {
	alert("삭제가 완료되었습니다.");
	search_answer();
}

function delete_question_callback() {
	alert("삭제가 완료되었습니다.");
	search_question();
}

function submit_voca_callback(data) {
	if (data == 'N') {
		alert("이미 등록된 단어입니다.");
	} else {
		alert("단어가 저장되었습니다.");
	}
}

function update_question_voca_callback() {
	alert("단어추출이 완료되었습니다.");
	search_question();
}

function easy_manager_pop() {
	var user = $("#user").val();
	var project = $("#project").val();
	var w = EASY_MANAGER_POPUP_WIDTH;
	var h = EASY_MANAGER_POPUP_HEIGHT;
	var x = (screen.width - w) / 2;
    var y = (screen.height - h) / 3;
	window.open('/easy_manager_pop?user=' + user + '&project=' + project, '_blank', 'scrollbars=yes, width=' + w + ', height=' + h + ', left=' + x + ', top=' + y);
}

function new_answer_pop() {
	var user = $("#user").val();
	var project = $("#project").val();
	var w = NEW_ANSWER_POPUP_WIDTH;
	var h = NEW_ANSWER_POPUP_HEIGHT;
	var x = (screen.width - w) / 2;
    var y = (screen.height - h) / 3;
	window.open('/new_answer_pop?user=' + user + '&project=' + project, '_blank', 'scrollbars=yes, width=' + w + ', height=' + h + ', left=' + x + ', top=' + y);
}

function new_function_pop() {
	var user = $("#user").val();
	var project = $("#project").val();
	var w = NEW_FUNCTION_POPUP_WIDTH;
	var h = NEW_FUNCTION_POPUP_HEIGHT;
	var x = (screen.width - w) / 2;
    var y = (screen.height - h) / 3;
	window.open('/new_function_pop?user=' + user + '&project=' + project, '_blank', 'scrollbars=yes, width=' + w + ', height=' + h + ', left=' + x + ', top=' + y);
}

function new_question_pop() {
	var user = $("#user").val();
	var project = $("#project").val();
	var w = NEW_QUESTION_POPUP_WIDTH;
	var h = NEW_QUESTION_POPUP_HEIGHT;
	var x = (screen.width - w) / 2;
    var y = (screen.height - h) / 3;
	var answer_num = $("#answer_num").val();
	if (answer_num == '') {
		alert("답변목록을 선택하세요.");
		return;
	}
	window.open('/new_question_pop?user=' + user + '&project=' + project + '&answer_num=' + answer_num, '_blank', 'scrollbars=yes, width=' + w + ', height=' + h + ', left=' + x + ', top=' + y);
}

function add_image_pop() {
	var user = $("#user").val();
	var project = $("#project").val();
	var w = ADD_IMAGE_POPUP_WIDTH;
	var h = ADD_IMAGE_POPUP_HEIGHT;
	var x = (screen.width - w) / 2;
    var y = (screen.height - h) / 3;
	var answer_num = $("#answer_num").val();
	if (answer_num == '') {
		alert("답변목록을 선택하세요.");
		return;
	}
	window.open('/add_image_pop?user=' + user + '&project=' + project + '&answer_num=' + answer_num, '_blank', 'scrollbars=yes, width=' + w + ', height=' + h + ', left=' + x + ', top=' + y);
}

function multiple_answer_pop() {
	var w = MULTIPLE_ANSWER_POPUP_WIDTH;
	var h = MULTIPLE_ANSWER_POPUP_HEIGHT;
	var y = window.top.outerHeight / 2 + window.top.screenY - ( h / 2);
	var x = window.top.outerWidth / 2 + window.top.screenX - ( w / 2);
	var user = $("#user").val();
	var project = $("#project").val();
	var answer_num = $("#answer_num").val();
	
	window.open('/multiple_answer_pop?user=' + user + '&project=' + project + '&answer_num=' + answer_num, '_blank', 'width=' + w + ', height=' + h + ', left=' + x + ', top=' + y);
}

function modify_answer_pop() {
	var user = $("#user").val();
	var project = $("#project").val();
	var w = MODIFY_ANSWER_POPUP_WIDTH;
	var h = MODIFY_ANSWER_POPUP_HEIGHT;
	var x = (screen.width - w) / 2;
    var y = (screen.height - h) / 3;
	var answer_num = $("#answer_num").val();
	var rpsn_question = $("#rpsn_question").val();
	var answer = $("#answer").val();
	if (answer_num == '') {
		alert("답변목록을 선택하세요.");
		return;
	}
	$("#modify_user").val(user);
	$("#modify_project").val(project);
	$("#modify_answer_num").val(answer_num);
	$("#modify_answer").val(answer);
	$("#modify_rpsn_question").val(rpsn_question);
    window.open('', 'modify_popup', 'scrollbars=yes, width=' + w + ', height=' + h + ', left=' + x + ', top=' + y);
	$("#modify").submit();
}

function delete_answer() {
	if ($("#answer_num").val() == "") {
		alert("삭제대상을 선택하세요");
		return;
	}
	if (!confirm("삭제 하시겠습니까?")) {
		return;
	}
	var user = $("#user").val();
	var project = $("#project").val();
	var answer_num = $("#answer_num").val();
	var input_data = {"user" : user, "project" : project, "answer_num" : answer_num};
	
	ajax('delete_answer', input_data, 'delete_answer', 'POST');
}

function submit_voca() {
	var voca = getSelectedText().trim();
	if (voca == '') {
		alert("등록할 단어를 화면에서 드래그 하여 선택하세요.");
		return;
	}
	if (!confirm("단어를 등록 하시겠습니까?\n\n[단어명: " + voca + "]")) {
		return;
	}
	var input_data = {"voca_nm" : voca};
	
	ajax('/submit_voca', input_data, 'submit_voca', 'POST');
}

function update_question_voca() {
	var user = $("#user").val();
	var project = $("#project").val();
	var answer_num = $("#answer_num").val();
	var input_data = {"user" : user, "project" : project, "answer_num" : answer_num};
	if (answer_num == '') {
		alert("답변목록을 선택하세요.");
		return;
	}
	if (!confirm("단어를 추출 하시겠습니까?")) {
		return;
	}
	
	ajax('/update_question_voca', input_data, 'update_question_voca', 'POST');
}

function delete_question() {
	if ($("#answer_num").val() == "" || $("#question_srno").val() == "") {
		alert("삭제할 열을 선택하세요");
		return;
	}
	if (!confirm("삭제 하시겠습니까?")) {
		return;
	}
	var user = $("#user").val();
	var project = $("#project").val();
	var answer_num = $("#answer_num").val();
	var question_srno = $("#question_srno").val();
	var input_data = {"user" : user, "project" : project, "answer_num" : answer_num, "question_srno" : question_srno};
	
	ajax('delete_question', input_data, 'delete_question', 'POST');
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
            if (gubun == "search_answer") {
            	search_answer_callback(data);
            } else if (gubun == "search_question") {
            	search_question_callback(data);
            } else if (gubun == "delete_answer") {
            	delete_answer_callback();
            } else if (gubun == "delete_question") {
            	delete_question_callback();
            } else if (gubun == "submit_voca") {
            	submit_voca_callback(data);
            } else if (gubun == "update_question_voca") {
            	update_question_voca_callback();
            }
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}
