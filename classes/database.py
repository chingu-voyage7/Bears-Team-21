import sqlite3

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
    try:
        c.execute('INSERT INTO users VALUES ("%s", "%s")' % (username, password))
        db.commit()
    except sqlite3.Error as e:
        if str(e).startswith('UNIQUE'):
            return 'Username already in use.'
        return 'Error. Please try again.'
    except Exception as e:
        return 'Error. Please try again.'
    db.close()
    return 'Signed up successfully!'

init_db()