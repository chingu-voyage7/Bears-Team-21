console.log('hello');


$(() => {

    var socket = io.connect('//127.0.0.1:5000/');

    function load_game_rooms(data) {
        // to bind
        return false;
    }

    function create_game_room(data) {
        socket.emit('create_room', '/clicked to do');
        return false;
    }

    function join_game_room() {
        socket.emit('join', '/clicked to do');
        return true;

    }

    socket.on('connect', () => {
       socket.emit('join', '/home?');

       document.querySelector('#join_game_room').onclick = join_game_room;

    });

    
    socket.on('ecc ecc', message_data => {
      
        
    });


});