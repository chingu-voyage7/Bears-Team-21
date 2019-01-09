

var testData = {hand: ["path-01","path-02","path-03","path-19","path-20"], role:"path-03", 
board:{"203":"path-03","8":"path-02","208":"path-01","408":"path-01"}, 
players:["Game Opponent 1","Game Opponent 2","Game Opponent 3","Game Opponent 4"]};


var socket

window.onload = function() {
    const gameName = document.getElementById("gamename").firstChild.data;
    socket = io.connect('http://' + document.domain + ':' + location.port+'/' + gameName, { query: 'foo=bar', extra: 'extra'});
    var squarewidth = 120; 
    var squareheight= 195; 
    var divMain = document.getElementById('grid');
    var size = 19;
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
            }); 
            divMain.appendChild(sqr); 
        }
    }
    document.getElementById('grid').scrollBy({
        top: 620,
        left: 1090
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
                socket.emit('send_message', {
                user_name : user_name,
                message : user_input,
                room: "tab1primary",
                })
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
            console.log(msg.room)
            $('div #'+msg.room).append(
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
        data.forEach(function(name) {
            var cardNode = document.createElement("DIV");  
            cardNode.className= "card sprite " + name;
            cards.push(name);
            cardNode.index = cards.length
            cardNode.addEventListener("dblclick", function () {
                if ($(this).hasClass( "rotate" )){
                    $(this).removeClass('rotate');
                } else {
                    $(this).addClass('rotate');
                }
            });
            cardNode.addEventListener('click', function(){
                selected.push(cardNode.index);
                console.log('selected ',cardNode.index);
                //cardNode.className += " red-border";
            });
            document.getElementById("hand").appendChild(cardNode);
        });
    })

    $('#discard').click(function(){
        selected.forEach(function(i){
            console.log(i);
            $('#hand .card:nth-child('+i+')').addClass('red-border');
        })
        selected = []
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
