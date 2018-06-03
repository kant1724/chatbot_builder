function getSelectedText() {
	var selectedText = '';
	if (window.getSelection) {  // all browsers, except IE before version 9
		if (document.activeElement &&
				(document.activeElement.tagName.toLowerCase() == "textarea" ||
				 document.activeElement.tagName.toLowerCase() == "input")) {
			var text = document.activeElement.value;
			selectedText = text.substring(document.activeElement.selectionStart,
	                                     document.activeElement.selectionEnd);
		} else {
			var selRange = window.getSelection();
			selectedText = selRange.toString();
		}
	} else {
		if (document.selection.createRange) { // Internet Explorer
			var range = document.selection.createRange();
			selectedText = range.text;
		}
	}
	return selectedText;
}

function getSelectedRange() {
	return [document.activeElement.selectionStart, document.activeElement.selectionEnd];
}

function char_tokenizer(sentence, exception) {
	var words = [];
	var i = 0;
	while (i < sentence.length) {
		var c = sentence.charAt(i);
		var except = false;
		for (var j = 0; j < exception.length; ++j) {
			if (c == exception[j]) {
				except = true;
			}
		}
		if (except) {
			i += 1;
			continue;
		}
		if (!isNaN(Number(c))) {
			num = "";
			while (i < sentence.length && !isNaN(sentence.charAt(i))) {
				num += sentence.charAt(i);
				i += 1;
			}
			words.push(num.replace('\n', ''));
		} else {
			if (!except) {
				words.push(sentence[i].replace('\n', ''));
			}
			i += 1;
		}
	}
	return words;
}

function replaceSelectedText(txtarea) {
    var prefix = '<a style="color:red;font-weight:700;">';
    var suffix = '</a>';
    var start = txtarea.prop("selectionStart");
    var end = txtarea.prop("selectionEnd");
    var left = txtarea.val().substring(0, start);
    var right = txtarea.val().substring(end, txtarea.val().length);
    var selected = txtarea.val().substring(start, end);
    if (selected == '') {
    	return;
    }
    txtarea.val(left + prefix + selected + suffix + right);
}
