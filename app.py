from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = ''
db = SQLAlchemy(app)
s = db.session
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.debug = True
    app.run()