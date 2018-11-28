console.log('hello');

$(() => {

    var socket = io.connect('http://' + document.domain + ':' + location.port);

    function load_game_rooms(data) {
        // to bind
        return false;
    }

    socket.on('connect', () => {
       console.log('Websocket connected!');
       //socket.emit('join', '/home?');
    });

    
    socket.on('join_room', message_data => {
      console.log(message_data);
        
    });

    function createGame() {
        console.log('Creating game...');
        socket.emit('create_room', {STUFF: "TO-BE DEFINED", roomId: 'random_string()', players: []});
    }
    function joinGame() {
        console.log('Joining game...');
        socket.emit('join_room', {roomId: 'random_string()'});
    }
    document.querySelector('#create_game_room').onclick = createGame;
    document.querySelector('#join_game_room').onclick = joinGame;
});