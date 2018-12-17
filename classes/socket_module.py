from flask import Flask, render_template, session, request, redirect,url_for
from flask_socketio import SocketIO, Namespace, emit, send, join_room, leave_room, close_room, rooms, disconnect
from flask_login import current_user
import classes.settings as config

class GameLobbyNs(Namespace):
    clients = {}
    game_rooms = {'roomId1': ["Jhon","Alex","Alice"],'roomId2': ["Bob"],'roomId3': ["Ted","Max"]}

    player_ready = {"Jhon":False,"Alex":True,"Alice":False,"Bob":True,"Ted":True,"Max":False}

    RESPONSE_EVENTS = [
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

    def make_rm_List(self):
        roomList = {}
        for key in self.game_rooms:
            roomList[key] = len(self.game_rooms[key])
        return roomList

    def filterOutUser(self, userId, room):
        for player in self.game_rooms[room]:
            if player.keys(0) == userId: yield player

    def remove_player_room(self, userId, roomId):
        if (userId) in self.game_rooms[roomId]:
            self.game_rooms[roomId].remove(current_user.username)
            emit('roomsList', {'data': 'Connected', 'roomList': self.make_rm_List()},room='/lobby')

    def remove_player(self, userId):
        for key in self.game_rooms:
            self.remove_player_room(userId, key)
        emit('roomsList', {'data': 'Connected', 'roomList': self.make_rm_List()},room='/lobby')

    def add_player(self, userId, roomId):
        self.game_rooms[roomId].append(userId)
        self.player_ready[userId]= {userId: False}
        emit('roomsList', {'data': 'Connected', 'roomList': self.make_rm_List()},room='/lobby')

    def on_connect(self):
        self.clients[current_user.username] = session['username']
        join_room('/lobby')
        print('/room joined ')#+ session['username']
        emit('roomsList', {'data': 'Connected', 'roomList': self.make_rm_List()},room='/lobby')

    def on_disconnect(self):
        self.remove_player(request.sid)
        if current_user.username in self.clients: del self.clients[current_user.username] 
        print('Client disconnected', request.sid)

    def on_my_ping(self):
        emit('my_pong')

    def on_disconnect_request(self):
        emit('my_response', {'data': 'Disconnected!'})
        disconnect()

    def on_create_room(self, data):
        print('create_room' + data['roomId'])
        roomId = data['roomId']
        self.game_rooms[roomId] = []
        self.on_join_room( data)
        emit('roomsList',{'data': 'Connected', 'roomList': self.make_rm_List()},room='/lobby')

    def on_my_event(self, message):
        emit('my_response', {'data': message['data']})

    def on_my_broadcast_event(self, message):
        emit('my_response', {'data': message['data']}, broadcast=True)

    def on_close_room(self, message):
        emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.'}, room=message['room'])
        close_room(message['room'])

    def on_my_room_event(self, message):
        print('my_room_event' + request.sid)
        emit('my_response', {'data': message['data']}, room=message['room'])

    def on_join_room(self, data):
        print(request.sid + " joining " + data['roomId'])
        emit('roomsList', {'data': 'Connected', 'roomList': self.make_rm_List()},room='/lobby')
        roomId = data['roomId']

        leave_room('/lobby')
        join_room('/'+roomId)
        if ((roomId in self.game_rooms) 
        and (len(self.game_rooms[roomId]) < config.MAX_ROOM_SIZE)  
        and (current_user.username not in self.game_rooms[roomId])):
            self.add_player(current_user.username, data['roomId'])
            emit('join_room',{'room':'/'+roomId, 'players': self.game_rooms[roomId]}, room='/'+roomId)
        elif roomId != '/lobby':
            if (current_user.username in self.game_rooms[roomId]): #need it for refrersh page load
                emit('join_room',{'room':'/'+roomId, 
                'players': self.game_rooms[roomId]}, room='/'+roomId)

    def on_ready_event(self, message):
        self.player_ready[current_user.username] = message['Toggle']
        playersReady = True
        for roomId in self.game_rooms:
            if current_user.username in self.game_rooms[roomId]:
                if len(self.game_rooms[roomId]) < config.MIN_PLAYER_START:
                    playersReady = False
                else:
                    for player in self.game_rooms[roomId]:
                        if (self.player_ready[player] == False):
                            playersReady = False
                break
        if playersReady:
            print("all ready")
            emit('start_game',{'room':'/'+roomId, 'players': self.game_rooms[roomId]}, room='/'+roomId)

    def on_leave(self, message):
        print('leaving ' + message['room'])
        leave_room(message['room'])
        join_room('/lobby')
        self.remove_player_room(current_user.username, message['room'][1:])
        emit('roomsList',{'data': 'Connected', 'roomList': self.make_rm_List()},room='/lobby')
        emit('restore_input',{'data': 'Connected', 'roomList': self.make_rm_List()},room=request.sid)
        return redirect('dashboard')

    def on_send_message(self, message, room, methods=['GET', 'POST']):
        emit('receiveMessage', message, room=room)
