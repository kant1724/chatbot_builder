var chat = {
	messageToSend: '',
	init: function() {
		this.cacheDOM();
		this.bindEvents();
		this.render();
	},
	
	cacheDOM: function() {
		this.$chatHistory = $('.chat-history');
		this.$peopleList = $('.people-list').find('ul');
		this.$button = $('button');
		this.$textarea = $('#message-to-send');
		this.$chatHistoryList = this.$chatHistory.find('ul');
	},
	
	bindEvents: function() {
		this.$button.on('click', this.addMessage.bind(this));
		this.$textarea.on('keyup', this.addMessageEnter.bind(this));
	},
	
	render: function() {
		this.scrollToBottom();
		if (this.messageToSend.trim() !== '') {
			var html_template = '<li class="clearfix"><div class="message-data align-right"><span class="message-data-time" >' + this.getCurrentTime() + ', Today</span> &nbsp; &nbsp;';
				html_template += '<span class="message-data-name" >나</span> <i class="fa fa-circle me"></i></div>';
				html_template += '<div class="message other-message float-right">' + this.messageToSend + '</div></li>'
	    	
			this.$chatHistoryList.append(html_template);
	        this.scrollToBottom();
	        this.$textarea.val('');
		}
	},
	
	render_others: function(message) {
		var html_template = '<li><div class="message-data"><span class="message-data-name"><i class="fa fa-circle online"></i>상대방</span>';
			html_template += '<span class="message-data-time">' + this.getCurrentTime() + ', Today</span></div><div class="message my-message">';
			html_template += message + '</div></li>'
		this.$chatHistoryList.append(html_template);
		this.scrollToBottom();
	},
	
	add_person: function (name) {
		var html_template = '<li class="clearfix"><div class="about"><div class="name">' + name + '</div>';
			html_template += '<div class="status"><i class="fa fa-circle online"></i> 온라인</div>';
			html_template += '</div></li>';
		this.$peopleList.append(html_template);
	},
	
	addMessage: function() {
		this.messageToSend = this.$textarea.val();
		send(this.$textarea.val());
		this.render();
	},
	
	addMessageEnter: function(event) {
		if (event.keyCode === 13) {
			if (this.$textarea.val().replace('\n', '').replace(' ', '') == '') {
				this.$textarea.val('');
				return;
			}
			this.addMessage();
	    }
	},
	
	scrollToBottom: function() {
		this.$chatHistory.scrollTop(this.$chatHistory[0].scrollHeight);
	},
	
	getCurrentTime: function() {
		return new Date().toLocaleTimeString().
	    	replace(/([\d]+:[\d]{2})(:[\d]{2})(.*)/, "$1$3");
	},
	
	getRandomItem: function(arr) {
		return arr[Math.floor(Math.random()*arr.length)];
	}
}

chat.init();

function send(message) {
	var send_data = {"message" : $('#emno').val() + ": " + message, "members" : ""};
	websocket.send(JSON.stringify(send_data));
	if (message.charAt(0) == '!') {
		interact(message.substring(1));
	}
}

function interact(message) {
	$.post('/message_group_chat', {
		user : $('#user').val(),
		project : $('#project').val(),
		msg: message
	}).done(function(reply) {
		var answer = "i-Learning: " + reply['answer'];
		chat.messageToSend = answer;
		chat.render_others(answer);
		var send_data = {"message" : answer, "members" : ""};
		websocket.send(JSON.stringify(send_data));
	}).fail(function() {
	});
}

window.addEventListener("load", init, false);

function init() {
	connect();
}

function connect() {
	websocket = new WebSocket("ws://" + $('#group_chat_ip').val());
	websocket.onopen = function(evt) { onOpen(evt) };
	websocket.onclose = function(evt) { onClose(evt) };
	websocket.onmessage = function(evt) { onMessage(evt) };
	websocket.onerror = function(evt) { onError(evt) };
	setTimeout(function() {
		var message = $('#emno').val() + "님이 대화방에 참여하였습니다.";
		var notice = "<br>대화의 첫 마디에 '!'를 붙여 챗봇에게 말을 걸어 보세요.<br>";
			notice += "예) !안녕하세요";
		chat.messageToSend = message.replace('$', '') + notice;
		var send_data = {"message" : message, "members" : ""};
		websocket.send(JSON.stringify(send_data));
		chat.render();
    }.bind(this), 1000);
}

function onOpen(evt) {
}

function onClose(evt) {
}

function onMessage(evt) {
	var data = eval(evt.data);
	var message = data[0];
	if (message != '') {
		chat.render_others(message);
	}
	var members = data[1].split(";");
	if (members != '') {
		chat.$peopleList.empty();
		for (var i = 0; i < members.length; ++i) {
			chat.add_person(members[i]);
		}
	}
}

function onError(evt) {
	websocket.close();
}

function doDisconnect() {
	websocket.close();
}
