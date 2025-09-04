import streamlit as st
from utils.db import create_table
from auth import login_user, register_user


st.set_page_config(page_title="Digital Diet & Nutritional Planner", layout="centered")
create_table()

if "user" not in st.session_state:
    st.session_state.user = None

st.title("Digital Diet & Nutritional Planner")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
    st.subheader("Login to Your Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(username, password)

        if user:
            st.success(f"Welcome back, {user[1]}")
            st.session_state.user = user

            st.switch_page("pages/Dashboard.py")
        else:
            st.error("Invalid Credentials!")

elif choice == "Register":
    st.subheader("Create a New Account")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password  = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match!")
        else:
            success, message = register_user(username, email, password)

            if success:
                st.success(message)

                st.session_state.new_username = username
                st.session_state.new_email = email

                st.switch_page("pages/Profile_Setup.py")
            else:
                st.error(message)