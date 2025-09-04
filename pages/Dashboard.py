import streamlit as st

st.set_page_config(page_title="Dashboard", layout="centered")

user = st.session_state.get("user")

if not user:
    st.error("Please log in first!")
    st.stop()

st.title("Welcome to your Dashboard")
st.markdown(f"Hello, {user[1]}")

col1, col2 = st.columns(2)

with col1:
    if st.button("View Calculations"):
        st.switch_page("pages/Calculations.py")
    if st.button("Update Profile"):
        st.switch_page("pages/Profile_Update.py")
    if st.button("View Progress"):
        st.switch_page("pages/Progress.py")
    if st.button("Set Weight Goal"):
        st.switch_page("pages/Set_Goal.py")

with col2:
    if st.button("Generate your Customized Meal Plan"):
        st.switch_page("pages/Meal_Planner.py")
    if st.button("View Meal History"):
        st.switch_page("pages/Meal_History.py")
    if st.button("Indian Food Info"):
        st.switch_page("pages/Food_Info.py")
    if st.button("View Goal History"):
        st.switch_page("pages/Goal_History.py")



