const socket = io.connect('http://' + document.domain + ':' + location.port+'/lobby');

info = {}

socket.on('connect', () => {    
    info.username = $("#username").html();
    info.room = "/lobby";

    $( 'form' ).on( 'submit', function( e ) {
        e.preventDefault()
        let user_name = info.username;
        let user_input = $( 'input.chat_input' ).val();
        if (user_input != '')
            socket.emit('send_message', {
            user_name : user_name,
            message : user_input,
            room: $(".tab-pane.active")[0].id == "tab1primary" || info.room == "/lobby" ? "#tab1primary": "#tab2primary",
            }, room=info.room )
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

socket.on('roomsList',(rmData)=>{
    if (info.room != "/lobby") return;
    
    $('.toggle').css('display','none');
    let roomListContainer = document.querySelector('.gamerooms');
    roomListContainer.innerHTML = '<ul class="list-group"></ul>';
    let roomListDiv = document.querySelector('.list-group');
    roomListDiv.innerHTML = "";
    Object.keys(rmData['roomList']).forEach(room => {
        roomListDiv.innerHTML += `<li class="list-group-item room" ns="${room}">${room} - Players ${rmData['roomList'][room]}/10</li>`;
    });

    Array.from(document.getElementsByClassName('room')).forEach(room=>{
        room.addEventListener('click', e =>{
            const endpoint = room.getAttribute('ns');
            joinGame(endpoint)
            setCookie("endpoint", endpoint, 1);
        })
    });
    createLobby();
})

socket.on('join_room', message_data => {
    info.room = message_data.room;
    buildRoomList(message_data);
});

socket.on('room_busy', message_data => {
    var node = document.createTextNode("Game already in progress!");
    var modal = document.getElementById("modal-body");
    modal.innerHTML="";
    modal.appendChild(node);
    document.getElementById("exampleModalLabel").innerText=message_data.room;
    $('#modalBtn').click();
});

socket.on('room_exist', message_data => {
    var node = document.createTextNode("Game room name present!");
    var modal = document.getElementById("modal-body");
    modal.innerHTML="";
    modal.appendChild(node);
    document.getElementById("exampleModalLabel").innerText=message_data.room;
    $('#modalBtn').click();
});

socket.on('restore_input',createLobby);

function createLobby(){
    $('#new-room').show();
    document.querySelector('#create_game_room').onclick = createGame;
    document.querySelector('#lbl-new-room').addEventListener("keyup", function(event) {
        event.preventDefault();
        if (event.keyCode === 13) {
            document.getElementById("create_game_room").click();
        }
    });
    if (document.querySelector('#toggle-ready').checked){
        document.querySelector('.toggle').click();
    };
}

function buildRoomList(message_data){  
    $('#new-room').hide();
    $('#event-room').show();
    $('#tab2').css('visibility', 'visible');
    //document.querySelector('.gamerooms').innerHTML=`<p>Joined Room: ${message_data['room']}</p><p>${message_data['players']}</p>`;
    document.querySelector('.gamerooms').innerHTML=`<div class="row">
    <div class="container" id="joinedDiv">
        <h2>Joined Room: ${message_data['room']}</h2>
        <h3>${message_data['players']}</h3>
    </div>
    </div>`;
    //document.querySelector('#testP').addEventListener('click', e =>{
    //    socket.emit('my_room_event',{'data':"test",'room':message_data['room']})
    //});
    document.querySelector('#btn-leave').addEventListener('click', leaveRooms);
    $('.toggle').css('display','block');
}

function leaveRooms(){
        var old = info.room
        info.room = "/lobby";
        $('#tab1').click();
        $('#tab2').css('visibility', 'hidden');
        socket.emit('leave',{'data':"test",'room':old})
        setCookie("endpoint", "/lobby", 1);
        $('#event-room').hide();
}

function createGame() {
    const endpoint = document.querySelector('#lbl-new-room').value;
    socket.emit('create_room', {STUFF: "TO-BE DEFINED", roomId: endpoint, userId: info.username});
    setCookie("endpoint", endpoint, 1);
}

function joinGame(endpoint) {
    socket.emit('join_room', {roomId: endpoint, userId: info.username});
}

socket.on('disconnect', () => {
    if (document.querySelector('#toggle-ready').checked){
        document.querySelector('.toggle').click();
    };
    setCookie("endpoint", "", 1);
});

socket.on('start_game', message_data => {
    $(location).attr('href', '/game'+message_data['room']);
});

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
        c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
        }
    }
    return "";
}

function checkCookie() {
    var endpoint = getCookie("endpoint");
    if (endpoint != "") {
        joinGame(endpoint)
    }
} 

$( document ).ready(function() {
    checkCookie();
    $('.toggle').on('change',()=>{
        socket.emit('ready_event', {'Toggle':document.querySelector('#toggle-ready').checked, 'room':info.room});
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
    $("#leave-room").on("click",  leaveRooms);

});

