import streamlit as st
from utils.db import create_connection, insert_user_progress, insert_calculations, insert_macros
from utils.calculations import find_tdee, find_bmi, water_intake, calculate_macros, protein_intake
from utils.user import User

user_session = st.session_state.get("user")
if not user_session:
    st.error("Please login to view this page!")
    st.stop()

st.title("Update Your Profile")

conn = create_connection()  
cursor = conn.cursor()

user_email = user_session[0]

cursor.execute("SELECT * FROM users WHERE email = ?", (user_email,))
data = cursor.fetchone()
conn.close()

if not data:
    st.error("No user data found!")
    st.stop()

temp_user = User(*data[1:])
temp_user.id = data[0]

st.subheader("Update any information")
temp_user.height = st.number_input("Height (cm)", value=temp_user.height)
temp_user.weight = st.number_input("Weight (kg)", value=temp_user.weight)
temp_user.age = st.number_input("Age", value=temp_user.age)

goal_options = ["Weight Loss", "Weight Gain", "Muscle Gain", "Maintenance"]
goal_display = temp_user.goal.title()
temp_user.goal = st.selectbox("Goal",goal_options, index=goal_options.index(goal_display)).lower()

diet_options = ["Vegetarian", "Non-Vegetarian", "Eggitarian"]
diet_display = temp_user.diet_preference.title()
temp_user.diet_preference = st.selectbox("Diet Preference", diet_options, index=diet_options.index(diet_display))

activity_options = {
            "Sedentary (Little or no exercise)" : "sedentary",
            "Lightly Active (1-3 days/week)" : "lightly active",
            "Moderately Active (4-5 days/week)" : "moderately active",
            "Active (6-7 days/week or intense exercise 3-4 times/week)" : "active",
            "Very Active (Intense exercise 6-7 times/week or physical job)" : "very active"
    }

activity_display = st.selectbox(
    "Activity Level: ",
    list(activity_options.keys())
)
temp_user.activity_level = activity_options[activity_display]

if st.button("Update Profile"):
    insert_user_progress(temp_user)

    tdee = find_tdee(temp_user)
    bmi, bmi_category = find_bmi(temp_user)
    protein = protein_intake(temp_user)
    water = water_intake(temp_user)
    macros = calculate_macros(temp_user)

    insert_calculations(temp_user.id, tdee, bmi, bmi_category, water)
    insert_macros(temp_user.id, protein, macros["Target Calories"], macros["Carbs (g)"], macros["Fats (g)"])

    st.success("Profile Updated Successfully!")
    
    