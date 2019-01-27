from flask import Flask, render_template, session, request, redirect,url_for, make_response
from flask_socketio import SocketIO, Namespace, emit, send, join_room, leave_room, close_room, rooms, disconnect
from flask_login import current_user
from .settings import *
from .game_manager import GameManager
from .timer_thread import TimerThread
from .utility import alphanum
startedGame = {}

class GameLobbyNs(Namespace):
    clients = {}
    game_rooms = {'roomId1': ["Jhon","Alex","Alice"],'roomId2': ["Bob"],'roomId3': ["Ted","Max"]}
    player_ready = {"Jhon":False,"Alex":True,"Alice":False,"Bob":True,"Ted":True,"Max":False}

    def __init__(self, namespace=None, appCtx=None, sio=None):
        super(GameLobbyNs, self).__init__(namespace)
        self.appCtx = appCtx
        self.sio = sio

    def make_rm_List(self):
        roomList = {}
        keyToRemove = []
        for key in self.game_rooms.keys():
            roomList[key] = len(self.game_rooms[key])
            if roomList[key] == 0:
                try:
                    del roomList[key]
                    keyToRemove.append(key)
                except KeyError:
                    pass
            if ( ("/"+ key) in startedGame.keys() and  startedGame["/"+key].all_disconnected()):
                try:
                    del roomList[key]
                    keyToRemove.append(key)
                except KeyError:
                    pass
        for key in keyToRemove:
            try:
                print("£",key)
                del self.game_rooms[key]
            except KeyError:
                pass
        keyToRemove = []
        for key in startedGame.keys():
            if (startedGame[key].all_disconnected()):
                keyToRemove.append(key)
            else:
                roomList[key[1:]] = len(startedGame[key].players)
        for key in keyToRemove:
            try:
                del startedGame[key]
            except KeyError:
                pass
        print (roomList)
        return roomList

    def filterOutUser(self, userId, room):
        for player in self.game_rooms[room]:
            if player.keys(0) == userId: yield player

    def remove_player_room(self, userId, roomId):
        if userId in self.game_rooms[roomId]:
            print("remove from", userId)
            self.game_rooms[roomId].remove(userId)
            emit('roomsList', {'data': 'Connected',
            'roomList': self.make_rm_List(), 'started':list(startedGame.keys())},room='/lobby')

    def remove_player(self, userId):
        for key in self.game_rooms.keys():
            self.remove_player_room(userId, key)
        emit('roomsList', {'data': 'Connected', 
        'roomList': self.make_rm_List(), 'started':list(startedGame.keys())},room='/lobby')

    def add_player(self, userId, roomId):
        self.game_rooms[roomId].append(userId)
        self.player_ready[userId]= False
        emit('roomsList', {'data': 'Connected', 
        'roomList': self.make_rm_List(), 'started':list(startedGame.keys())},room='/lobby')

    def on_connect(self):
        self.clients[current_user.username] = session['username']
        self.remove_player(current_user.username)
        join_room('/lobby')
        print('/room joined ')#+ session['username']
        emit('roomsList', {'data': 'Connected', 
        'roomList': self.make_rm_List(), 'started':list(startedGame.keys())},room='/lobby')

    def on_disconnect(self):
        self.remove_player(current_user.username)
        if current_user.username in self.clients: 
            del self.clients[current_user.username] 
        print('Client disconnected', request.sid)

    def on_my_ping(self):
        emit('my_pong')

    def on_disconnect_request(self):
        emit('my_response', {'data': 'Disconnected!'})
        disconnect()

    def on_create_room(self, data):
        print('create_room' + data['roomId'])
        print(self.game_rooms.keys())
        if ((data['roomId']) in self.game_rooms.keys()):
            emit("room_exist", {"room": data['roomId']}, room=request.sid)
            return
        if (not alphanum(data['roomId'])):
            emit("alpha_num", {"room": data['roomId']}, room=request.sid)
            return 
        roomId = data['roomId']
        self.game_rooms[roomId] = []
        self.on_join_room( data)
        #emit('roomsList',{'data': 'Connected', 
        #'roomList': self.make_rm_List(), 'started':list(startedGame.keys())},room='/lobby')

    def on_my_event(self, message):
        emit('my_response', {'data': message['data']})

    def on_my_broadcast_event(self, message):
        emit('my_response', {'data': message['data']}, broadcast=True)

    def on_close_room(self, message):
        emit('my_response', {'data': 'Room ' + message['room'] 
        + ' is closing.'}, room=message['room'])
        close_room(message['room'])

    def on_my_room_event(self, message):
        print('my_room_event' + request.sid)
        emit('my_response', {'data': message['data']}, room=message['room'])

    def on_join_room(self, data):
        print(request.sid + " joining " + data['roomId'])
        if ("/"+data['roomId'] in startedGame.keys()):
            if ((current_user.username in startedGame["/"+data['roomId']].players_list().keys()) and data['auto'] != "auto"):
                emit("room_rejoin", {"room": "/"+data['roomId']}, room=request.sid)
                return 
            else:    
                emit("room_busy", {"room": data['roomId']}, room=request.sid)
            return
        #emit('roomsList', {'data': 'Connected', 
        #'roomList': self.make_rm_List(), 'started':list(startedGame.keys())},room='/lobby')
        roomId = data['roomId']
        #leave_room('/lobby')
        join_room('/'+roomId)
        if ((roomId in self.game_rooms) 
        and (len(self.game_rooms[roomId]) < MAX_ROOM_SIZE)  
        and (current_user.username not in self.game_rooms[roomId])):
            self.add_player(current_user.username, data['roomId'])
            emit('join_room',{'room':'/'+roomId, 
            'players': self.game_rooms[roomId]}, room='/'+roomId)
        elif roomId != '/lobby':
            if  ((roomId in self.game_rooms) and (current_user.username in self.game_rooms[roomId])): #need it for refrersh page load
                emit('join_room',{'room':'/'+roomId, 
                'players': self.game_rooms[roomId]}, room='/'+roomId)

    def on_ready_event(self, message):
        print("on_ready_event")
        self.player_ready[current_user.username] = message['Toggle']
        playersReady = True
        roomId = message['room'][1:]
        for player in self.game_rooms[roomId]:
            if (self.player_ready[player] == False):
                playersReady = False
        if playersReady:
            startedGame['/'+roomId] = GameManager('/'+roomId,self.game_rooms[roomId])
            print("all ready")
            emit('start_game',{'room':'/'+roomId, 'players': self.game_rooms[roomId]}, room='/'+roomId)
            #for player in self.game_rooms[roomId]:
                #leave_room('/'+roomId)
                #self.remove_player_room(player, roomId)

    def on_leave(self, message):
        print('leaving ' + message['room'])
        leave_room(message['room'])
        join_room('/lobby')
        if message['room'] != '/lobby':
            self.remove_player_room(current_user.username, message['room'][1:])
        emit('roomsList',{'data': 'Connected', 
        'roomList': self.make_rm_List(), 'started':list(startedGame.keys())},room='/lobby')
        emit('restore_input',{'data': 'Connected'},room=request.sid)
        return redirect('dashboard')

    def on_send_message(self, message, room, methods=['GET', 'POST']):
        print('got message ns')
        emit('receiveMessage', message, room=room)



class GameRoomNs(Namespace):

    TEST_DATA = {
        "test_players":["User Player","Opponent 1","Opponent 2"],
        "test_hand":["path-01","path-02","path-03","path-19","path-20"],
        "test_role":{"role":"path-02"},
        "test_board":{"203":"path-03","8":"path-02","208":"path-01","408":"path-01"}
    }
    last_log = ""

    def __init__(self, namespace=None, appCtx=None, sio=None):
        super(GameRoomNs, self).__init__(namespace)
        self.appCtx = appCtx
        self.sio = sio

    def on_connect(self):
        print("got connection", request.namespace)
        if (request.namespace == '/') or (request.namespace not in startedGame.keys()):
            disconnect()
        emit("update_players", startedGame[request.namespace].players_list(), room=request.sid)
        emit("update_hand", startedGame[request.namespace].player_hand_list(current_user.username), room=request.sid)
        emit("update_role", {"role":startedGame[request.namespace].get_player_role(current_user.username)}, room=request.sid)
        emit("update_board", startedGame[request.namespace].board.getBoardData(), broadcast= True)
        emit("available_cells", startedGame[request.namespace].board.available, broadcast= True)
        startedGame[request.namespace].set_player_sid(current_user.username, request.sid)
        self.active_player(request.sid, request.namespace)
        if startedGame[request.namespace].timerThread is None:
            print("Starting Timer Thread") 
            startedGame[request.namespace].timerThread = TimerThread(request.namespace, self.appCtx, self.sio, startedGame[request.namespace])
            startedGame[request.namespace].timerThread.start()

    def on_disconnect(self):
        print("got disconnection")

    def on_my_event(self, data):
        print("got event")
        emit('my_response', data)

    def on_send_message(self, message, methods=['GET', 'POST']):
        print('got message')
        emit('receiveMessage', message, broadcast=True)

    def on_card_discarded(self, message):
        print('got discarded', message["cards"])
        startedGame[request.namespace].handle_move(card=message["cards"])
        self.all_update_hand(request.namespace)
        self.active_player(request.sid, request.namespace)

    def on_show_goal(self, message):
        show = startedGame[request.namespace].handle_move(message["cards"],target=[message["x"], message["y"]])
        print ("reveal:", show)
        emit("reveal_goal", {"show": show,"x":message["x"], "y" : message["y"]}, room=request.sid)
        self.all_update_hand(request.namespace)
        self.active_player(request.sid, request.namespace)

    def on_place_card(self, message):
        print ("place_card: ",message["cards"], message["x"], message["y"])
        startedGame[request.namespace].handle_move(message["cards"], message["x"],message["y"])
        emit("update_board", startedGame[request.namespace].board.getBoardData(),broadcast= True)
        emit("available_cells", startedGame[request.namespace].board.available, broadcast= True)
        self.all_update_hand(request.namespace)
        self.active_player(request.sid, request.namespace)

    def on_rotate_card(self, message):
        print ("rotate_card: ",message["card"])
        startedGame[request.namespace].player_rotate_card(current_user.username, message["card"])
    
    def on_remove_card(self, message):
        print ("remove_card: ",message["card"])
        startedGame[request.namespace].handle_move(message["card"],target=[message["x"], message["y"]])
        emit("update_board", startedGame[request.namespace].board.getBoardData(), broadcast= True)
        emit("available_cells", startedGame[request.namespace].board.available, broadcast= True)
        self.all_update_hand(request.namespace)
        self.active_player(request.sid, request.namespace)

    def on_inspect_player(self, message):
        print ("inspect:", message["player"])
        role = startedGame[request.namespace].handle_move(message["card"],target=message["player"])
        print(role)
        emit("reveal_role", {"role": role,"player":message["player"]}, room=request.sid)
        self.all_update_hand(request.namespace)
        self.active_player(request.sid, request.namespace)

    def on_play_action(self, message):
        print("action")
        startedGame[request.namespace].handle_move(message["card"],target=message['target'])
        self.all_update_hand(request.namespace)
        self.active_player(request.sid, request.namespace)

    def active_player(self, sid, ns):
        self.broadcastGameLog(startedGame[ns].log_message)
        current_player = startedGame[ns].get_current_player()
        nround = startedGame[ns].rounds + 1
        ncards = len(startedGame[ns].deck.cards)
        emit("wait_for_player", {"active" : 0, "player":current_player[1], "round": nround, "deck": ncards}, broadcast= True)
        emit("wait_for_player", {"active" : 1, "player":current_player[1], "round": nround, "deck": ncards}, room=current_player[0])
        if startedGame[ns].state == "round_over": 
            scores = startedGame[ns].round_over()
            self.broadcastGameLog(startedGame[ns].log_message)
            emit("round_over", sorted(scores.items(), key=lambda kv: kv[1], reverse = True), broadcast= True)
        if startedGame[ns].state == "start_round":
            startedGame[ns].start_round()
            emit("update_board", startedGame[ns].board.getBoardData(), broadcast= True)
            emit("available_cells", startedGame[ns].board.available, broadcast= True)
            for player in startedGame[ns].players:
                emit("update_hand", startedGame[ns].player_hand_list(player.name), room=player.sid)
                emit("update_role", {"role":startedGame[ns].get_player_role(player.name)}, room=player.sid)
            self.broadcastGameLog(startedGame[ns].log_message)
        elif startedGame[ns].state == "game_over":
            startedGame[ns].game_over()
            emit("game_over", startedGame[ns].winners, broadcast= True)
            self.broadcastGameLog(startedGame[ns].log_message)
        emit("update_players", startedGame[ns].players_list(), broadcast=True) 

    def all_update_hand(self, ns):
        for player in startedGame[ns].players:
            print(player.sid)
            emit("update_hand", startedGame[ns].player_hand_list(player.name), room=player.sid)
            emit("update_role", {"role":startedGame[ns].get_player_role(player.name)}, room=player.sid)
        emit("update_players", startedGame[ns].players_list(), broadcast=True)

    def broadcastGameLog(self, message):
        if (message != self.last_log):
            emit('game_message', {'message':message}, broadcast=True)
            self.last_log = message
    
    def on_disconnect(self):
        print(current_user.username, "game disconnect")
        startedGame[request.namespace].player_disconnected(current_user.username)

    def on_leave(self):
        print(current_user.username, "game leave")
        startedGame[request.namespace].player_disconnected(current_user.username)
        return redirect('dashboard.html')

    def on_received_timer(self, data):
        print("update stuff after timeout")
        self.all_update_hand(request.namespace)
        self.active_player(request.sid, request.namespace)
    
    def on_update_me(self, data):
        print("update player")
        emit("update_players", startedGame[request.namespace].players_list(), room=request.sid)
        emit("update_hand", startedGame[request.namespace].player_hand_list(current_user.username), room=request.sid)
        emit("update_role", {"role":startedGame[request.namespace].get_player_role(current_user.username)}, room=request.sid)
        emit("update_board", startedGame[request.namespace].board.getBoardData(), broadcast= True)
        emit("available_cells", startedGame[request.namespace].board.available, broadcast= True)
    