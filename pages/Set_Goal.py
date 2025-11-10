import streamlit as st
from utils.db import create_connection
from utils.calculations import weight_loss, weight_gain
from utils.user import User

user_session = st.session_state.get("user")
if not user_session:
    st.warning("Please login to view this page!")
    st.stop()

conn = create_connection()
cursor = conn.cursor()

user_email = user_session[0]

cursor.execute("SELECT * FROM users WHERE email = ?", (user_email,))
row = cursor.fetchone()
conn.close()

if not row:
    st.error("User profile not found!")
    st.stop()

user_session = User(*row[1:])
user_session.id = row[0]

st.set_page_config(page_title="Set Goal", layout="centered")
st.title("Set Your Weight Goal")

goal_type = st.radio("What is your goal?", ["Weight Loss", "Weight Gain"])
target_weight = st.number_input("Enter your target weight (kg)", min_value=10, max_value=300)
months = st.number_input("In how many months do you want to achieve this?", min_value=1, max_value=100)

if st.button("Set Goal"):
    if goal_type == "Weight Loss":
        result = weight_loss(user_session, target_weight, months)
    else:
        result = weight_gain(user_session, target_weight, months)

    if result.startswith("\nYour goal may be unhealthy") or "unhealthy" in result.lower():
        st.warning(result)
    else:
        st.success(result)
