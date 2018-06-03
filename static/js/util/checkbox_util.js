function is_grid_checked(cell) {
	var htmlstr = $(cell.innerHTML).html();
	var parsed = $.parseHTML(htmlstr)
	var value = $(parsed).val();
	var name = $(parsed).attr("name");
	var res = $('input[name=' + name + '][value=' + value + ']').is(":checked");
	return res;
}
