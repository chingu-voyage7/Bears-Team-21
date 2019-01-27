const lobbySocket = io.connect('http://' + document.domain + ':' + location.port+'/lobby');
var sx = 0, sy = 0, stop = 0, sleft = 0;
var testData = {hand: ["path-01","path-02","path-03","path-19","path-20"], role:"path-03", 
board:{"203":"path-03","8":"path-02","208":"path-01","408":"path-01"}, 
players:["Game Opponent 1","Game Opponent 2","Game Opponent 3","Game Opponent 4"]};
const CELL_ZOOM = 0.75;
const WIDTH = 19;

var socket;
var cards = [];
var selected = [];
var available = [];
var active_player = false;

window.onload = function() {
    $('footer').css('position', 'relative');
    const gameName = document.getElementById("gamename").firstChild.data;
    socket = io.connect('http://' + document.domain + ':' + location.port+'/' + gameName, { query: 'foo=bar', extra: 'extra'});
    var squarewidth = 120; 
    var squareheight= 195; 
    var divMain = document.getElementById('grid');
    var size = WIDTH;
    var count = 0;
    for (var j = 0; j < size; j++) {
        for (var i = 0; i < size; i++) {
            var sqr = document.createElement('div'), 
            coord = [i,j]
            sqr.className = 'square'; 
            count++;
            sqr.id ="square-"+count;
            sqr.style.width = squarewidth + 'px'; 
            sqr.style.height = squareheight + 'px'; 
            sqr.style.left = (coord[0] * Math.floor(squarewidth * CELL_ZOOM)) + 'px'; 
            sqr.style.top = (coord[1] * Math.floor(squareheight * CELL_ZOOM)) + 'px';
            sqr.setAttribute("x", coord[0]);
            sqr.setAttribute("y", coord[1]);
            sqr.style.transform = `scale(${CELL_ZOOM})`;
            sqr.addEventListener('click', function(evt) { 
                if (active_player == false) {
                    return;
                }
                cell = this.id.split('-')[1];
                if (selected.length == 1){
                    coord = [parseInt(this.getAttribute("x")),parseInt(this.getAttribute("y"))]
                    switch(selected[0].type){
                        case 'path':
                            //path card, check if i can place it
                            //get data from backend for available spots
                            flag = false;
                            for (i = 0; i < available.length; i++){ 
                                coords = available[i];
                                if (coord[1] == coords[0] && coord[0] == coords[1]){
                                    if (canBePlaced(coord, selected[0].required)){
                                        placeCard(coord, selected[0].index-1);                                    
                                    }
                                    break;
                                }
                            }
                            break;
                        case 'remove':
                            if((this.classList.length > 1) && !(this.classList.contains("path-00") || this.classList.contains("goal-back"))){
                                removeCard(coord, selected[0].index-1);
                            }
                            break;
                        case 'reveal':
                            if (this.classList.contains("goal-back")){
                                revealCard(coord, selected[0].index-1);
                            }
                            break;
                    }                 
                }
            }); 
            divMain.appendChild(sqr); 
        }
        //dragElement(document.getElementById("chat"));//chat-body
        document.getElementById('handle').addEventListener('mousedown', initialiseResize, false);
    }

    function modifyPlayer(player, card){
        socket.emit('play_action',{'card': card, 'target': player});
        active_player = false;
    }

    function placeCard(coords, card){
        //emit handle move for path card
        socket.emit("place_card",{"cards": card,"x":coords[1],"y":coords[0]});
        active_player = false;
    }
    function removeCard(coords, card){
        //emit handle move for path card
        socket.emit("remove_card",{"card": card,"x":coords[1],"y":coords[0]});
        active_player = false;
    }
    function inspectPlayer(player, card){
        //emit handle move for path card
        socket.emit("inspect_player",{"card": card,"player":player});
        active_player = false;
    }
    function canBePlaced(coords, card){
        return true;
    }
    function revealCard(coords, card){
        socket.emit("show_goal",{"cards": card,"x":coords[1],"y":coords[0]});
        active_player = false;
    }

    document.getElementById('grid').scrollBy({
        top: 400,
        left: 420
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
        $( '#btn-chat' ).on( 'click', function( e ) {
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
            $('div '+msg.room).append(
                (msg.user_name == $("#username").html() ? base_sent : base_receive)
            );
            $('div.msg_container_base').scrollTop($('div.msg_container_base')[0].scrollHeight);
        }
    }) 
    lobbySocket.on('receiveMessage', function(msg) {
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
            $('div '+msg.room).append(
                (msg.user_name == $("#username").html() ? base_sent : base_receive)
            );
            $('div.msg_container_base').scrollTop($('div.msg_container_base')[0].scrollHeight);
        }
    }) 
    socket.on("update_players", data => {
        document.getElementById("opponents").innerHTML = ""
        var players = Object.keys(data);
        players.forEach(function(name,i) {
            var opponentNode = `<div class="col-sm-12">
            <div class="game-opponent well well-sm" style="min-height: 100px;" id="player-${i}" name="${name}">
                <div class="row text-center">
                    <label>${name}</label>
                </div>
                <div class="row"><div class="col-sm-1"></div>`;
                    //<div class="col-sm-1"></div>`;
            var count = 0;
            data[name].forEach(function(icon) {
                count += 1;
                if (!icon.startsWith("Gold") && !icon.startsWith("Cards")){
                    opponentNode += `<div class="col-sm-2 tools ${icon}"></div>`
                }
                //if (count%3 == 0){
                //    opponentNode +='<div class="col-sm-2"></div></div><div class="row"><div class="col-sm-1"></div>';
                //}
            });        
            //opponentNode += `<div class="col-sm-1"></div>
            opponentNode += `</div><div class="row-fluid">
                    <span>
                        <div style="float: left;"><span class="gold"></span></div>
                        <small>${data[name][data[name].length-2]}</small>
                    </span>
                </div>
                <div class="row-fluid">
                    <span>
                        <div style="float: left;"><span class="back-small"></span></div>
                        <small>${data[name][data[name].length-1]}</small>
                    </span>
                </div>
                </div></div>`;
            document.getElementById("opponents").innerHTML += (opponentNode);
            $('.game-opponent').each(function (i,div) {
                div.addEventListener('click', function(evt) { 
                    if (active_player == false) {
                        return;
                    }
                    player = parseInt(i);
                    if (selected.length == 1){
                        switch(selected[0].type){
                            case 'handsoff':
                            case 'swaphats':
                            case 'trapped':                                
                            case 'theft':
                            case 'damage':
                            case 'repair':                            
                            case 'free':
                            case 'swaphand':
                                modifyPlayer(player, selected[0].index-1);
                                break;
                            case 'inspection':
                                inspectPlayer(player, selected[0].index-1);
                                break;
                    }                 
                }
                });
            });
        });
    })

    socket.on("update_hand", (data)=>{
        document.getElementById("hand").innerHTML = "";
        cards = [];
        selected = [];
        data.forEach(function(card) {
            var cardNode = document.createElement("DIV");  
            cardNode.style.width = squarewidth + 'px'; 
            cardNode.style.height = squareheight + 'px'; 
            cardNode.className= "card sprite " + card.name + (card.rotated ? " rotate" : "");
            cardNode.type = ("edges" in card ? 'path' : card.type);
            cardNode.setAttribute("data-toggle", "tooltip");
            cardNode.setAttribute("title", card.tooltip);
            cardNode.tooltiptext = card.tooltip
            if (cardNode.type == "path"){
                cardNode.required = card.required;
            }
            cards.push(card);
            cardNode.index = cards.length;
            cardNode.addEventListener("dblclick", function () {
                if (cards[$(this).index()].name.startsWith('path')){
                    socket.emit("rotate_card",{"card": $(this).index()});
                    if ($(this).hasClass( "rotate" )){
                        $(this).removeClass('rotate');
                    } else {
                        $(this).addClass('rotate');
                    }
                }
            });
            cardNode.addEventListener('click', function(e){
                e.preventDefault();
                if (selected.length <= 3) {
                    if ($(this).hasClass( "red-border" )){
                        $(this).removeClass('red-border');
                        selected = selected.filter(card => card.index !== cardNode.index);
                    } else if (selected.length != 3){
                        selected.push(cardNode);
                        $(this).addClass('red-border');                    
                    }
                }            
            });
            document.getElementById("hand").appendChild(cardNode);
            $('[data-toggle="tooltip"]').tooltip(); 
        });
    })

    $('#discard').click(function(){
        if (active_player == false) {
            return;
        }
        selected.forEach(function(card){
            i = card.index;
            if ($('#hand .card:nth-child('+i+')').hasClass( "red-border" )){
                $('#hand .card:nth-child('+i+')').removeClass('red-border');
            }
        });
        socket.emit('card_discarded', {'cards':selected.map(function(x) {
            return x.index - 1;})});
        active_player = false;
        selected = [];
    });

    socket.on("update_role", (data)=> {
        var roleNode = document.createElement("DIV"); 
        roleNode.className= "card sprite " + data["role"];
        var roleContainer = document.getElementById("player-role");
        while (roleContainer.firstChild) {
            roleContainer.removeChild(roleContainer.firstChild);
        }
        roleNode.setAttribute("data-toggle", "tooltip");
        switch(data["role"]) {
            case "bluedigger":
                roleNode.setAttribute("title", "Blue Team Digger, build a path from the Start card to the treasure card, among the three End cards.");
            break;
            case "greendigger":
                roleNode.setAttribute("title", "Green Team Digger, build a path from the Start card to the treasure card, among the three End cards.");
            break;
            case "profiteer":
                roleNode.setAttribute("title", "The Profiteer, you win when the gold-diggers or The Saboteurs win. However, two Gold Pieces less.");
            break;
            case "geologist":
                roleNode.setAttribute("title", "The Geologist, has no interest for gold, for each visible crystal, you receive 1 Gold Piece.");
            break;
            case "theboss":
                roleNode.setAttribute("title", "The Boss, you win whenever the Green or the Blue Team wins, but always gets one Gold Piece less than them.");
            break;
            case "saboteurs":
                roleNode.setAttribute("title", "The Saboteur, in association with other saboteurs, prevent the gold diggers from getting to the treasure.");
            break;
        }
        roleContainer.appendChild(roleNode);
        $('[data-toggle="tooltip"]').tooltip(); 
    })
    
    socket.on("wait_for_player", (data)=> {
        active_player = data["active"];
        $("#player-active").text("Round: " + data["round"] + " - " + (data["active"] == 1 ? "It's your turn!" : "Waiting for "+ data["player"]));
        $("#deck-cards").text(data["deck"]);
    })

    socket.on("wait_for_timer", (data)=> {
        console.log("wait");
        socket.emit('received_timer', data);
    })

    socket.on("update_board", (data)=> {
        jQuery('.square').each(function(i, cell) {
            cell.className = "square";
        });
        Object.keys(data).forEach(function(key) {
            var card_square = document.getElementById("square-"+key);
            card_square.className="square sprite "+data[key].split('.').join(' ');
            //card_square.style.transform = (card_square.className.includes("rotate")? `rotate(180) ` : "") + `scale(${CELL_ZOOM})`;
        });
    })
    
    socket.on("available_cells", (data)=> {
        available = data; //(y,x)
        available.forEach(function(coords) {
            $("#square-"+(coordsToPos(coords[0],coords[1])+1)).addClass("available");
        });
    })

    socket.on("reveal_goal", (data)=> {
        var goalNode = document.createElement("DIV"); 
        if (data["show"] == "gold") {
            goalNode.className= "card sprite goal-00";
        } else {
            goalNode.className= "card sprite goal-01";
        }
        var modal = document.getElementById("modal-body");
        modal.innerHTML="";
        modal.appendChild(goalNode);
        document.getElementById("exampleModalLabel").innerText="Destination Revealed";
        $('#modalBtn').click();
    })

    socket.on("reveal_role", (data)=> {
        var playerNode = document.createElement("DIV"); 
        playerNode.className= "card sprite "+ data["role"];
        var modal = document.getElementById("modal-body");
        modal.innerHTML="";
        modal.appendChild(playerNode);
        document.getElementById("exampleModalLabel").innerText= "Player: " + $("#player-"+data["player"]).attr("name");
        $('#modalBtn').click();
    })

    socket.on("round_over", (data)=> { 
        var modal = document.getElementById("modal-body");
        var htmlScores = `<div class="leaderboard"><ol>`;
        Object.keys(data).forEach(function(current,idx) {
            htmlScores += `<li>
                    <mark>${data[current][0]}</mark>
                    <small>${data[current][1]}</small>
                    </li>`;
        });
        htmlScores += "</ol></div>"
        modal.innerHTML=htmlScores;
        document.getElementById("exampleModalLabel").innerText="Round Scores";
        $('#modalBtn').click();
    })
    socket.on("game_over", (data)=> {
        $("#player-active").text("Game Over! Winners: " + data.join(" "));
    })

    let el = document.querySelector(".game-board");
    let draggingFunction = (e) => {
        el.scrollLeft = sleft - e.pageX + sx;
        el.scrollTop = stop - e.pageY + sy;
    };
    el.addEventListener('mousedown', (e) => {
        e.preventDefault();
        sy = e.pageY;
        sx = e.pageX;
        stop = el.scrollTop;
        sleft = el.scrollLeft;
        document.addEventListener('mousemove', draggingFunction);
    });
    document.addEventListener('mouseup', () => {
        document.removeEventListener("mousemove", draggingFunction);
    });
    socket.on('game_message', function(msg) {
            var base_receive = `<div class="row msg_container base_receive">
                    <div class="col-md-12 col-xs-12">
                        <div class="messages msg_receive">
                            <b style="color: #000">Game Log</b> <p>${msg.message}</p>
                        </div>
                    </div>
                </div>`;
            $('div #tab2primary').append(base_receive);
            $('div.msg_container_base').scrollTop($('div.msg_container_base')[0].scrollHeight);
    }) 
    socket.on('time_out', function(data) {
       console.log("time out");
       if (active_player == false) {
        return;
        }
        selected.forEach(function(card){
            i = card.index;
            if ($('#hand .card:nth-child('+i+')').hasClass( "red-border" )){
                $('#hand .card:nth-child('+i+')').removeClass('red-border');
            }
        });
        socket.emit('card_discarded', {'cards':[0]});
        active_player = false;
        selected = [];
    }) 
    socket.on('seconds_left', function(data) {
        $("#seconds").text(padding_left(data['number'].toString()) + " seconds");
     }) 
};

info = {}

function posToCoords(cell){
    let x = cell % WIDTH;
    let y = Math.floor(cell / WIDTH);
    return [x , y]
}
function coordsToPos(x, y){
    n = y + WIDTH * x 
    return n
}

function padding_left(s) {
    if (s.length >= 2) {
      return s;
    }
    return "0" + s;
  }

