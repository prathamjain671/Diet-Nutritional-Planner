import streamlit as st
from utils.db import insert_meal_plan, create_connection
from utils.calculations import find_tdee, protein_intake
from utils.meal_prompt import base_prompt
from google import genai
from markdown import markdown
from bs4 import BeautifulSoup
from utils.user import User

client = genai.Client(api_key='')

user = st.session_state.get("user")
if not user:
    st.error("Please Login first to view this page!")
    st.stop()

conn = create_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM users WHERE id = ?", (user[0],))
row = cursor.fetchone()
conn.close()
if not row:
    st.error("User profile not found!")
    st.stop()

user = User(*row[1:])
user.id = row[0]

st.title("Meal Planner")
st.markdown(f"Hello, {user.name}! Lets get your personalized meal plan.")

plan_type = st.radio("Select meal plan type:", ["Daily", "Weekly"] )
custom_note = st.text_area("Add any specific cooking instructions (optional): ")

target_calories = find_tdee(user)
protein_goal = protein_intake(user)

prompt = base_prompt(plan_type, user, target_calories, protein_goal, custom_note)

if st.button("Generate Meal Plan"):
    st.info("Generating your customized meal plan...")

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',contents=prompt
    )

    text_response = markdown(response.text)
    meal_plan = ''.join(BeautifulSoup(text_response,'html.parser').find_all(string=True))

    insert_meal_plan(user.id, plan_type, custom_note, prompt, meal_plan)

    st.success("Here is your meal plan:")
    st.text_area("Meal Plan", meal_plan, height=600)

    