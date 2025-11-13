import streamlit as st
from utils.db import create_connection
import pandas as pd
from datetime import datetime
from utils.calculations import log_weight
from utils.user import User
import altair as alt

st.set_page_config(page_title="Dashboard", layout="wide")

st.markdown(
    """
    <style>
    .colored-container {
        background-color: #74746E; 
        padding: 10px; /* Made padding a bit smaller */
        border-radius: 10px;
        margin-bottom: 9px; /* Space between box and text */
    }
    
    /* This styles the "Dashboard" title */
    .colored-container h3 {
        color: #FFFFFF; /* White color */
        font-family: 'Times New Roman', Times, serif; /* Serif font */
        font-weight: bold;
        margin: 0; /* Remove default margins */
        padding: 0;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. Build the HTML string with ONLY the title
title_box_html = """
<div class="colored-container">
    <h3>Dashboard</h3>
</div>
"""

# 3. Put everything in the sidebar
with st.sidebar.container(border=True):
    with st.container():
        # Render the title box
        st.markdown(title_box_html, unsafe_allow_html=True)
        
        # Now, render the text *outside* the box
        st.text("Welcome to your dashboard! ")
        st.text("Here you can view you key metrics, log your weight, navigate to other features and so much more!")

user_session = st.session_state.get("user")
if not user_session:
    st.error("Please log in first!")
    st.stop()

conn = create_connection()
cursor = conn.cursor()
user_email = user_session[0]
cursor.execute("SELECT * FROM users WHERE email = ?", (user_email,))
user_row = cursor.fetchone()

if not user_row:
    st.error("User profile not found! Please complete your profile.")
    conn.close()
    st.stop()

user_id = user_row[0]
user = User(*user_row[1:])
user.id = user_id

cursor.execute("SELECT target_calories FROM macros WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1", (user_id,))
macro_data = cursor.fetchone()
target_cals = macro_data[0] if macro_data else 0

cursor.execute("SELECT protein, carbs, fats FROM macros WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1", (user_id,))
macro_data = cursor.fetchone()
protein_goal = macro_data[0] if macro_data else 0
carbs_goal = macro_data[1] if macro_data else 0
fats_goal = macro_data[2] if macro_data else 0

cursor.execute('SELECT water_intake FROM calculations WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1', (user_id,))
water_data = cursor.fetchone()
water_goal = water_data[0]

cursor.execute("SELECT weight FROM user_progress WHERE user_id = ? ORDER BY timestamp DESC LIMIT 2", (user_id,))
weight_data = cursor.fetchall()

current_weight = 0
weight_delta = None
if weight_data:
    current_weight = weight_data[0][0]
    if len(weight_data) > 1:
        previous_weight = weight_data[1][0]
        delta = round(current_weight - previous_weight, 2)
        weight_delta = f"{delta:.2f} kg"

cursor.execute("SELECT meal_plan, plan_type FROM meal_plans WHERE user_id = ? AND DATE(timestamp) = DATE('now', 'localtime') ORDER BY timestamp DESC LIMIT 1", (user_id,))
meal_plan_today = cursor.fetchone()

cursor.execute("SELECT timestamp, weight FROM user_progress WHERE user_id = ? ORDER BY timestamp ASC", (user_id,))
progress_data = cursor.fetchall()

cursor.execute("SELECT target_weight, goal_type FROM goals WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1", (user_id,))
goal_data = cursor.fetchone()

cursor.execute("SELECT weight FROM user_progress WHERE user_id = ? ORDER BY timestamp ASC LIMIT 1", (user_id,))
start_weight_data = cursor.fetchone()
conn.close()

hour = datetime.now().hour
greeting = "Welcome Back"
if hour < 12:
    greeting = "Good Morning"
elif 12 <= hour < 18:
    greeting = "Good Afternoon"
else:
    greeting = "Good Evening"

st.title(f"{greeting}, {user_session[1]}!")
st.markdown("Here is your health snapshot for the day.")
st.divider()

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True, height=442):
        st.subheader("💡Key Metrics")
        c1, c2 = st.columns(2)
        with c1:
            st.metric(label="Your Target Calories", value=f"{target_cals:.2f} kcal")
            st.metric(label="Current Weight", value=f"{current_weight:.2f} kg", delta=weight_delta, delta_color="inverse")
            st.metric(label="Daily Water Intake", value=f"{water_goal:.2f} L")
        with c2:
            st.metric(label="Daily Protein Goal", value=f"{protein_goal:.2f} g")
            st.metric(label="Daily Carbs Goal", value=f"{carbs_goal:.2f} g")
            st.metric(label="Daily Fats Goal", value=f"{fats_goal:.2f} g")



with col2:
    with st.container(border=True, height=442):
        st.subheader("⚖️Your Weight Progress")
        if not progress_data:
            st.info("No weight data to show yet. Update your profile to start tracking!")
        else:
            df = pd.DataFrame(progress_data, columns=["Date", "Weight (kg)"])
            df["Date"] = pd.to_datetime(df["Date"])
            df["Day"] = df["Date"].dt.date
            df_plot = df.groupby("Date")["Weight (kg)"].last().reset_index()

            chart = alt.Chart(df_plot).mark_line(point=True).encode(
                x=alt.X('Date', type='temporal', title='Date', axis=alt.Axis(format="%d-%b")),
                y=alt.Y('Weight (kg)', title='Weight (kg)'),

                tooltip=[alt.Tooltip('Date', format="%Y-%m-%d", title="Date"), 
                            alt.Tooltip('Date', format="%H:%M:%S", title="Time"), 'Weight (kg)']
            ).interactive()

            st.altair_chart(chart, use_container_width=True)

st.divider()

with st.container(border=True):
    st.subheader("🏃🏻Progress to Your Goal")
    
    if not goal_data:
        st.info("You haven't set a goal weight yet! Go to 'Set Weight Goal' to create one.")
    elif not start_weight_data:
        st.info("Log your weight at least once (e.g., in 'Update Profile') to see your progress.")
    else:
        target_weight, goal_type = goal_data
        start_weight = start_weight_data[0]
        progress_percent = 0

        if goal_type == "loss":
            total_to_lose = start_weight - target_weight
            current_lost = start_weight - current_weight
            
            if total_to_lose <= 0: 
                progress_percent = 100 if current_lost >= 0 else 0
            else:
                progress_percent = int((current_lost / total_to_lose) * 100)
            
            st.write(f"**Goal:** Lose {total_to_lose:.1f} kg (from {start_weight} kg to {target_weight} kg)")
            st.write(f"**Current:** You have lost {current_lost:.1f} kg so far.")

        elif goal_type == 'gain':
                total_to_gain = target_weight - start_weight
                current_gained = current_weight - start_weight
                
                if total_to_gain <= 0:
                    progress_percent = 100 if current_gained >= 0 else 0
                else:
                    progress_percent = int((current_gained / total_to_gain) * 100)
                
                st.write(f"**Goal:** Gain {total_to_gain:.1f} kg (from {start_weight} kg to {target_weight} kg)")
                st.write(f"**Current:** You have gained {current_gained:.1f} kg so far.")

        if progress_percent < 0: progress_percent = 0
        if progress_percent > 100: progress_percent = 100
        
        st.progress(progress_percent / 100, text=f"{progress_percent}% Complete")

st.divider()

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True, height=228):
        st.subheader("🍽️Today's Meal Plan")
        if meal_plan_today:
            plan_text, plan_type = meal_plan_today
            with st.expander(f"View Your {plan_type} Plan"):
                st.markdown(plan_text)
        else:
            st.info("You haven't generated a meal plan today.")
            if st.button("Generate Your Plan Now!"):
                st.switch_page("pages/Meal_Planner.py")

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
    st.subheader("Manage Your Health")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        if st.button("Update Profile", use_container_width=True):
            st.switch_page("pages/Profile_Update.py")
        if st.button("Set Weight Goal", use_container_width=True):
            st.switch_page("pages/Set_Goal.py")
            
    with c2:
        if st.button("Generate New Meal Plan", use_container_width=True):
            st.switch_page("pages/Meal_Planner.py")
        if st.button("View Meal History", use_container_width=True):
            st.switch_page("pages/Meal_History.py")

    with c3:
        if st.button("View Progress", use_container_width=True):
            st.switch_page("pages/Progress.py")
        if st.button("View Goal History", use_container_width=True):
            st.switch_page("pages/Goal_History.py")

    with c4:
        if st.button("View Calculations", use_container_width=True):
            st.switch_page("pages/Calculations.py")
        if st.button("Indian Food Info", use_container_width=True):
            st.switch_page("pages/Food_Info.py")



