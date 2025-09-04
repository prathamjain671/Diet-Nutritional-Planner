import streamlit as st
from utils.db import create_connection
from datetime import datetime
from zoneinfo import ZoneInfo


st.title("Meal History")

user = st.session_state.get("user")
if not user:
    st.error("Please login first to view this page!")
    st.stop()

conn = create_connection()
cursor = conn.cursor()

cursor.execute('''
        SELECT plan_type, custom_note, meal_plan, timestamp
        FROM meal_plans
        WHERE user_id = ?
        ORDER BY timestamp DESC
''', (user[0],))

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
        