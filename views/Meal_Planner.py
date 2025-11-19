import streamlit as st
from utils.db import insert_meal_plan, create_connection
from utils.calculations import find_tdee, protein_intake
from utils.meal_prompt import base_prompt
import google.generativeai as genai
from utils.user import User
from openai import OpenAI
from utils.custom_css import load_css
from utils.ui_helper import render_sidebar_info, render_footer
from sqlalchemy import text

load_css()
render_sidebar_info(
    icon_path="icons/menu_book_2.png",
    title="Meal Planner",
    text_lines=["Generate a new, personalized meal plan tailored to your goals."]
)

user_session = st.session_state.get("user")

if "provider" not in st.session_state:
    st.session_state.provider = "Google Gemini"
if "google_api_key" not in st.session_state:
    st.session_state.google_api_key = ""
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""

st.subheader("1. Choose Your AI Provider")
provider = st.selectbox("Provider:", ["Google Gemini", "OpenAI ChatGPT"], key="provider")

st.subheader("2. Enter your API Key")
api_key_input = ""


if st.session_state.provider == "Google Gemini":
    api_key_input = st.text_input("Google AI API Key:", type="password", value=st.session_state.google_api_key, placeholder="Just Relax! We do not store your key.", 
                                  help="Get your key from Google AI Studio. We do not store your API key. It is only used for your current session and is discarded when you close the browser tab or logout.")
    
    if api_key_input != st.session_state.google_api_key:
        st.session_state.google_api_key = api_key_input
        st.rerun()

elif st.session_state.provider == "OpenAI ChatGPT":
    api_key_input = st.text_input("OpenAI API Key:", type="password", value=st.session_state.openai_api_key, placeholder="Just Relax! We do not store your key.", 
                                  help="Get your API key from OpenAI Dev Studio. We do not store your API key. It is only used for your current session and is discarded when you close the browser tab or logout.")

    if api_key_input != st.session_state.openai_api_key:
        st.session_state.openai_api_key = api_key_input
        st.rerun()


user_session = st.session_state.get("user")
if not user_session:
    st.error("Please Login first to view this page!")
    st.stop()


conn = create_connection()
with conn.session as s:
    row = s.execute(
        text("SELECT * FROM users WHERE email = :email"), 
        {"email": user_session[0]}
    ).fetchone()

if not row:
    st.error("User profile not found!")
    st.stop()   

user_obj = User(*row[1:])
user_obj.id = row[0]

goal_row = s.execute(
        text("SELECT target_calories FROM goals WHERE user_id = :uid ORDER BY timestamp DESC LIMIT 1"),
        {"uid": user_obj.id}
    ).fetchone()

if goal_row and goal_row[0]:
        target_calories = goal_row[0]
else:
    target_calories = find_tdee(user_obj)

st.title("Meal Planner")

client = None
if st.session_state.provider == "Google Gemini":
    if st.session_state.google_api_key:
        try:
            client = genai.Client(api_key = st.session_state.google_api_key)
            client.list_models()
            st.success("Google Gemini API Key is valid!")
        except Exception as e:
            st.error(f"Invalid Google API Key")
            client = None
    else:
        st.warning("Please enter your Google AI API Key to use Gemini!")

if st.session_state.provider == "OpenAI ChatGPT":
    if st.session_state.openai_api_key:
        try:
            client = OpenAI(api_key = st.session_state.openai_api_key)
            client.models.list()
            st.success("OpenAI API Key is valid!")
        except Exception as e:
            st.error(f"Invalid OpenAI API Key")
            client = None
    else:
        st.warning("Please enter your OpenAI API Key to use ChatGPT!")

if client:
    st.subheader("3. Generate Your Plan")
    st.markdown(f"Hello, {user_obj.name}! Lets get your personalized meal plan.")
    st.info(f"Generating plan for target: **{int(target_calories)} kcal** (based on your goal)")

    plan_type = st.radio("Select meal plan type:", ["Daily", "Weekly"] )
    custom_note = st.text_area("Add any specific cooking instructions (optional): ")

    protein_goal = protein_intake(user_obj)

    prompt = base_prompt(plan_type, user_obj, target_calories, protein_goal, custom_note)

    if st.button("Generate Meal Plan"):
        with st.spinner(f"Generating your customized meal plan with {st.session_state.provider}..."):

            try:
                meal_plan_markdown = ""

                if st.session_state.provider == "Google Gemini":
                    response = client.models.generate_content(
                        model='gemini-2.0-flash-001',contents=prompt
                    )
                    meal_plan_markdown = response.text

                elif st.session_state.provider == "OpenAI ChatGPT":
                    response = client.chat.completions.create(
                        model="gpt-5.1",
                        messages=[
                            {"role": "system", "content": "You are a helpful nutritional planner."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    meal_plan_markdown = response.choices[0].message.content

                insert_meal_plan(user_obj.id, plan_type, custom_note, prompt, meal_plan_markdown) 

            except Exception as e:
                st.error(f"An error occurred while generating the plan: {e}")
                meal_plan_markdown = None

        if meal_plan_markdown:
            st.success("Here is your meal plan:")
            with st.container(border=True):
                st.markdown(meal_plan_markdown)

render_footer()


        

    