import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = 'database.db'

def init_db():
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
    (username TEXT, password TEXT, UNIQUE (username)) ''')
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

def find_user(username,password):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    user = c.execute('''SELECT * FROM users WHERE
    username = ?''', (username,)).fetchone()
    if user is not None:
        if check_password_hash(user[1], password):
            return user
    return None

def find_username(username):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    user = c.execute("SELECT username from users where username = (?)",
                    [username]).fetchone()
    userid = user[0]
    return userid

init_db()