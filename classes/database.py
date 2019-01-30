import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import datetime, time


DATABASE = 'database.db'

def init_db():
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
    (username TEXT, password TEXT, UNIQUE (username)) ''')
    c.execute('''CREATE TABLE IF NOT EXISTS scores 
    (usernames TEXT, roles TEXT, scores TEXT, gamename TEXT, UNIQUE (gamename)) ''')
    db.commit()
    db.close()

def add_user(username, password):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    password = generate_password_hash(password)
    try:
        c.execute('INSERT INTO users VALUES (?, ?)',(username, password,))
        db.commit()
    except sqlite3.Error as e:
        if str(e).startswith('UNIQUE'):
            return 'Username already in use.'
        return 'Error. Please try again.'
    except Exception as e:
        return 'Error. Please try again.'
    db.close()
    return 'Signed up successfully!'

def add_scores(usernames, roles, scores, gamename):
    st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
    gameid = gamename + st
    print(gameid)
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    try:
        c.execute('INSERT INTO scores VALUES (?, ?, ?, ?)',(usernames, roles,scores, gameid))
        db.commit()
    except sqlite3.Error as e:
        if str(e).startswith('UNIQUE'):
            return 'Game scores already in DB.'
        return 'Error. Please try again.'
    except Exception as e:
        return 'Error. Please try again.'
    db.close()
    return gameid

def find_user(username,password):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    user = c.execute('''SELECT * FROM users WHERE
    username = ?''', (username,)).fetchone()
    if user is not None:
        if check_password_hash(user[1], password):
            return user
    return None

def find_scores(gameid):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    scores = c.execute('''SELECT * FROM scores WHERE
    gamename = ?''', (gameid,)).fetchone()
    print(scores)
    return scores

init_db()