import streamlit as st
from utils.db import create_table, create_connection
from auth import login_user, register_user
from utils.custom_css import load_css

load_css()
st.set_page_config(page_title="Digital Diet & Nutritional Planner", layout="centered")

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)

create_table()

if "user" not in st.session_state:
    st.session_state.user = None

if "page_choice" not in st.session_state:
    st.session_state.page_choice = "Login"

st.title("Digital Diet & Nutritional Planner")

if st.session_state.page_choice == "Login":
    st.subheader("Login to Your Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login", width='stretch', type="primary"):
            user = login_user(username, password)

            if user:
                user_email = user[0]
                user_name = user[1]

                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM users WHERE email = ?", (user_email,))
                profile_exists = cursor.fetchone()

                st.success(f"Welcome back, {user[1]}")
                st.session_state.user = user
                
                if profile_exists:
                    st.switch_page("pages/Dashboard.py")
                else:
                    st.session_state.new_email = user_email
                    st.session_state.new_username = user_name
                    st.switch_page("pages\Profile_Update.py")
            else:
                st.error("Invalid Credentials!")

    with col2:
        if st.button("Don't have an account? Sign up", width='stretch'):
            st.session_state.page_choice = "Register"
            st.rerun()

elif st.session_state.page_choice == "Register":
    st.subheader("Create a New Account")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password  = st.text_input("Confirm Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Register", width='stretch', type="primary"):
            if password != confirm_password:
                st.error("Passwords do not match!")
            else:
                success, message = register_user(username, email, password)

                if success:
                    st.success(message)
                    st.session_state.user = (email, username)
                    st.switch_page("pages\Profile_Update.py")
                else:
                    st.error(message)
    with col2:
        if st.button("Have an account? Log in", width='stretch'):
            st.session_state.page_choice = "Login"
            st.rerun()
        