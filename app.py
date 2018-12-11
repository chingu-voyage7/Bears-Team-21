#!/usr/bin/env python
import os, sqlite3
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, json
from flask_socketio import SocketIO, emit, send, join_room, leave_room, close_room, rooms, disconnect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from classes.socket_module import GameLobbyNs
from classes.database import add_user, find_user, find_username
import classes.settings as config

app = Flask(__name__)
app.secret_key = 'thisissecret' # os.getenv("SABOTEUR_SECRET_KEY")
DATABASE = 'database.db'
db = sqlite3.connect(DATABASE)
c = db.cursor()

socketio = SocketIO(app, ping_timeout=30000)

game_rooms = {'roomId1': ["Jhon","Alex","Alice"],
            'roomId2': ["Bob"],
            'roomId3': ["Ted","Max"]}


socketio.on_namespace(GameLobbyNs('/lobby'))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, username):
        self.username = username
    @property
    def id(self):
        return self.username

@login_manager.user_loader
def load_user(id):
    return User(find_username(id))
 
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect('dashboard')
    return render_template('index.html')

@app.route('/signup', methods=['GET','POST'])
def signup(text=''):
    if current_user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        text = add_user(username,password)
    return render_template('signup.html', text=text)

@app.route('/login', methods=['GET','POST'])
def login(text=''):    
    if current_user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = find_user(username, password)
        if user is not None:
            login_user(User(username))
            return redirect('dashboard')
        else:
            text = 'Wrong username or password'
    return render_template('login.html', text=text)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
