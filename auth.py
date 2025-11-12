from utils.db import create_connection
from passlib.context import CryptContext
import sqlite3

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


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

    cursor.execute("SELECT * FROM auth WHERE username = ?", (username,))
    user_auth_row = cursor.fetchone()
    conn.close()

    if user_auth_row:
        hashed_password_from_db = user_auth_row[3]

        if verify_password(password, hashed_password_from_db):
            return(user_auth_row[2], user_auth_row[1])

    return None

