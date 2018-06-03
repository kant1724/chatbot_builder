$(document).ready(function() {
	var column_info = eval($('#column_info').val());
	var content = eval($('#content').val());
	for (var i = 0; i < column_info.length; ++i) {
		var col = {id : column_info[i][0], header : column_info[i][1], width : column_info[i][2]};
		var ds = {name : column_info[i][0]};
		dsOption1['fields'].push(ds); 
		colsOption1.push(col);
	}
	for (var i = 0; i < content.length; ++i) {
		var d = [];
		for (var j = 0; j < content[i].length; ++j) {
			d.push(content[i][j]);				
		}
		grid_data1.push(d)
	}
});
