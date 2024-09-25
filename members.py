import sqlite3
from data_dict import random_users


def create():
    with sqlite3.connect('members.sqlite') as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                birth_date TEXT,
                gender TEXT,
                email TEXT,
                phonenumber TEXT,
                address TEXT,
                nationality TEXT,
                active BOOLEAN,
                github_username TEXT
            )
        ''')
        cur.executemany('INSERT INTO members (first_name, last_name, birth_date, gender, email, phonenumber, address, nationality, active, github_username) VALUES (:first_name, :last_name, :birth_date, :gender, :email, :phonenumber, :address, :nationality, :active, :github_username)', random_users)
        
        conn.commit()