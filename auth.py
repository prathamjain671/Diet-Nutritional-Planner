import streamlit as st
from utils.db import create_connection
import bcrypt
from sqlalchemy import text

def hash_password(password):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)

    return hashed_bytes.decode('utf-8')

def verify_password(plain_password, hashed_password):
    try:
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.strip().encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        print(f"Error during password verification: {e}")
        return False

def change_password(email, old_password, new_password):
    conn = create_connection()
    with conn.session as s:
        user_auth_row = s.execute(
            text("SELECT * FROM auth WHERE email = :email"), 
            {"email": email}
        ).fetchone()

        if user_auth_row:
            hashed_password_from_db = user_auth_row[3]
            if verify_password(old_password, hashed_password_from_db):
                new_hashed = hash_password(new_password)
                s.execute(
                    text("UPDATE auth SET password = :new_pass WHERE email = :email"), 
                    {"new_pass": new_hashed, "email": email}
                )
                s.commit()
                return True, "Password Updated Successfully!"
            else:
                return False, "Incorrect Old Password!"
        else:
            return False, "User not found!"

def register_user(username, email, password):
    conn = create_connection()
    with conn.session as s:
        user = s.execute(
            text("SELECT * FROM auth WHERE username = :username OR email = :email"), 
            {"username": username, "email": email}
        ).fetchone()
        
        if user:
            return False, "Username or Email already exists!"
        
        hashed = hash_password(password)
        s.execute(
            text("INSERT INTO auth (username, email, password) VALUES (:username, :email, :password)"), 
            {"username": username, "email": email, "password": hashed}
        )
        s.commit()
        return True, "Account Created Successfully!"

def login_user(username, password):
    conn = create_connection()
    with conn.session as s:
        user_auth_row = s.execute(
            text("SELECT * FROM auth WHERE username = :username"), 
            {"username": username}
        ).fetchone()

    if user_auth_row:
        hashed_password_from_db = user_auth_row[3]
        if verify_password(password, hashed_password_from_db):
            return (user_auth_row[2], user_auth_row[1])
    return None

def update_username(email, new_username):
    conn = create_connection()
    with conn.session as s:
        user = s.execute(
            text("SELECT * FROM auth WHERE username = :username AND email != :email"), 
            {"username": new_username, "email": email}
        ).fetchone()
        
        if user:
            return False, "The username is already taken!"
        
        try:
            s.execute(
                text("UPDATE auth SET username = :username WHERE email = :email"), 
                {"username": new_username, "email": email}
            )
            s.commit()
            return True, "Username updated successfully!"
        except Exception as e:
            return False, "An error occurred! Please try again later."