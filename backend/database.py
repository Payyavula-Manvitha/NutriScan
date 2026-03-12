import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT UNIQUE,
password TEXT,
age INTEGER,
height REAL,
weight REAL
)
""")

conn.commit()

def add_user(name,email,password,age,height,weight):

    cursor.execute(
        "INSERT INTO users(name,email,password,age,height,weight) VALUES(?,?,?,?,?,?)",
        (name,email,password,age,height,weight)
    )

    conn.commit()


def login_user(email,password):

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email,password)
    )

    return cursor.fetchone()


def get_all_users():

    cursor.execute("SELECT name,email,age,height,weight FROM users")

    return cursor.fetchall()