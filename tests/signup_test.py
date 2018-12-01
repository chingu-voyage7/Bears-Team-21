import unittest
from classes.database import add_user
import sqlite3
import random

DATABASE = 'database.db'
db = sqlite3.connect(DATABASE)
c = db.cursor()

class TestDB(unittest.TestCase):

    def test_add_new_user(self):
        username = str(random.randint(1,10000000000000))
        password = 'qwfpp'
        self.assertEqual('Signed up successfully!', add_user(username,password))

    def test_add_same_user(self):
        username = str(random.randint(1,10000000000000))
        password = 'qrat'
        add_user(username, password)
        self.assertEqual('Username already in use.',
        add_user(username, password))

if __name__ == '__main__':
    unittest.main()
