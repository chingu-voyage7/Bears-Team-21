from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, Namespace, emit, send, join_room, leave_room, close_room, rooms, disconnect
import classes.settings as config

class GameLobbyNs(Namespace):

    game_rooms = {'roomId1': ["Jhon","Alex","Alice"],'roomId2': ["Bob"],'roomId3': ["Ted","Max"]}

    def make_rm_List(self):
        roomList = {}
        for key in self.game_rooms:
            roomList[key] = len(self.game_rooms[key])
        return roomList

    def on_connect(self):
        join_room('/lobby')
        print('/room joined')
        emit('roomsList', {'data': 'Connected', 'count': 0, 'roomList': self.make_rm_List()},room='/lobby')

    def on_disconnect(self):
        print('Client disconnected', request.sid)

    def on_my_ping(self):
        emit('my_pong')

    def on_disconnect_request(self):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response', {'data': 'Disconnected!', 'count': session['receive_count']})
        disconnect()

    def on_create_room(self, data):
        print('create_room'+data)
        roomId = data['roomId']
        self.game_rooms[roomId] = [data["userId"]]
        join_room(roomId)
        emit('join_room', {'game_roomId': roomId})
        emit('roomsList',self.make_rm_List(), broadcast=True)

    def on_my_event(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response', {'data': message['data'], 'count': session['receive_count']})

    def on_my_broadcast_event(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response', {'data': message['data'], 'count': session['receive_count']}, broadcast=True)

    def on_close_room(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.', 'count': session['receive_count']}, room=message['room'])
        close_room(message['room'])

    def on_my_room_event(self, message):
        print('my_room_event' + request.sid)
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response', {'data': message['data'], 'count': session['receive_count']}, room=message['room'])

    def on_join_room(self, data):
        print(request.sid + " joining " + data['roomId'])
        roomId = data['roomId']
        if (roomId in self.game_rooms) and (len(self.game_rooms[roomId]) < config.MAX_ROOM_SIZE)  and (data['userId'] not in self.game_rooms[roomId]):
            self.game_rooms[roomId].append(data['userId'])
            leave_room('/lobby')
            join_room(roomId)
            send(self.game_rooms[roomId], roomId=roomId)
            emit('roomsList',self.make_rm_List(), room='/lobby')
        else:
            emit('error', {'error': 'Unable to join room.'})

    def on_join(self, message):
        join_room(message['room'])
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response', {'data': 'In rooms: ' + ', '.join(rooms()), 'count': session['receive_count']})

    def on_leave(self, message):
        leave_room(message['room'])
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response', {'data': 'In rooms: ' + ', '.join(rooms()), 'count': session['receive_count']})



