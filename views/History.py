import streamlit as st
from utils.db import create_connection
from utils.custom_css import load_css
from utils.ui_helper import render_sidebar_info, render_footer
from sqlalchemy import text
import pandas as pd

load_css()
render_sidebar_info(
    icon_path="icons/history.png",
    title="History",
    text_lines=["Review your past meal plans and weight goals. This is your complete history."]
)

user_session = st.session_state.get("user")

st.title(":material/history: Your History")


conn = create_connection()
with conn.session as s:
    user_email = user_session[0]
    user_row = s.execute(
        text("SELECT id FROM users WHERE email = :email"), 
        {"email": user_email}
    ).fetchone()

    if not user_row:
        st.error("User profile not found! Please complete profile setup.")
        st.stop()

    user_id = user_row[0]

    tab1, tab2 = st.tabs(["Meal Plan History", "Goal History"])

    with tab1:
        st.subheader("Your Saved Meal Plans")
        
        plans = s.execute(
            text('''
                SELECT plan_type, custom_note, meal_plan, timestamp
                FROM meal_plans
                WHERE user_id = :uid
                ORDER BY timestamp DESC
            '''), {"uid": user_id}
        ).fetchall()

        if not plans:
            st.info("You have no meal plans yet!")
        else:
            st.success(f"Showing {len(plans)} saved meal plans")
            count = 1
            for plan in plans:
                plan_type, note, meal_plan, timestamp = plan
                pd_timestamp = pd.to_datetime(timestamp)
                ist = pd_timestamp.tz_convert("Asia/Kolkata")
                time = ist.strftime("%d %b %Y, %I:%M %p")

                with st.expander(f"[{count}] {time} | Type: {plan_type.capitalize()}"):
                    if note and note.strip():
                        st.markdown(f"Custom Note: {note}")
                    st.markdown("Full Meal Plan:")
                    st.markdown(meal_plan)
                count += 1

with tab2:
    st.subheader("Your Past Weight Goals")

    rows = s.execute(
            text('''
                SELECT goal_type, target_weight, target_time_months, daily_calorie_change, target_calories, health_warning, timestamp
                FROM goals
                WHERE user_id = :uid
                ORDER BY timestamp DESC
            '''), {"uid": user_id}
        ).fetchall()

    if not rows:
        st.info("No past goal records!")
    else:
        count = 1
        for row in rows:
            goal_type, target_weight, months, change, target_calories, warning, timestamp = row
            pd_timestamp = pd.to_datetime(timestamp)
            ist = pd_timestamp.tz_convert("Asia/Kolkata")
            time = ist.strftime("%d %b %Y, %I:%M %p")

            with st.expander(f"{count}. [{time}] • {goal_type.capitalize()} Goal"):
                st.markdown(f"- Target Weight: {target_weight:.2f} kg")
                st.markdown(f"- Time Frame: {months} months")
                st.markdown(f"- Daily Calorie {'Deficit' if goal_type == 'loss' else 'Surplus'}: {int(change)} kcal")
                st.markdown(f"- Target Calories: {int(target_calories)} kcal/day")
                if warning and warning.strip():
                    st.warning(warning)
            count += 1

render_footer()