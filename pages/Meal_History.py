import streamlit as st
from utils.db import create_connection
from datetime import datetime
from zoneinfo import ZoneInfo
from utils.custom_css import load_css
from utils.ui_helper import render_sidebar_info

st.set_page_config(page_title="Meal History", layout="wide")
load_css()

render_sidebar_info(
    title="Meal History",
    text_lines=["View all the meal plans you've generated in the past."]
)

st.title("Meal History")

user_session = st.session_state.get("user")
if not user_session:
    st.error("Please login first to view this page!")
    st.stop()

conn = create_connection()
cursor = conn.cursor()

user_email = user_session[0]

cursor.execute("SELECT id FROM users WHERE email = ?", (user_email,))
user_row = cursor.fetchone()

if not user_row:
    st.error("User profile not found! Please complete profile setup.")
    conn.close()
    st.stop()

user_id = user_row[0]

cursor.execute('''
        SELECT plan_type, custom_note, meal_plan, timestamp
        FROM meal_plans
        WHERE user_id = ?
        ORDER BY timestamp DESC
''', (user_session[0],))

plans = cursor.fetchall()
conn.close()

if not plans:
    st.info("You have no meal plans yet!")
else:
    st.success(f"Showing {len(plans)} saved meal plans")

    count = 1
    for plan in plans:
        
        plan_type, note, meal_plan, timestamp = plan

        utc = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        ist = utc.replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("Asia/Kolkata"))
        time = ist.strftime("%d %b %Y, %I:%M %p")

        with st.expander(f"[{count}] {time} | Type: {plan_type.capitalize()}"):
            if note.strip():
                st.markdown(f"Custom Note: {note}")
            st.markdown("Full Meal Plan:")
            st.markdown(meal_plan)

        count += 1
        