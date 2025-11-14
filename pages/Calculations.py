import streamlit as st
import sqlite3
from utils.db import create_connection
from utils.custom_css import load_css
from utils.ui_helper import render_sidebar_info

st.set_page_config(page_title="Calculations", layout="wide")
load_css()

render_sidebar_info(
    title="Calculations",
    text_lines=["View a snapshot of your latest calculated health metrics and macro breakdown."]
)

user_session = st.session_state.get("user")
if not user_session:
    st.error("Please Login to access this page!")
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
        SELECT tdee, bmi, bmi_category, water_intake, timestamp
        FROM calculations
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
''', (user_id,))
calc = cursor.fetchone()

cursor.execute('''
        SELECT protein, target_calories, carbs, fats, timestamp
        FROM macros
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
''', (user_id,))
macro = cursor.fetchone()

conn.close()

st.title("Your Latest Health Snapshot")
st.markdown("---")

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