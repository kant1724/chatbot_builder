# chatbot_builder
Korean Chatbot Build Platform
```
python build.py
```

## Chatbot Platform
this chatbot platform to build chatbot effeciently.

1. training session : you can train chatbot online, while training is in progress, you can test how much the bot is trained
2. running session : when you runs chatbot, it lets you find the right question by automatic question making function.
3. web builder : you can register and test vocabulary, synonym, sentence fragment, wrong answer, etc.. and everything is used to
enhance the accuracy of answers and comfort of users.

# requirement
it needs to interface with chatbot_tf, chatbot_file, chatbot_external_adapter, group_chat for integration.
1. chatbot_tf : using google tensorflow, builder engine only requests multi dimention matrix to chatbot_tf server. and it only gets response in form of the same type of input data with different value.

2. chatbot_file : when chatbot needs to print image or file, it requires file data from chatbot_file server. when does training, it also sends request to get training-related data from chatbot_file server.

3. chatbot_extenal_adapter : when the chatbot needs to interface with other systems, it can do it by using external adapter.

4. group_chat : multi-to-one (multi people to one A.I) conversion can be done by entering the group chat server.
