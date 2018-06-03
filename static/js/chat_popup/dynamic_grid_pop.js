var grid_data1 = [];
var grid_demo_id1 = "myGrid1";

var dsOption1 = {
	fields :[
	],
	recordType : 'array',
	data : grid_data1
}

var colsOption1 = [	 
];

var gridOption1={
	id : grid_demo_id1,
	height: "450",
	container : 'dynamic_data_grid', 
	replaceContainer : true, 
	dataset : dsOption1 ,
	columns : colsOption1,
	pageSize: 20000,
	remoteSort: true,
	toolbarContent : 'nav goto | pagesize | reload | print filter chart | state',
	pageSizeList : [20000],
	onRowClick:function(value, record, cell, row, colNO, rowNO, columnObj, grid) {		
	}
};

var param_holder = {};
$(document).ready(function() {
	param_holder = JSON.parse($('#param_holder').val().replace(/\'/g, '\"'));
	$('#dynamic_title').text($('#title').val())
	var column_info = eval($('#column_info').val());
	var content = eval($('#content').val());
	var width = 0;
	for (var i = 0; i < column_info.length; ++i) {
		var col = {id : column_info[i][0], header : column_info[i][1], width : column_info[i][2]};
		var ds = {name : column_info[i][0]};
		dsOption1['fields'].push(ds); 
		colsOption1.push(col);
		width += Number(column_info[i][2]);
	}
	width += 30
	gridOption1['width'] = Math.min(width, 920);
	for (var i = 0; i < content.length; ++i) {
		var d = [];
		for (var j = 0; j < content[i].length; ++j) {
			d.push(content[i][j]);				
		}
		grid_data1.push(d)
	}
	var mygrid1 = new Sigma.Grid(gridOption1);
	Sigma.Util.onLoad(Sigma.Grid.render(mygrid1));
	
	$("#question").keydown(function (key) {
        if (key.keyCode == 13) {        	
        	get_more_info($("#question").val());
        }
    });
});

function get_more_info(question){
	$.post('/reply_dynamic_popup', {
		user : $('#user').val(),
		project : $('#project').val(),
		msg: question,
		param_holder : JSON.stringify(param_holder)
	}).done(function(reply) {
	    var answer = reply['text'];	    
	    if (answer == '') {
	    	return;
	    }
	    answer = eval(answer);
	    var title = answer[0];
	    var column_info = JSON.stringify(answer[1]);
	    var content = JSON.stringify(answer[2]);
	    $("#dynamic_grid_user").val($('#user').val());
		$("#dynamic_grid_project").val($('#project').val());
		$("#dynamic_grid_param_holder").val(JSON.stringify(param_holder));
		$("#dynamic_grid_title").val(title);
	    $("#dynamic_grid_column_info").val(column_info);
		$("#dynamic_grid_content").val(content);
		
		$("#form_dynamic_grid_pop").submit();
	    
	}).fail(function() {
	});
}
