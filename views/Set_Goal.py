import streamlit as st
from utils.db import create_connection, update_user
from utils.calculations import weight_loss, weight_gain
from utils.user import User
from utils.custom_css import load_css
from utils.ui_helper import render_sidebar_info, render_footer
from sqlalchemy import text

load_css()
render_sidebar_info(
    icon_path="icons/flag.png",
    title="Set Goal",
    text_lines=["Define your next weight target and a timeframe to achieve it."]
)

user_session = st.session_state.get("user")

conn = create_connection()
with conn.session as s:
    user_email = user_session[0]
    row = s.execute(
        text("SELECT * FROM users WHERE email = :email"), 
        {"email": user_email}
    ).fetchone()

if not row:
    st.error("User profile not found!")
    st.stop()

user = User(*row[1:])
user.id = row[0]

st.title(":material/track_changes: Set Your Weight Goal")

goal_type = st.radio("What is your goal?", ["Weight Loss", "Weight Gain"])

if goal_type == "Weight Loss":
    amount = st.number_input("How many kgs do you want to lose?", min_value=0.5, max_value=100.0, step=0.5)
else:
    amount = st.number_input("How many kgs do you want to gain?", min_value=0.5, max_value=100.0, step=0.5)

months = st.number_input("In how many months do you want to achieve this?", min_value=1, max_value=100)

if st.button("Set Goal", width=100):
    user.goal = goal_type.lower()
    update_user(user)
    
    if goal_type == "Weight Loss":
        result = weight_loss(user, amount_to_lose=amount, months=months)
    else:
        result = weight_gain(user, amount_to_gain=amount, months=months)

    if result.startswith("\nYour goal may be unhealthy") or "unhealthy" in result.lower():
        st.warning(result)
    else:
        st.success(result)

render_footer()