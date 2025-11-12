from utils.db import create_connection
import bcrypt
import sqlite3


def hash_password(password):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)

    return hashed_bytes.decode('utf-8')

def verify_password(plain_password, hashed_password):
    try:
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        print(f"Error during password verification: {e}")
        return False


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

