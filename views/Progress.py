import streamlit as st
import pandas as pd
from utils.db import create_connection
from datetime import datetime
from zoneinfo import ZoneInfo
import altair as alt
from utils.custom_css import load_css
from utils.ui_helper import render_sidebar_info

load_css()
render_sidebar_info(
    icon_path="icons/chart_data.png",
    title="Progress",
    text_lines=["See detailed charts of your weight, BMI, and TDEE over time."]
)

user_session = st.session_state.get("user")

st.title(":material/steps: Your Progress")

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
        ORDER BY timestamp DESC
''', (user_id,))

progress = cursor.fetchall()

cursor.execute('''
        SELECT tdee, bmi, bmi_category, timestamp
        FROM calculations
        WHERE user_id = ?
        ORDER BY timestamp DESC
''', (user_id,))

calc = cursor.fetchall()

conn.close()

with st.container(border=True):
    if not progress:
        st.info("No progress data found!")
    else:
        st.subheader("Profile History")
        df_progress = pd.DataFrame(progress, columns=["Weight (kg)", "Height (cm)", "Age", "Goal", "Diet", "Activity", "Date"])
        df_progress["Date"] = pd.to_datetime(df_progress["Date"])
        df_progress["Date"] = df_progress["Date"].dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata")
        df_progress["Date"] = df_progress["Date"].dt.strftime("%d %b %Y, %I:%M %p")
        st.dataframe(
            df_progress.style.format({
                "Weight (kg)": "{:.2f}",
                "Height (cm)": "{:.2f}"
            }),
            width='stretch'
        )

    if not calc:
        st.info("No calculations data found!")
    else:
        st.subheader("Calculation History")
        df_calc = pd.DataFrame(calc, columns=["TDEE", "BMI", "BMI Category", "Date"])
        df_calc["Date"] = pd.to_datetime(df_calc["Date"])
        df_calc["Date"] = df_calc["Date"].dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata")
        df_calc["Date"] = df_calc["Date"].dt.strftime("%d %b %Y, %I:%M %p")
        st.dataframe(
            df_calc.style.format({
                "TDEE": "{:.2f}",
                "BMI": "{:.2f}"
            }),
            width='stretch'
        )

if not progress or not calc:
    st.warning("Not enough data for visualization!")
else:
    with st.container(border=True):
        st.subheader(":material/bar_chart_4_bars: Visualize Your Progress")

        df_progress_raw = pd.DataFrame(progress, columns=["Weight (kg)", "Height (cm)", "Age", "Goal", "Diet", "Activity", "Date"])
        df_progress_raw["Date"] = pd.to_datetime(df_progress_raw["Date"])
        df_progress_raw["Day"] = df_progress_raw["Date"].dt.date
        df_weight_plot = df_progress_raw.groupby("Day").last().reset_index()

        df_calc_raw = pd.DataFrame(calc, columns=["TDEE", "BMI", "BMI Category", "Date"])
        df_calc_raw["Date"] = pd.to_datetime(df_calc_raw["Date"])
        df_calc_raw["Day"] = df_calc_raw["Date"].dt.date
        df_calc_plot = df_calc_raw.groupby("Day").last().reset_index()
        

        with st.container(border=True):
            st.markdown("#### Weight Over Time")
            weight_chart = alt.Chart(df_weight_plot).mark_line(point=True, color="#0d6efd").encode(
                x=alt.X('Day', type='temporal', title=None, axis=alt.Axis(format="%d-%b")),
                y=alt.Y('Weight (kg)', title=None),
                
                tooltip=[
                    alt.Tooltip('Date', format="%Y-%m-%d", title="Date"),
                    alt.Tooltip('Date', format="%I:%M %p", title="Time"),
                    alt.Tooltip('Weight (kg):Q', format='.2f', title='Weight (kg)')
                ]
            ).interactive()
            st.altair_chart(weight_chart)

        with st.container(border=True):
            st.markdown("#### TDEE Over Time")
            tdee_chart = alt.Chart(df_calc_plot).mark_line(point=True, color="#28a745").encode(
                x=alt.X('Day', type='temporal', title=None, axis=alt.Axis(format="%d-%b")),
                y=alt.Y('TDEE', title=None),
                
                tooltip=[
                    alt.Tooltip('Date', format="%Y-%m-%d", title="Date"),
                    alt.Tooltip('Date', format="%I:%M %p", title="Time"),
                    alt.Tooltip('TDEE:Q', format='.2f', title='TDEE')
                ]
            ).interactive()
            st.altair_chart(tdee_chart)

        with st.container(border=True):
            st.markdown("#### BMI Over Time")
            bmi_chart = alt.Chart(df_calc_plot).mark_line(point=True, color="#dc3545").encode(
                x=alt.X('Day', type='temporal', title=None, axis=alt.Axis(format="%d-%b")),
                y=alt.Y('BMI', title=None),
                
                tooltip=[
                    alt.Tooltip('Date', format="%Y-%m-%d", title="Date"),
                    alt.Tooltip('Date', format="%I:%M %p", title="Time"),
                    alt.Tooltip('BMI:Q', format='.2f', title='BMI')
                ]
            ).interactive()
            st.altair_chart(bmi_chart)