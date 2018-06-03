function highlight(content, word_arr, spanClass) {
	word_arr.sort(function(a, b){
		return b.length - a.length;
	});
	var highlighted = content;
	for (var i = 0; i < word_arr.length; ++i) {
		var prefix = '<span ' + (spanClass ? 'class="' + spanClass + '"' : '') + '">';
		var suffix = '</span>';
		var replaceWith = prefix + word_arr[i] + suffix;
		highlighted = highlighted.replace(word_arr[i], replaceWith, "g");
		for (var j = 0; j < word_arr[i].length; ++j) {
			var left = word_arr[i].substring(0, j)
			var right = word_arr[i].substring(j, word_arr[i].length);
			var full = left + prefix + right;
			replaceWith = prefix + word_arr[i];
			highlighted = highlighted.replace(full, replaceWith, "g");
		}
		for (var j = 0; j < word_arr[i].length; ++j) {
			var left = word_arr[i].substring(0, j)
			var right = word_arr[i].substring(j, word_arr[i].length);
			var full = left + suffix + right;
			replaceWith = word_arr[i] + suffix;
			highlighted = highlighted.replace(full, replaceWith, "g");
		}
	}
	
    return highlighted;
}
