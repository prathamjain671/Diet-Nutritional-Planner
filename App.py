import streamlit as st
from utils.db import create_table, create_connection
from auth import login_user, register_user
from utils.custom_css import load_css
from sqlalchemy import text

st.set_page_config(page_title="Diet & Nutritional Planner", layout="wide")
load_css()
create_table()

if "user" not in st.session_state:
    st.session_state.user = None
if "profile_exists" not in st.session_state:
    st.session_state.profile_exists = False

if st.session_state.user is None:

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


    if "page_choice" not in st.session_state:
        st.session_state.page_choice = "Login"

    st.title("Diet & Nutritional Planner")

    if st.session_state.page_choice == "Login":
        st.subheader("Login to Your Account")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Login", width='stretch', type="primary"):
                user = login_user(username, password)

                if user:
                    with st.container(width='stretch'):
                        st.success(f"Welcome back, {user[1]}")
                    st.session_state.user = user

                    conn = create_connection()
                    with conn.session as s:
                        profile_exists = s.execute(
                            text("SELECT 1 FROM users WHERE email = :email"), 
                            {"email": st.session_state.user[0]}
                        ).fetchone() is not None
                        st.session_state.profile_exists = profile_exists

                    st.rerun()    
                else:
                    with st.container(width='stretch'):
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
                    with st.container(width='stretch'):
                        st.error("Passwords do not match!")
                else:
                    success, message = register_user(username, email, password)

                    if success:
                        with st.container(width='stretch'):
                            st.success(message)
                        st.session_state.user = (email, username)
                        st.session_state.profile_exists = False
                        st.rerun()  
                    else:
                        with st.container():
                            st.error(message)
        with col2:
            if st.button("Have an account? Log in", width='stretch'):
                st.session_state.page_choice = "Login"
                st.rerun()
        
else:
    conn = create_connection()
    with conn.session as s:
        profile_exists = s.execute(
            text("SELECT 1 FROM users WHERE email = :email"), 
            {"email": st.session_state.user[0]}
        ).fetchone() is not None

    if not st.session_state.profile_exists:
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
        
        with open("views/Profile_Update.py", "r") as f:
            file_code = f.read()
        exec(file_code, globals())

        if st.session_state.profile_exists:
            st.rerun()

    else:
        pages = st.navigation([
            st.Page("views/Dashboard.py", title="Dashboard", icon=":material/dashboard:"),
            st.Page("views/Profile_Update.py", title="Health Profile", icon=":material/person_edit:"),
            st.Page("views/Progress.py", title="Progress", icon=":material/chart_data:"),
            st.Page("views/Meal_Planner.py", title="Meal Planner", icon=":material/menu_book_2:"),
            st.Page("views/Set_Goal.py", title="Set Goal", icon=":material/flag:"),
            st.Page("views/History.py", title="History", icon=":material/history:"),
            st.Page("views/Calculations.py", title="Calculations", icon=":material/calculate:"),
            st.Page("views/Food_Info.py", title="Food Info", icon=":material/search:"),
            st.Page("views/Account.py", title="Account", icon=":material/account_circle:"),
        ])

        pages.run()