<<<<<<< HEAD
=======
const lobbySocket = io.connect('http://' + document.domain + ':' + location.port+'/lobby');

>>>>>>> aadcaeb4143c70f79bddb9cfe865c569409660a5
var testData = {hand: ["path-01","path-02","path-03","path-19","path-20"], role:"path-03", 
board:{"203":"path-03","8":"path-02","208":"path-01","408":"path-01"}, 
players:["Game Opponent 1","Game Opponent 2","Game Opponent 3","Game Opponent 4"]};

const WIDTH = 19

var socket

window.onload = function() {
    const gameName = document.getElementById("gamename").firstChild.data;
    socket = io.connect('http://' + document.domain + ':' + location.port+'/' + gameName, { query: 'foo=bar', extra: 'extra'});
    var squarewidth = 120; 
    var squareheight= 195; 
    var divMain = document.getElementById('grid');
    var size = WIDTH;
    var count = 0;
    var cards = []
    var selected = []
    for (var j = 0; j < size; j++) {
        for (var i = 0; i < size; i++) {
            var sqr = document.createElement('div'), 
            coord = {"x":i,"y":j} 
            sqr.className = 'square'; 
            count++;
            sqr.id ="square-"+count;
            sqr.style.width = squarewidth + 'px'; 
            sqr.style.height = squareheight + 'px'; 
            sqr.style.left = (coord.x * squarewidth) + 'px'; 
            sqr.style.top = (coord.y * squareheight) + 'px';
            sqr.addEventListener('click', function(evt) { 
                console.log(this); 
                cell = this.id.split('-')[1];
                if (selected.length == 1){
                    
                }
            }); 
            divMain.appendChild(sqr); 
        }
    }
    document.getElementById('grid').scrollBy({
        top: 620,
        left: 1090
    });
    $('#tab2').css('visibility', 'visible');
    $("a.nourl").click(function(e){
        e.preventDefault();
        
     });
    $(".nav li").on("click", function(e) {
        $(".nav li").removeClass("active");
        $(".tab-pane").removeClass("in active");
        $(this).addClass("active");
        $(e.target.hash).addClass("in active");
        $('div.msg_container_base').scrollTop($('div.msg_container_base')[0].scrollHeight);
    });

    $(".toggle-chat").click(function () {
        $header = $(this);
        $content = $(".msg_container_base");
        $content.slideToggle(500, function () {
            $header.text(function () {
                return $content.is(":visible") ? "Collapse" : "Expand";
            });
        });
    });

    socket.on('connect', () => {    
        info.username = $("#username").html();
        info.room =  $("#gamename").html();
        console.log(`Websocket ${info.username} connected!`);
        $( '#btn-chat' ).on( 'click', function( e ) {
            console.log("info",info);
            e.preventDefault()
            let user_name = info.username;
            let user_input = $( 'input.chat_input' ).val();
            if (user_input != '')
                if ($(".tab-pane.active")[0].id == "tab2primary") {
                    socket.emit('send_message', {
                        user_name : user_name,
                        message : user_input,
                        room: "#tab2primary",
                        })
                } else {
                    lobbySocket.emit('send_message', {
                        user_name : user_name,
                        message : user_input,
                        room: "#tab1primary",
                    }, room="/lobby")
                }
            $('input.chat_input').val('').focus()
          } )
    });

    socket.on('receiveMessage', function(msg) {
        console.log( msg )
        if(typeof msg.user_name !== 'undefined') {
            var base_receive = `<div class="row msg_container base_receive">
                    <div class="col-md-2 col-xs-2 avatar">
                        <img src="http://www.tectotum.com.br/perfilx/assets_pizza/img/search/avatar7_big.png" class=" img-responsive ">
                    </div>
                    <div class="col-md-10 col-xs-10">
                        <div class="messages msg_receive">
                            <b style="color: #000">${msg.user_name}</b> <p>${msg.message}</p>
                        </div>
                    </div>
                </div>`;
            var base_sent=`<div class="row msg_container base_sent">
                    <div class="col-md-10 col-xs-10">
                        <div class="messages msg_sent">
                            <b style="color: #000">${msg.user_name}</b> <p>${msg.message}</p>
                        </div>
                    </div>
                    <div class="col-md-2 col-xs-2 avatar">
                        <img src="http://www.tectotum.com.br/perfilx/assets_pizza/img/search/avatar7_big.png" class=" img-responsive ">
                    </div>
                </div>`;
            //var chatTab = msg.room == "/lobby"? "#tab1primary" : "#tab2primary"
            console.log("room msg:"+msg.room)
            $('div '+msg.room).append(
                (msg.user_name == $("#username").html() ? base_sent : base_receive)
            );
            $('div.msg_container_base').scrollTop($('div.msg_container_base')[0].scrollHeight);
        }
    }) 
    lobbySocket.on('receiveMessage', function(msg) {
        console.log("lobby msg:"+ msg )
        if(typeof msg.user_name !== 'undefined') {
            var base_receive = `<div class="row msg_container base_receive">
                    <div class="col-md-2 col-xs-2 avatar">
                        <img src="http://www.tectotum.com.br/perfilx/assets_pizza/img/search/avatar7_big.png" class=" img-responsive ">
                    </div>
                    <div class="col-md-10 col-xs-10">
                        <div class="messages msg_receive">
                            <b style="color: #000">${msg.user_name}</b> <p>${msg.message}</p>
                        </div>
                    </div>
                </div>`;
            var base_sent=`<div class="row msg_container base_sent">
                    <div class="col-md-10 col-xs-10">
                        <div class="messages msg_sent">
                            <b style="color: #000">${msg.user_name}</b> <p>${msg.message}</p>
                        </div>
                    </div>
                    <div class="col-md-2 col-xs-2 avatar">
                        <img src="http://www.tectotum.com.br/perfilx/assets_pizza/img/search/avatar7_big.png" class=" img-responsive ">
                    </div>
                </div>`;
            //var chatTab = msg.room == "/lobby"? "#tab1primary" : "#tab2primary"
            console.log(msg.room)
            $('div '+msg.room).append(
                (msg.user_name == $("#username").html() ? base_sent : base_receive)
            );
            $('div.msg_container_base').scrollTop($('div.msg_container_base')[0].scrollHeight);
        }
    }) 
    socket.on("update_players", players => {
        console.log(players);
        document.getElementById("opponents").innerHTML = ""
        players.forEach(function(name) {
            var opponentNode = `<div class="col-sm-3">
            <div class="game-opponent well well-sm" style="min-height: 100px;">
                <div class="icon">
                     <i class="glyphicon glyphicon-user"></i>
                </div>
                <div class="text">
                    <label class="text-muted">${name}</label>
                </div>
            </div>
            </div>`;
            document.getElementById("opponents").innerHTML += (opponentNode);
        });
    })

    socket.on("update_hand", (data)=>{
        document.getElementById("hand").innerHTML = ""
        cards = []
        selected = [];
        data.forEach(function(card) {
            var cardNode = document.createElement("DIV");  
            console.log(card);
            cardNode.className= "card sprite " + card.name;
            cards.push(card.name);
            cardNode.index = cards.length
            cardNode.addEventListener("dblclick", function () {
                if ($(this).hasClass( "rotate" )){
                    $(this).removeClass('rotate');
                } else {
                    $(this).addClass('rotate');
                }
            });
            cardNode.addEventListener('click', function(){
                //selected.push(cardNode.index);
                console.log('selected ',cardNode.index);
                //cardNode.className += " red-border";
                if (selected.length < 3) {
                    if ($(this).hasClass( "red-border" )){
                        $(this).removeClass('red-border');
                        selected = selected.filter(index => index !== cardNode.index)
                    } else {
                        selected.push(cardNode.index);
                        $(this).addClass('red-border');                    
                    }
                }            
            });
            document.getElementById("hand").appendChild(cardNode);
        });
    })

    $('#discard').click(function(){
        selected.forEach(function(i){
            console.log(i);
            if ($('#hand .card:nth-child('+i+')').hasClass( "red-border" )){
                $('#hand .card:nth-child('+i+')').removeClass('red-border');
            }
        });
        socket.emit('card_discarded', {'cards':selected.map(function(x) {
            return x - 1;})});
        selected = [];
    });

    socket.on("update_role", (data)=> {
        var roleNode = document.createElement("DIV"); 
        roleNode.className= "card sprite " + data["role"];
        document.getElementById("player-role").appendChild(roleNode);
    })

    socket.on("update_board", (data)=> {
        Object.keys(data).forEach(function(key) {
            console.log(key, data[key]);
            document.getElementById("square-"+key).className+=" sprite "+data[key];
        });
    })
};

const RESPONSE_EVENTS = [
    'round_result',
    'new_round',
    'score_gold',
    'show_end_card',
    'update_counters',
    'gold_earned',
    'gold_stolen',
    'gold_card_earned',
    'path_card_destroyed',
    'show_goal_card',
    'path_card_played',
    'tool_status_changed',
    'draw_new_cards',
    'draw_new_role',
    'give_cards',
    'cards_discarded'
]

info = {}

function posToCoords(cell){
    let x = cell % WIDTH;
    let y = Math.floor(cell / WIDTH);
    return [x , y]
}

function testReveal(cell, index){
    console.log("75: " + posToCoords(75))
    console.log("113: " + posToCoords(113))
    console.log("151: " + posToCoords(151))
    let coords = posToCoords(cell) // To-Do saved switching coords and x -1? need to check
    socket.emit("show_goal",{"cards": index,"x":coords[1],"y":(coords[0]-1)})
}
