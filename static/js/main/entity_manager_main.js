var grid_data1 = [];
var grid_demo_id1 = "myGrid1";

var dsOption1= {
	fields :[
		{name : 'num'  },
		{name : 'entity_nm'  }		
	],
	recordType : 'array',
	data : grid_data1
}

var colsOption1 = [
	 {id: 'num' , header: "순번" , width :60 },
	 {id: 'entity_nm' , header: "엔티티명" , width :800 }
];

var gridOption1={
	id : grid_demo_id1,
	width: "900",
	height: "644",
	container : 'entity_grid', 
	replaceContainer : true, 
	dataset : dsOption1 ,
	columns : colsOption1,
	pageSize: 27,
	toolbarContent : 'nav goto | pagesize | reload | print filter chart | state',
	pageSizeList : [27,54,80,100],
	skin : "mac",
	onRowClick:function(value, record, cell, row, colNO, rowNO, columnObj, grid) {
		var entity_nm = record[1];
		$("#entity_nm").val(entity_nm);
	}
};

var mygrid1 = new Sigma.Grid(gridOption1);
Sigma.Util.onLoad(Sigma.Grid.render(mygrid1));

$(document).ready(function() {
	$("#search_entity").click(function() {
		search_entity();
	});
	$("#new_entity").click(function() {
		new_entity();
	});
	$("#submit_entity").click(function() {
		submit_entity();
	});
	$("#delete_entity").click(function() {
		delete_entity();
	});
	$("#subject").keydown(function (key) {
        if (key.keyCode == 13) {
        	search_entity();
        }
    });
	search_entity();
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
        	if (gubun == "search_entity") {
        		search_entity_callback(data['results']);
            } else if (gubun == "submit_entity") {
            	submit_entity_callback(data);
            } else if (gubun == "delete_entity") {
            	delete_entity_callback();
            }
        },
        error: function (jqXhr, textStatus, errorMessage) {
        	if(jqXhr.status==404) {
        		alert(textStatus);
            }
        }
    });
}

function search_entity() {
	var input_data = {"entity_nm" : $('#subject').val()};
	ajax('/search_entity', input_data, 'search_entity', 'POST');
}

function search_entity_callback(ret_data) {
	grid_data1 = [];
	for (var i = 0; i < ret_data.length; i++) {
		var a = [];
		a.push(i + 1);
		a.push(ret_data[i]["entity_nm"]);
		grid_data1.push(a);
	}
	mygrid1.refresh(grid_data1);
	mygrid1.gotoPage(1);
	$("#entity_nm").val('');
}

function submit_entity() {
	if ($("#entity_input").val() == '') {
		alert("엔티티명을 입력하세요.");
		return;
	}
	if (!confirm("저장 하시겠습니까?")) {
		return;
	}
	var input_data = {"entity_nm" : $("#entity_input").val()};
	
	ajax('/submit_entity', input_data, 'submit_entity', 'POST');
}

function delete_entity() {
	if ($("#entity_nm").val() == '') {
		alert("삭제할 엔티티를 선택하세요.");
		return;
	}
	if (!confirm("삭제 하시겠습니까?")) {
		return;
	}
	var input_data = {"entity_nm" : $("#entity_nm").val()};
	ajax('/delete_entity', input_data, 'delete_entity', 'POST');
}

function submit_entity_callback(data) {
	if (data == 'N') {
		alert("이미 등록된 단어입니다.");
	} else {
		alert("엔티티가 저장되었습니다.");
	}
	search_entity();
}

function delete_entity_callback() {
	alert("삭제가 완료되었습니다.");
	search_entity();
}
