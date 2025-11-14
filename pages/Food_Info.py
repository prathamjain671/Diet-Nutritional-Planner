import streamlit as st
import json
from utils.custom_css import load_css
from utils.ui_helper import render_sidebar_info

st.set_page_config(page_title="Food Info", layout="wide")
load_css()

render_sidebar_info(
    title="Food Info",
    text_lines=["A simple lookup tool for the calories and macros of common food items."]
)

def load_food_data():
    with open('data/food_db.json', "r") as file:
        return json.load(file)
    

food_data = load_food_data()

food_name_map = {item["item"].capitalize(): item["item"] for item in food_data}
food_names_display = list(food_name_map.keys())

st.title("Food Nutrition Info")
st.write("Search for a food item or select from the list below to view its nutritional info")

selected_food_display = st.selectbox("Type or choose a food item:", food_names_display)
original_food_name = food_name_map[selected_food_display]

food = next((item for item in food_data if item["item"] == original_food_name), None)

if food:
    st.subheader(f"Nutrition for: {food['item'].capitalize()}")
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Calories", f"{food['calories']} kcal")
            st.metric("Protein", f"{food['protein']} g")
        with col2:
            st.metric("Carbs", f"{food['carbs']} g")
            st.metric("Fats", f"{food['fat']} g")
        st.caption(f"Portion: {food['portion']}")