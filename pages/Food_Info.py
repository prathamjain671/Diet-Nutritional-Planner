import streamlit as st
import json

def load_food_data():
    with open('data/indian_food.json', "r") as file:
        return json.load(file)
    

food_data = load_food_data()

st.title("Indian Food Nutrition Info")
st.write("Select a food to view its nutritional info")

food_names = [item["item"] for item in food_data]
selected_food = st.selectbox("Choose a food item:", food_names)

food = next((item for item in food_data if item["item"] == selected_food), None)
if food:
    st.subheader(f"Nutrition for: {food['item'].capitalize()}")
    st.write(f"Calories: {food['calories']}")
    st.write(f"Protein: {food['protein']}")
    st.write(f"Carbs: {food['carbs']}")
    st.write(f"Fats: {food['fat']}")
    st.write(f"Portion: {food['portion']}")