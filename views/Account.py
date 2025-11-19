import streamlit as st
from utils.user import User
from utils.db import create_connection
from auth import change_password, update_username
from utils.custom_css import load_css
from utils.ui_helper import render_sidebar_info, render_footer
from sqlalchemy import text

load_css()
render_sidebar_info(
    icon_path="icons/account_circle.png",
    title="Account",
    text_lines=["Manage your account security, change your username or password, and log out."]
)

user_session = st.session_state.get("user")

conn = create_connection()
with conn.session as s:
    user_email = user_session[0]
    user_name = user_session[1]
    user_data = s.execute(
        text("SELECT * FROM users WHERE email = :email"), 
        {"email": user_email}
    ).fetchone()

user = User(*user_data[1:])
user.id = user_data[0]

st.title(f":material/settings_account_box: Account Settings: {user_name}")

with st.container(border=True):
    st.subheader(":material/demography: Your Account Details")
    st.text_input("Username", value=user_name, disabled=True)
    st.text_input("Email", value=user.email, disabled=True)
    
    st.subheader(":material/clinical_notes: Your Current Health Profile")
    st.text_input("Current Goal", value=user.goal.title(), disabled=True)
    st.text_input("Current Height", value=f"{user.height:.2f} cm", disabled=True)
    st.text_input("Current Weight", value=f"{user.weight:.2f} kg", disabled=True)

    
    if st.button("Update Health Details (Go to Health Profile)"):
        st.switch_page("views/Profile_Update.py")

st.divider()

with st.expander("Change Your Username"):
    with st.form("username_form"):
        new_username = st.text_input("New Username", value=user_name)
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
                    st.rerun()
                else:
                    st.error(message)

st.divider()

col1, col2 = st.columns(2)
with col1:
    if st.button("Log Out", type="primary",width='stretch'):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

with col2:
    if st.button("Go to Dashboard",width='stretch'):
        st.switch_page("views/Dashboard.py")

render_footer()