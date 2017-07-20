$(document).ready(function() {
      updateScroll();
    });

nlp = window.nlp_compromise;

var messages = [],
  lastUserMessage = "",
  botMessage = "",
  botName = 'Chatbot',
  userName = 'User'
  talking = true;

function printer_cricket(msg0,msg1,msg2) {
    document.getElementById("chatbox").value = "";
    messages.push("<div id='tooltip-left' style='display:none;'></div>");
    messages.push("<div id='tooltip-right'><b>" + botName + ": </b><br><b>Match 1 :</b>" + msg0 + "<br><b>Match 2 :</b>" + msg1 + "<br><b>Match 3 :</b>" +msg2 + "</div>");
    for (var i = 1; i < 120; i++) {
      if (messages[messages.length - i])
      {
        document.getElementById("chatlog" + i).innerHTML = messages[messages.length - i];
        updateScroll();
       } 
    }
}

function printer_football(msg0,msg1,msg2,msg3,msg4,msg5,msg6,msg7) {
    document.getElementById("chatbox").value = "";
    messages.push("<div id='tooltip-left' style='display:none;'></div>");
    messages.push("<div id='tooltip-right'><b>" + botName + ": </b><br><b>Match 1 :</b>" + "<br><u>Minutes</u> :" + msg0 + "<br><u>Teams</u> :" + msg1 + " vs " +msg3 + " <br><u>Score</u> : " +msg2 + "<br><b>Match 2 :</b>" + " <br><u>Minutes</u> : " + msg4 + " <br><u>Teams</u> : " +msg5 +" vs " +msg7 +"<br><u>Score</u> :" +msg6 + "</div>");
    for (var i = 1; i < 120; i++) {
      if (messages[messages.length - i])
      {
        document.getElementById("chatlog" + i).innerHTML = messages[messages.length - i];
        updateScroll();
       } 
    }
}

function printer_weather(msg0,msg1,msg2,msg3) {
    document.getElementById("chatbox").value = "";
    messages.push("<div id='tooltip-left' style='display:none;'></div>");
    messages.push("<div id='tooltip-right'><b>" + botName + ": </b><br><b>Temperature :</b>" + msg0 + " " + msg1 + "<br><b>Condition :</b>" + msg2 + "<br><b>Humidity :</b>" + msg3 + "</div>");
    for (var i = 1; i < 120; i++) {
      if (messages[messages.length - i])
      {
        document.getElementById("chatlog" + i).innerHTML = messages[messages.length - i];
        updateScroll();
       } 
    }
}

function printer_stock(msg0,msg1,msg2,msg3) {
    document.getElementById("chatbox").value = "";
    messages.push("<div id='tooltip-left' style='display:none;'></div>");
    messages.push("<div id='tooltip-right'><b>" + botName + ": </b><br><b>Nifty :</b>" + msg0 + "<br><b>Sensex :</b>" + msg1 + "<br><b>Gold :</b>" + "₹" + msg2 + " per 10 gms " + "<br><b>Silver :</b>" + "₹" + msg3 + " per 1 kg" + "</div>");
    for (var i = 1; i < 120; i++) {
      if (messages[messages.length - i])
      {
        document.getElementById("chatlog" + i).innerHTML = messages[messages.length - i];
        updateScroll();
       } 
    }
}

function printer_petrol(msg0,msg1,msg2) {
    document.getElementById("chatbox").value = "";
    messages.push("<div id='tooltip-left' style='display:none;'></div>");
    messages.push("<div id='tooltip-right'><b>" + botName + ": </b><br>" + msg0 + "<br>" + msg1 + "<br>" + msg2 + "</div>");
    for (var i = 1; i < 120; i++) {
      if (messages[messages.length - i])
      {
        document.getElementById("chatlog" + i).innerHTML = messages[messages.length - i];
        updateScroll();
       } 
    }
}

function cricket_score(){
    $.ajax({
        url: '/scrapingcricket/',
        type: 'GET',
        success : function(data) {
            printer_cricket(JSON.stringify(data.result['match3']),JSON.stringify(data.result['match1']),JSON.stringify(data.result['match2']));
        }
    })
} 

function football_score(){
    $.ajax({
        url: '/scrapingfootball/',
        type: 'GET',
        success : function(data) {
            printer_football(JSON.stringify(data.result['0']),JSON.stringify(data.result['1']),JSON.stringify(data.result['2']),JSON.stringify(data.result['3']),JSON.stringify(data.result['4']),JSON.stringify(data.result['5']),JSON.stringify(data.result['6']),JSON.stringify(data.result['7']));
        }
    })
} 

function weather(){
    $.ajax({
        url: '/scrapingweather/',
        type: 'GET',
        success : function(data) {
            printer_weather(JSON.stringify(data.result['temp']),JSON.stringify(data.result['unit']),JSON.stringify(data.result['Condition']),JSON.stringify(data.result['Humidity']));
        }
    })
} 

function stock(){
    $.ajax({
        url: '/scrapingstock/',
        type: 'GET',
        success : function(data) {
            printer_stock(JSON.stringify(data.result['nifty']),JSON.stringify(data.result['sensex']),JSON.stringify(data.result['gold']),JSON.stringify(data.result['silver']));
        }
    })
}

function petrol(){
    $.ajax({
        url: '/scrapingpetrol/',
        type: 'GET',
        success : function(data) {
            printer_petrol(JSON.stringify(data.result['petrol']),JSON.stringify(data.result['diesel']),JSON.stringify(data.result['cng']),JSON.stringify(data.result['silver']));
        }
    })
} 

function clear(){

  messages = [];
  for (var i = 1; i < 120; i++) 
      {
        document.getElementById("chatlog" + i).innerHTML = '&nbsp;';
       } 
}


function updateScroll(){
    var element = document.getElementById("umchat");
    element.scrollTop = element.scrollHeight;
}

function chatbotResponse() {
  botMessage = "Could not understand what you meant. Still the Automated chatbot is here to help you. Type -<br>1. <b>cricket</b>: to get live cricket score<br>2. <b>football</b>: to get live football score<br>3. <b>weather</b>: to get live weather condition in delhi<br>4. <b>stock</b> - to get live stock market status<br>5. <b>fuels</b> - to get fuel rates for today<br>6. <b>clear</b> - to clear the chat log"; //the default message

  if (lastUserMessage === 'hi') {
    botMessage = "Hey there! Here to help you. Type -<br>1. <b>cricket</b>: to get live cricket score<br>2. <b>football</b>: to get live football<br>3. <b>weather</b>: to get live weather condition in delhi<br>4. <b>stock</b> - to get live stock market status<br>5. <b>fuels</b> - to get fuel rates for today<br>6. <b>clear</b> - to clear the chat log";
  }
  if (lastUserMessage === 'cricket') {
    botMessage = '<b> Live cricket score :</b>';
    cricket_score();
  }

  if (lastUserMessage === 'football') {
    botMessage = '<b> Live football score :</b>';
    football_score();
  }

  if (lastUserMessage === 'weather') {
    botMessage = '<b> Current weather in Delhi :</b>';
    weather();
  }

  if (lastUserMessage === 'stock') {
    botMessage = '<b> Live stock market status :</b>';
    stock();
  }

  if (lastUserMessage === 'fuels') {
    botMessage = '<b> Fuels prices in delhi today :</b>';
    petrol();
  }

  if (lastUserMessage === 'how are you?') {
    botMessage = 'I am all awesome what about you?';
  }
  if (lastUserMessage === 'Is mugs fat?') {
    botMessage = 'Banana shake for life';
  }

  if (lastUserMessage === 'clear') {
    botMessage = 'Chat cleared.';
    clear();
  }

  if (lastUserMessage === 'Hi') {
    botMessage = "Hey there! Here to help you. Type -<br>1. <b>cricket</b>: to get live cricket score<br>2. <b>football</b>: to get live football<br>3. <b>weather</b>: to get live weather condition in delhi<br>4. <b>stock</b> - to get live stock market status<br>5. <b>fuels</b> - to get fuel rates for today<br>6. <b>clear</b> - to clear the chat log";
  }
  if (lastUserMessage === 'Cricket') {
    botMessage = '<b> Live cricket score :</b>';
    cricket_score();
  }

  if (lastUserMessage === 'Football') {
    botMessage = '<b> Live football score :</b>';
    football_score();
  }

  if (lastUserMessage === 'Weather') {
    botMessage = '<b> Current weather in Delhi :</b>';
    weather();
  }

  if (lastUserMessage === 'Stock') {
    botMessage = '<b> Live stock market status :</b>';
    stock();
  }

  if (lastUserMessage === 'Fuels') {
    botMessage = '<b> Fuels prices in delhi today :</b>';
    petrol();
  }

  if (lastUserMessage === 'How are you?') {
    botMessage = 'I am all awesome what about you?';
  }
  if (lastUserMessage === 'Is mugs fat?') {
    botMessage = 'Banana shake for life';
  }

  if (lastUserMessage === 'Clear') {
    botMessage = 'Chat cleared.';
    clear();
  }
}


function newEntry() {
  if (document.getElementById("chatbox").value != "") {
    lastUserMessage = document.getElementById("chatbox").value;
    document.getElementById("chatbox").value = "";
    messages.push("<div id='tooltip-left'><b>" + userName + ": </b>" + lastUserMessage + "</div");
    chatbotResponse();
    messages.push("<div id='tooltip-right'><b>" + botName + ": </b>" + botMessage + "</div");
    for (var i = 1; i < 120; i++) {
      if (messages[messages.length - i])
      {
        document.getElementById("chatlog" + i).innerHTML = messages[messages.length - i];
        updateScroll();
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

$( "#send" ).click(function() {
  newEntry();
});


