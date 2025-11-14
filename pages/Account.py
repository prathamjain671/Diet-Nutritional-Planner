import streamlit as st
from utils.user import User
from utils.db import create_connection
from auth import change_password, update_username
import time
from utils.custom_css import load_css
from utils.ui_helper import render_sidebar_info

st.set_page_config(page_title="Account", layout="wide")
load_css()

render_sidebar_info(
    title="Account",
    text_lines=["Manage your account security, change your username or password, and log out."]
)

user_session = st.session_state.get("user")
if not user_session:
    st.error("Please login to view this page!")
    st.stop()

conn = create_connection()
cursor = conn.cursor()
user_email = user_session[0]
user_name = user_session[1]

cursor.execute("SELECT * FROM users WHERE email = ?", (user_email,))
user_data = cursor.fetchone()
conn.close()

user = User(*user_data[1:])
user.id = user_data[0]

st.title(f"Account Settings: {user_name}")

with st.container(border=True):
    st.subheader("Your Account Details")
    st.text_input("Username", value=user_name, disabled=True)
    st.text_input("Email", value=user.email, disabled=True)
    
    st.subheader("Your Current Health Profile")
    st.text_input("Current Goal", value=user.goal.title(), disabled=True)
    st.text_input("Current Height", value=f"{user.height} cm", disabled=True)
    st.text_input("Current Weight", value=f"{user.weight} kg", disabled=True)

    
    if st.button("Update Health Details (Go to Profile Update)"):
        st.switch_page("pages/Profile_Update.py")

st.divider()

with st.expander("Change Your Username"):
    with st.form("username_form"):
        new_username = st.text_input("New username", value=user_name)
        submitted_username = st.form_submit_button("Change Username")

        if submitted_username:
            if not new_username:
                st.error("Please enter a new username!")
            elif new_username == user_name:
                st.info("That is already your username!")
            else:
                success, message = update_username(user_email, new_username)

                if success:
                    st.session_state.user = (user_email, new_username)
                    st.success(message)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(message)


with st.expander("Change Your Password"):
    with st.form("password_form"):
        old_password = st.text_input("Old Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")

        submitted = st.form_submit_button("Change Password")

        if submitted:
            if new_password != confirm_password:
                st.error("New passwords do not match!")
            if old_password == new_password:
                st.error("New Password cannot be same as Old Password!")
            elif not old_password or not new_password:
                st.error("Please fill out all the fields!")
            else:
                success, message = change_password(user_email, old_password=old_password, new_password=new_password)
                if success:
                    st.success(message)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(message)

st.divider()

col1, col2 = st.columns(2)
with col1:
    if st.button("Log Out", type="primary",width='stretch'):
        for key in st.session_state.keys():
            del st.session_state[key]

        st.switch_page("App.py")

with col2:
    if st.button("Go to Dashboard",width='stretch',type="primary"):
        st.switch_page("pages/Dashboard.py")