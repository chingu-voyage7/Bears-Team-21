#!/usr/bin/env python
import os, sqlite3
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, json
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from classes.socket_module import GameRoomNamespace
from classes.database import add_user, find_user
import classes.settings as config

app = Flask(__name__)
app.config['SECRET KEY'] = 'thisissecret' # os.getenv("SABOTEUR_SECRET_KEY")

DATABASE = 'database.db'
db = sqlite3.connect(DATABASE)
c = db.cursor()

socketio = SocketIO(app)
game_rooms = {'roomId1': ["Jhon","Alex","Alice"],
            'roomId2': ["Bob"],
            'roomId3': ["Ted","Max"]}

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET','POST'])
def signup(text=''):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        text = add_user(username,password)
    return render_template('signup.html', text=text)

@app.route('/login', methods=['GET','POST'])
def login(text=''):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if find_user(username,password) is not None:
            return redirect('dashboard')
        else:
            text = 'Wrong username or password'
    return render_template('login.html', text=text)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@socketio.on('connect')
def send_rm_list():
    join_room('/lobby')
    print('/room joined')
    emit('roomsList',make_rm_List(),room='/lobby')

@socketio.on('create_room')
def on_create(data):
    #if not current_user.is_authenticated:
    #    print (request.sid + ' unauthorized')
    #    return
    print(data)
    # create game room, query game-manager.py for new game room
    #room_entry = data#{STUFF: "TO-BE DEFINED", roomId: random_string(20), players: []}
    roomId = data['roomId']
    game_rooms[roomId] = [data["userId"]]
    join_room(roomId)
    emit('join_room', {'game_roomId': roomId})
    emit('roomsList',make_rm_List(), broadcast=True)

@socketio.on('join_room')
def on_join(data):
    #if not current_user.is_authenticated:
    #    print (request.sid + ' unauthorized')
    #    return
    print(request.sid + " joining " + data['roomId'])
    # join a game room
    roomId = data['roomId']
    if (roomId in game_rooms) and (len(game_rooms[roomId]) < config.MAX_ROOM_SIZE)  and (data['userId'] not in game_rooms[roomId]):
        game_rooms[roomId].append(data['userId'])
        leave_room('/lobby')
        join_room(roomId)
        send(game_rooms[roomId], roomId=roomId)
        emit('roomsList',make_rm_List(), room='/lobby')
        socketio.on_namespace(GameRoomNamespace('/lobby'))
    else:
        emit('error', {'error': 'Unable to join room.'})

@socketio.on("leave")
def on_leave(roomId):
        leave_room(roomId)
        emit("leave game room", room=roomId)

def make_rm_List():
    roomList = {}
    for key in game_rooms:
        roomList[key] = len(game_rooms[key])
    return roomList

if __name__ == "__main__":
    app.debug = True
    app.run()
