import streamlit as st
from utils.db import create_connection
from utils.user import User
from utils.calculations import find_tdee, find_bmi
from utils.custom_css import load_css
from utils.ui_helper import render_sidebar_info, render_footer
from sqlalchemy import text

load_css()
render_sidebar_info(
    icon_path="icons/calculate.png",
    title="Calculations",
    text_lines=["View a snapshot of your latest calculated health metrics, macro breakdown and try the 'What-If' calculator."]
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
        st.error("User profile not found! Please complete profile setup.")
        st.stop()

    user_id = user_row[0]
    saved_user = User(*user_row[1:])
    saved_user.id = user_id

    calc = s.execute(
        text('''
            SELECT tdee, bmi, bmi_category, water_intake, timestamp
            FROM calculations
            WHERE user_id = :uid
            ORDER BY timestamp DESC
            LIMIT 1
        '''), {"uid": user_id}
    ).fetchone()

    macro = s.execute(
        text('''
            SELECT protein, target_calories, carbs, fats, timestamp
            FROM macros
            WHERE user_id = :uid
            ORDER BY timestamp DESC
            LIMIT 1
        '''), {"uid": user_id}
    ).fetchone()

st.title(":material/camera: Your Latest Health Snapshot")
st.markdown("---")

with st.container(border=True):
    if calc:
        tdee, bmi, bmi_category, water_intake, timestamp = calc
        st.subheader("Calorie & Health Info")
        st.markdown(f"- **TDEE (Total Daily Energy Expenditure)**: {int(tdee)}kcal/day",
                    help="**TDEE**: Total Daily Energy Expenditure. The calories you burn per day. To lose weight, you must eat less than this.")
        
        st.markdown(f"- **BMI**: {round(bmi, 2)} {bmi_category.title()}", 
                    help="**BMI**: Body Mass Index. A measure of body fat based on height and weight.")
        
        st.markdown(f"- **Water Intake Goal**: {round(water_intake, 2)}L/day", 
                    help="**Water Intake Goal**: Your daily water intake goal, calculated based on your body weight.")
    else:
        st.warning("No records found!")

    if macro:
        protein, target_calories, carbs, fats, timestamp = macro
        st.subheader("Macronutrient Breakdown")
        st.markdown(f"- **Target Calories**: `{int(target_calories)} kcal/day`")
        st.markdown(f"- **Protein**: `{round(protein, 2)} g`")
        st.markdown(f"- **Carbohydrates**: `{round(carbs, 2)} g`")
        st.markdown(f"- **Fats**: `{round(fats, 2)} g`")
    else:
        st.warning("No macro data found.")


with st.container(border=True):

    st.subheader("What-If Calculator")
    st.markdown("See how your metrics would change. **This will not be saved to your profile.**")

    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True, height=315):
            st.markdown("##### Adjust Your Stats:")
            what_if_age = st.slider(
                "What if my age was...", 
                13, 100, saved_user.age
            )
            what_if_weight = st.slider(
                "What if my weight was...", 
                10.0, 300.0, saved_user.weight, 0.5
            )
            
            activity_options = {
                "Sedentary (Little or no exercise)" : "sedentary",
                "Lightly Active (1-3 days/week)" : "lightly active",
                "Moderately Active (4-5 days/week)" : "moderately active",
                "Active (6-7 days/week or intense exercise 3-4 times/week)" : "active",
                "Very Active (Intense exercise 6-7 times/week or physical job)" : "very active"
            }
            
            activity_keys = list(activity_options.keys())
            default_activity_index = 0
            try:
                default_activity_value = saved_user.activity_level
                default_activity_key = [k for k, v in activity_options.items() if v == default_activity_value][0]
                default_activity_index = activity_keys.index(default_activity_key)
            except Exception:
                pass
            
            what_if_activity_display = st.selectbox(
                "What if my activity level was...",
                activity_keys,
                index=default_activity_index
            )
            what_if_activity = activity_options[what_if_activity_display]

    with col2:
        with st.container(border=True, height=315):
            what_if_user = User(
                name=saved_user.name,
                age=what_if_age,
                gender=saved_user.gender,
                email=saved_user.email,
                height=saved_user.height,
                weight=what_if_weight,
                goal=saved_user.goal,
                diet_preference=saved_user.diet_preference,
                activity_level=what_if_activity
            )
            
            what_if_tdee = find_tdee(what_if_user)
            what_if_bmi, what_if_bmi_category = find_bmi(what_if_user)
            
            st.markdown("##### Your New Calculated Metrics:")
            st.metric(
                label="Your 'What-If' TDEE", 
                value=f"{int(what_if_tdee)} kcal/day",
                delta=f"{int(what_if_tdee - (calc[0] if calc else 0))} kcal vs. current"
            )
            st.metric(
                label="Your 'What-If' BMI", 
                value=f"{round(what_if_bmi, 2)} ({what_if_bmi_category.title()})",
                delta=f"{round(what_if_bmi - (calc[1] if calc else 0), 2)} vs. current"
            )

render_footer()