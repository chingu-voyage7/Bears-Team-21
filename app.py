import os
from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from classes.socket_module import GameRoomNamespace
from classes.database import add_user, find_user
import string, random

app = Flask(__name__)
app.config['SECRET KEY'] = 'thisissecret' # os.getenv("SABOTEUR_SECRET_KEY")

DATABASE = 'database.db'
db = sqlite3.connect(DATABASE)
c = db.cursor()

socketio = SocketIO(app)
game_rooms = {}

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

@socketio.on('create_room')
def on_create(data):
    print('Creating')
    # create game room, query game-manager.py for new game room
    room_entry = data#{STUFF: "TO-BE DEFINED", roomId: random_string(), players: []}
    roomId = room_entry['roomId']
    game_rooms[roomId] = roomId
    join_room(roomId)
    emit('join_room', {'game_roomId': roomId})

@socketio.on('join_room')
def on_join(data):
    print('Joining')
    # join a game room
    roomId = data['roomId']
    if roomId in game_rooms:
        game_rooms[roomId] # append(data['userId'])
        join_room(roomId)
        send(game_rooms[roomId], roomId=roomId)
        socketio.on_namespace(GameRoomNamespace(roomId))
    else:
        emit('error', {'error': 'Unable to join room.'})

@socketio.on("leave")
def on_leave(roomId):
        leave_room(roomId)
        emit("leave game room", room=roomId)

def random_string():
    # testing function
    N = 20
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

if __name__ == "__main__":
    app.debug = True
    app.run()
