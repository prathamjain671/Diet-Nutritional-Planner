import streamlit as st
from utils.db import insert_calculations, insert_user, insert_meal_plan, insert_goal, insert_macros, insert_user_progress, create_table, create_connection
from utils.calculations import find_tdee, find_bmi, protein_intake, calculate_macros, water_intake
from streamlit_extras.switch_page_button import switch_page
from utils.user import User

st.set_page_config(page_title="Profile Setup", layout="centered")
st.title("Complete Your Profile")

if "new_username" not in st.session_state or "new_email" not in st.session_state:
    st.warning("Profile setup already completed!")
    st.stop()

with st.form("profile_form"):
    name = st.text_input("Your Name")
    age = st.number_input("Age", min_value=0, max_value=130, step=1)
    gender = st.selectbox("Gender", ["Male", "Female"])
    height = st.number_input("Height (cm)", min_value=0, max_value=300)
    weight = st.number_input("Weight (kg)", min_value=10, max_value=300)
    goal = st.selectbox("Your Goal", ["Weight Loss", "Weight Gain", "Muscle Gain", "Maintenance"])
    diet_preference = st.selectbox("Dietary Preference", ["Vegetarian", "Non-Vegetarian", "Eggitarian"])

    activity_options = {
            "Sedentary (Little or no exercise)" : "sedentary",
            "Lightly Active (1-3 days/week)" : "lightly active",
            "Moderately Active (4-5 days/week)" : "moderately active",
            "Active (6-7 days/week or intense exercise 3-4 times/week)" : "active",
            "Very Active (Intense exercise 6-7 times/week or physical job)" : "very active"
    }

    activity_display = st.selectbox(
        "Select your Activity Level: ",
        list(activity_options.keys())
    )
    activity_level = activity_options[activity_display]

    submitted = st.form_submit_button("Save Profile")

if submitted:
    user = User(name, age, gender.lower(), st.session_state.new_email, height, weight, goal.lower(), diet_preference.lower(), activity_level.lower())
    user_id = insert_user(user)
    user.id = user_id

    tdee = find_tdee(user)
    bmi, bmi_category = find_bmi(user)
    protein = protein_intake(user)
    macros = calculate_macros(user)
    water = water_intake(user)

    insert_calculations(user_id, tdee, bmi, bmi_category, water)
    insert_macros(user_id, protein, macros["Target Calories"], macros["Carbs (g)"], macros["Fats (g)"])
    insert_user_progress(user)

    st.session_state.user = (user.id, user.name, user.email)

    st.success("Profile Setup Complete!")
    st.switch_page("pages/Dashboard.py")
