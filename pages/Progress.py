import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.db import create_connection
from datetime import datetime
from zoneinfo import ZoneInfo

user_session = st.session_state.get("user")
if not user_session:
    st.error("Please login to view this page!")
    st.stop()

st.title("Your Progress")

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
        SELECT weight, height, age, goal, diet_preference, activity_level, timestamp
        FROM user_progress
        WHERE user_id = ?
        ORDER BY timestamp ASC
''', (user_session[0],))

progress = cursor.fetchall()

cursor.execute('''
        SELECT tdee, bmi, bmi_category, timestamp
        FROM calculations
        WHERE user_id = ?
        ORDER BY timestamp ASC
''', (user_session[0],))

calc = cursor.fetchall()

conn.close()


if not progress:
    st.info("No progress data found!")
else:
    st.subheader("Profile History")
    df_progress = pd.DataFrame(progress, columns=["Weight (kg)", "Height (cm)", "Age", "Goal", "Diet", "Activity", "Date"])
    df_progress["Date"] = pd.to_datetime(df_progress["Date"])
    df_progress["Date"] = df_progress["Date"].dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata")
    df_progress["Date"] = df_progress["Date"].dt.strftime("%d %b %Y, %I:%M %p")
    st.dataframe(df_progress, use_container_width=True)

if not calc:
    st.info("No calculations data found!")
else:
    st.subheader("Calculation History")
    df_calc = pd.DataFrame(calc, columns=["TDEE", "BMI", "BMI Category", "Date"])
    df_calc["Date"] = pd.to_datetime(df_calc["Date"])
    df_calc["Date"] = df_calc["Date"].dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata")
    df_calc["Date"] = df_calc["Date"].dt.strftime("%d %b %Y, %I:%M %p")
    st.dataframe(df_calc, use_container_width=True)

if not progress or not calc:
    st.warning("Not enough data for visualization!")
else:
    st.subheader("Visualize Your Progress")

    df_progress["Date"] = pd.to_datetime(df_progress["Date"])
    df_calc["Date"] = pd.to_datetime(df_calc["Date"])

    fig, ax = plt.subplots()
    ax.plot(df_progress["Date"], df_progress["Weight (kg)"], marker="o", color="blue")
    ax.set_title("Weight Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Weight (kg)")
    st.pyplot(fig)

    fig1, ax1 = plt.subplots()
    ax1.plot(df_calc["Date"], df_calc["TDEE"], marker="s", color="green")
    ax1.set_title("TDEE Over Time")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Calories")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    ax2.plot(df_calc["Date"], df_calc["BMI"], marker="^", color="red")
    ax2.set_title("BMI Over Time")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("BMI")
    st.pyplot(fig2)
    

    