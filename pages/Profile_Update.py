import streamlit as st
from utils.db import create_connection, insert_user_progress, insert_calculations, insert_macros, update_user, insert_user
from utils.calculations import find_tdee, find_bmi, water_intake, calculate_macros, protein_intake
from utils.user import User
from utils.custom_css import load_css
from utils.ui_helper import render_sidebar_info
import time

st.set_page_config(page_title="Profile Update", layout="wide")
load_css()

render_sidebar_info(
    title="Profile Update",
    text_lines=["Manage your health data like weight, height, activity level, and dietary preferences."]
)

user_session = st.session_state.get("user")
if not user_session:
    st.error("Please login to view this page!")
    st.stop()

user_email = user_session[0]
user_name_from_auth = user_session[1]

conn = create_connection()  
cursor = conn.cursor()
cursor.execute("SELECT * FROM users WHERE email = ?", (user_email,))
data = cursor.fetchone()
conn.close()

if data:
    st.title("Update Your Profile")

    temp_user = User(*data[1:])
    temp_user.id = data[0]

    default_name = temp_user.name
    default_age = temp_user.age
    default_gender = temp_user.gender.title()
    default_height = temp_user.height
    default_weight = temp_user.weight
    default_goal = temp_user.goal.title()
    default_diet = temp_user.diet_preference.title()

    gender_options = ["Male", "Female"]
    goal_options = ["Weight Loss", "Weight Gain", "Muscle Gain", "Maintenance"]
    diet_options = ["Vegetarian", "Non-Vegetarian", "Eggitarian"]

    default_gender_index = gender_options.index(default_gender)
    default_goal_index = goal_options.index(default_goal)
    default_diet_index = diet_options.index(default_diet)

    is_new_user = False

else:
    st.title("Complete Your Profile")

    st.markdown("<style>[data-testid='stSidebar'] { display: none; }</style>", unsafe_allow_html=True)

    temp_user = User(name=user_name_from_auth, email=user_email, age=0, gender="", height=0, weight=0, goal="", diet_preference="", activity_level="")

    default_name = user_name_from_auth
    default_age = 18
    default_gender_index = 0
    default_height = 10.0
    default_weight = 10.0
    default_goal_index = 0
    default_diet_index = 0

    gender_options = ["Male", "Female"]
    goal_options = ["Weight Loss", "Weight Gain", "Muscle Gain", "Maintenance"]
    diet_options = ["Vegetarian", "Non-Vegetarian", "Eggitarian"]
    
    is_new_user = True


with st.form("Profile_Form"):
    with st.container(border=True):
        st.subheader("Your Details")
        name = st.text_input("Name", value=default_name)
        age = st.number_input("Age", value=default_age, min_value=5, max_value=130)
        gender = st.selectbox("Gender", gender_options, index=default_gender_index)
    with st.container(border=True):
        st.subheader("Health Metrics")
        height = st.number_input("Height (cm)", value=default_height, min_value=10.0, max_value=300.0)
        weight = st.number_input("Weight (kg)", value=default_weight, min_value=10.0, max_value=300.0)
    with st.container(border=True):
        st.subheader("Your Goals")
        goal = st.selectbox("Your Goal", goal_options, index=default_goal_index)
        diet_preference = st.selectbox("Dietary Preference", diet_options, index=default_diet_index)

        activity_options_dict = {
            "Sedentary (Little or no exercise)": "sedentary",
            "Lightly Active (1-3 days/week)": "lightly active",
            "Moderately Active (4-5 days/week)": "moderately active",
            "Active (6-7 days/week or intense exercise 3-4 times/week)": "active",
            "Very Active (Intense exercise 6-7 times/week or physical job)": "very active"
        }

        activity_keys = list(activity_options_dict.keys())
        default_activity_index = 0
        if not is_new_user:
            try:
                default_activity_value = temp_user.activity_level
                default_activity_key = [k for k, v in activity_options_dict.items() if v == default_activity_value][0]
                default_activity_index = activity_keys.index(default_activity_key)
            except Exception:
                default_activity_index = 0 

        activity_display = st.selectbox(
            "Select your Activity Level: ",
            activity_keys,
            index=default_activity_index
        )
        activity_level = activity_options_dict[activity_display]

    submitted = st.form_submit_button("Save Profile")

if submitted:

    temp_user.name = name
    temp_user.age = age
    temp_user.gender = gender.lower()
    temp_user.height = height
    temp_user.weight = weight
    temp_user.goal = goal.lower()
    temp_user.diet_preference = diet_preference.lower()
    temp_user.activity_level = activity_level.lower()

    if is_new_user:
        user_id = insert_user(temp_user)
        temp_user.id = user_id
        st.session_state.user = (temp_user.email, temp_user.name)
    else:
        update_user(temp_user)
        st.session_state.user = (temp_user.email, temp_user.name)

    tdee = find_tdee(temp_user)
    bmi, bmi_category = find_bmi(temp_user)
    protein = protein_intake(temp_user)
    water = water_intake(temp_user)
    macros = calculate_macros(temp_user)

    insert_calculations(temp_user.id, tdee, bmi, bmi_category, water)
    insert_macros(temp_user.id, protein, macros["Target Calories"], macros["Carbs (g)"], macros["Fats (g)"])
    insert_user_progress(temp_user)

    if is_new_user:
        st.success("Profile Setup Complete! Redirecting to Dashboard...")
        st.switch_page("pages/Dashboard.py")
    else:
        st.success("Profile Updated Successfully!")
        time.sleep(1)
        st.rerun()
    
    