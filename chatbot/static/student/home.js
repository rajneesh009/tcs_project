nlp = window.nlp_compromise;

var messages = [],
  lastUserMessage = "",
  botMessage = "",
  botName = 'Chatbot',
  userName = 'User'
  talking = true;


function chatbotResponse() {
  botMessage = "I'm confused"; //the default message

  if (lastUserMessage === 'hi') {
    botMessage = 'Hi there!';
  }
}


function newEntry() {
  if (document.getElementById("chatbox").value != "") {
    lastUserMessage = document.getElementById("chatbox").value;
    document.getElementById("chatbox").value = "";
    messages.push("<b>" + userName + ": </b>" + lastUserMessage);
    chatbotResponse();
    messages.push("<b>" + botName + ":</b> " + botMessage);
    for (var i = 1; i < 12; i++) {
      if (messages[messages.length - i])
      {
        document.getElementById("chatlog" + i).innerHTML = messages[messages.length - i];
       } 
    }
  }
}


//runs the keypress() function when a key is pressed
document.onkeypress = keyPress;
//if the key pressed is 'enter' runs the function newEntry()
function keyPress(e) {
  var x = e || window.event;
  var key = (x.keyCode || x.which);
  if (key == 13 || key == 3) {
    newEntry();
  }
}
