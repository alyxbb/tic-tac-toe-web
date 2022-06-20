if (window.location.protocol == "https:"){
    websocket=new WebSocket("wss://"+window.location.host+"/ws/tictactoe/");
} else {
    websocket=new WebSocket("ws://"+window.location.host+"/ws/tictactoe/");

}

websocket.onclose = function(e){
    document.getElementById("errorbar").innerHTML="connection lost!";
};
document.getElementById("playersubmit").onclick = function(e){
    players=0
    if(document.getElementById("1player").checked){
        players=1
    } else if(document.getElementById("2player").checked){
        players=2
    }
    websocket.send(JSON.stringify({
        "command":"startgame",
        "players":players,
    }));
};
document.getElementById("table0").onclick = function() {sendmove(0)};
document.getElementById("table1").onclick = function() {sendmove(1)};
document.getElementById("table2").onclick = function() {sendmove(2)};
document.getElementById("table3").onclick = function() {sendmove(3)};
document.getElementById("table4").onclick = function() {sendmove(4)};
document.getElementById("table5").onclick = function() {sendmove(5)};
document.getElementById("table6").onclick = function() {sendmove(6)};
document.getElementById("table7").onclick = function() {sendmove(7)};
document.getElementById("table8").onclick = function() {sendmove(8)};


function sendmove(move){
    websocket.send(JSON.stringify({
        "command":"playermove",
        "move":move
    }));
}




websocket.onmessage = function(e){
    data=JSON.parse(e.data);
    switch(data.command){
        case "startgame":
            document.getElementById("playerselector").remove();
            document.getElementById("gamegrid").style.display="block";
            document.getElementById("goindicator").innerHTML=data.go+"'s go";
            if(data.players==1){
                document.getElementById("xwintext").innerHTML="Player wins";
                document.getElementById("owintext").innerHTML="Computer wins";

            }
            break;
        case "popup":
            alert(data.message);
            break;
        case "update":
            document.getElementById("goindicator").innerHTML=data.go+"'s go";
            table = document.getElementById("table");
            for (var i = 0, row; row = table.rows[i]; i++) {
                for (var j = 0, col; col = row.cells[j]; j++) {

                    celdata=data.table[i][j];
                    if (celdata!="~"){
                        col.innerHTML=celdata;
                    }
                }  
            };
            break;
        case "refresh":
            for (var i = 0, row; row = table.rows[i]; i++) {
                for (var j = 0, col; col = row.cells[j]; j++) {
                    col.innerHTML="";
                }  
            };
            if(data.players==2){
                document.getElementById("goindicator").innerHTML=data.go+"'s go";
            } else if(data.players==1){
                document.getElementById("goindicator").innerHTML=data.go+"'s go.";

            }
            break;
        case "scoreboard":
            oldscore=parseInt(document.getElementById(data.value).innerHTML);
            document.getElementById(data.value).innerHTML=oldscore+1;
            break;
    }
                
};


 