from utils.db import create_connection
import hashlib
import sqlite3


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, email, password):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM auth WHERE username = ? OR email = ?", (username, email))
    if cursor.fetchone():
        return False, "Username or Email already exists!"
    
    hashed = hash_password(password)

    cursor.execute("INSERT INTO auth (username, email, password) VALUES (?, ?, ?)", (username, email, hashed))
    
    conn.commit()
    conn.close()

    return True, "Account Created Successfully!"


def login_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()

    hashed = hash_password(password)

    cursor.execute("SELECT * FROM auth WHERE username = ? AND password = ?", (username, hashed))
    user = cursor.fetchone()
    conn.close()

    return user 

