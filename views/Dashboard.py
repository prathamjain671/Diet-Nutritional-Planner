import streamlit as st
from utils.db import create_connection
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
from utils.calculations import log_weight
from utils.user import User
import altair as alt
from utils.custom_css import load_css
from utils.ui_helper import render_sidebar_info, render_footer
from sqlalchemy import text

load_css()
render_sidebar_info(
    icon_path="icons/dashboard.png",
    title="Dashboard",
    text_lines=[
        "Welcome to the dashboard!",
        "Here you can view you key metrics, log your weight, navigate to other features and so much more."]
)

user_session = st.session_state.get("user")

conn = create_connection()
with conn.session as s:
    user_email = user_session[0]
    user_row = s.execute(
        text("SELECT * FROM users WHERE email = :email"), 
        {"email": user_email}
    ).fetchone()

    if not user_row:
        st.error("User profile not found! Please complete your profile.")
        st.stop()

    user_id = user_row[0]
    user = User(*user_row[1:])
    user.id = user_id

    macro_data = s.execute(
        text("SELECT target_calories FROM macros WHERE user_id = :uid ORDER BY timestamp DESC LIMIT 1"),
        {"uid": user_id}
    ).fetchone()
    target_cals = macro_data[0] if macro_data else 0

    macro_data = s.execute(
        text("SELECT protein, carbs, fats FROM macros WHERE user_id = :uid ORDER BY timestamp DESC LIMIT 1"),
        {"uid": user_id}
    ).fetchone()
    protein_goal = macro_data[0] if macro_data else 0
    carbs_goal = macro_data[1] if macro_data else 0
    fats_goal = macro_data[2] if macro_data else 0

    water_data = s.execute(
        text('SELECT water_intake FROM calculations WHERE user_id = :uid ORDER BY timestamp DESC LIMIT 1'),
        {"uid": user_id}
    ).fetchone()
    water_goal = water_data[0] if water_data else 0

    meal_plan_today = s.execute(
            text("""
                SELECT meal_plan, plan_type 
                FROM meal_plans 
                WHERE user_id = :uid AND CAST(timestamp AS DATE) = CURRENT_DATE 
                ORDER BY timestamp DESC LIMIT 2
            """), 
            {"uid": user_id}
        ).fetchone()

    progress_data = s.execute(
        text("SELECT timestamp, weight FROM user_progress WHERE user_id = :uid ORDER BY timestamp ASC"),
        {"uid": user_id}
    ).fetchall()

    weight_data = s.execute(
        text("SELECT weight FROM user_progress WHERE user_id = :uid ORDER BY timestamp DESC LIMIT 2"),
        {"uid": user_id}
    ).fetchall()
    
    start_weight = None
    goal_data = None

    goal_data_raw = s.execute(
        text("SELECT target_weight, goal_type, timestamp FROM goals WHERE user_id = :uid ORDER BY timestamp DESC LIMIT 1"),
        {"uid": user_id}
    ).fetchone()

    if goal_data_raw:
        target_weight, goal_type, goal_timestamp = goal_data_raw
        start_weight_raw = s.execute(
            text("SELECT weight FROM user_progress WHERE user_id = :uid AND timestamp <= :ts ORDER BY timestamp DESC LIMIT 1"), 
            {"uid": user_id, "ts": goal_timestamp}
        ).fetchone()
        
        if start_weight_raw:
            start_weight = start_weight_raw[0]
        else:
            start_weight_raw = s.execute(
                text("SELECT weight FROM user_progress WHERE user_id = :uid ORDER BY timestamp ASC LIMIT 1"), 
                {"uid": user_id}
            ).fetchone()
            if start_weight_raw:
                start_weight = start_weight_raw[0]
        
        if start_weight is not None:
            goal_data = (target_weight, goal_type, start_weight)

current_weight = 0
weight_delta = None
if weight_data:
    current_weight = weight_data[0][0]
    if len(weight_data) > 1:
        previous_weight = weight_data[1][0]
        delta = round(current_weight - previous_weight, 2)
        weight_delta = f"{delta:.2f} kg"

hour = datetime.now(ZoneInfo("Asia/Kolkata")).hour
greeting = "Welcome Back"
if hour < 12:
    greeting = ":material/sunny: Good Morning"
elif 12 <= hour < 18:
    greeting = ":material/partly_cloudy_day: Good Afternoon"
else:
    greeting = ":material/moon_stars: Good Evening"

st.title(f"{greeting}, {user_session[1].capitalize()}")
st.markdown("Here is your health snapshot for the day.")
st.divider()

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True, height=442):
        st.subheader(":material/analytics: Key Metrics")
        c1, c2 = st.columns(2)
        with c1:
            st.metric(label="Your Target Calories", value=f"{int(target_cals)} kcal")
            st.metric(label="Current Weight", value=f"{current_weight:.2f} kg", delta=weight_delta, delta_color="inverse")
            st.metric(label="Daily Water Intake", value=f"{water_goal:.2f} L")
        with c2:
            st.metric(label="Daily Protein Goal", value=f"{protein_goal:.2f} g")
            st.metric(label="Daily Carbs Goal", value=f"{carbs_goal:.2f} g")
            st.metric(label="Daily Fats Goal", value=f"{fats_goal:.2f} g")



with col2:
    with st.container(border=True, height=442):
        st.subheader(":material/monitor_weight: Your Weight Progress")
        if not progress_data:
            st.info("No weight data to show yet. Update your profile to start tracking!")
        else:
            df = pd.DataFrame(progress_data, columns=["Date", "Weight (kg)"])
            df["Date"] = pd.to_datetime(df["Date"])
            df["Day"] = df["Date"].dt.date
            df_plot = df.groupby("Date")["Weight (kg)"].last().reset_index()

            chart = alt.Chart(df_plot).mark_line(point=True, color="#85BF8A").encode(
                x=alt.X('Date', type='temporal', title='Date', axis=alt.Axis(format="%d-%b")),
                y=alt.Y('Weight (kg)', title='Weight (kg)'),

                tooltip=[alt.Tooltip('Date', format="%Y-%m-%d", title="Date"), 
                            alt.Tooltip('Date', format="%H:%M:%S", title="Time"), 'Weight (kg)']
            ).interactive()
            
            st.altair_chart(chart)

st.divider()

with st.container(border=True):
    st.subheader(":material/sprint: Progress to Your Goal")
    
    if not goal_data:
        st.info("You haven't set a goal weight yet! Go to 'Set Goal' to create one.")
        if st.button("Set Weight Goal"):
            st.switch_page("views/Set_goal.py")
    elif start_weight is None:
        st.info("Log your weight at least once (e.g., in 'Update Profile') to see your progress.")
    else:
        target_weight, goal_type, start_weight_for_goal = goal_data
        progress_percent = 0

        if goal_type == "loss":
            total_to_lose = start_weight_for_goal - target_weight
            current_lost = start_weight_for_goal - current_weight
            
            if total_to_lose <= 0: 
                progress_percent = 100 if current_lost >= 0 else 0
            else:
                progress_percent = int((current_lost / total_to_lose) * 100)
            
            st.write(f"**Goal:** Lose {total_to_lose:.2f} kg (from {start_weight_for_goal:.2f} kg to {target_weight:.2f} kg)")
            st.write(f"**Current:** You have lost {current_lost:.2f} kg so far.")

        elif goal_type == 'gain':
                total_to_gain = target_weight - start_weight_for_goal
                current_gained = current_weight - start_weight_for_goal
                
                if total_to_gain <= 0:
                    progress_percent = 100 if current_gained >= 0 else 0
                else:
                    progress_percent = int((current_gained / total_to_gain) * 100)
                
                st.write(f"**Goal:** Gain {total_to_gain:.2f} kg (from {start_weight_for_goal:.2f} kg to {target_weight:.2f} kg)")
                st.write(f"**Current:** You have gained {current_gained:.2f} kg so far.")

        if progress_percent < 0: progress_percent = 0
        if progress_percent > 100: progress_percent = 100
        
        st.progress(progress_percent / 100, text=f"{progress_percent}% Complete")

st.divider()

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True, height=228):
        st.subheader(":material/hand_meal: Today's Meal Plan")
        if meal_plan_today:
            plan_text, plan_type = meal_plan_today

            @st.dialog(f"Your {plan_type} Meal Plan", width="large")
            def show_meal_plan_dialog():
                st.markdown(plan_text)
            
            if st.button(f"View Your Latest Meal Plan", width="stretch"):
                show_meal_plan_dialog()

            if st.button("Go to History"):
                st.switch_page("views/History.py")
        else:
            st.info("You haven't generated a meal plan today.")
            if st.button("Generate Your Plan Now!"):
                st.switch_page("views/Meal_Planner.py")

with col2:
    with st.expander("Quick Log Today's Weight", expanded=True):
        with st.form("quick_log_form"):
            quick_weight = st.number_input("Enter today's weight (kg)", value=current_weight, min_value=10.0, max_value=300.0, step=0.1)
            submitted = st.form_submit_button("Log Weight")

            if submitted:
                success, message = log_weight(user, quick_weight)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

st.divider() 

with st.container():
    st.subheader(":material/self_improvement: Manage Your Health")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        if st.button("Update Health Profile", width='stretch'):
            st.switch_page("views/Profile_Update.py")
        if st.button("Set Weight Goal", width='stretch'):
            st.switch_page("views/Set_Goal.py")
            
    with c2:
        if st.button("Generate New Meal Plan", width='stretch'):
            st.switch_page("views/Meal_Planner.py")
        if st.button("View Meal History", width='stretch'):
            st.switch_page("views/History.py")

    with c3:
        if st.button("View Progress", width='stretch'):
            st.switch_page("views/Progress.py")
        if st.button("View Goal History", width='stretch'):
            st.switch_page("views/History.py")

    with c4:
        if st.button("View Calculations", width='stretch'):
            st.switch_page("views/Calculations.py")
        if st.button("Food Info", width='stretch'):
            st.switch_page("views/Food_Info.py")

render_footer()

