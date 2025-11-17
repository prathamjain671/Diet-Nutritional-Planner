import streamlit as st
import pandas as pd
from utils.custom_css import load_css
from utils.ui_helper import render_sidebar_info

load_css()
render_sidebar_info(
    icon_path="icons/search.png",
    title="Food Info",
    text_lines=["A simple lookup tool for the calories and macros of common food items."]
)

@st.cache_data
def load_food_data():
    df = pd.read_csv("data/food_db.csv")
    return df
    

food_data_df = load_food_data()

food_name_map = dict(zip(food_data_df['item'].str.capitalize(), food_data_df['item']))
food_names_display = sorted(list(food_name_map.keys()), key=str.casefold)

st.title(":material/dining: Food Nutrition Info", 
         help="Please note: The nutritional data may not be 100% accurate. Always double-check with a reliable source.")
st.write("Search for a food item or select from the list below to view its nutritional info")

selected_food_display = st.selectbox("Type or choose a food item:", food_names_display)
original_food_name = food_name_map[selected_food_display]

if selected_food_display:
    original_food_name = food_name_map[selected_food_display]
    food_series = food_data_df[food_data_df['item'] == original_food_name].iloc[0]

    if not food_series.empty:
        st.subheader(f"Nutrition for: {food_series['item'].capitalize()}")
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Calories", f"{food_series['calories']} kcal")
                st.metric("Protein", f"{food_series['protein']} g")
            with col2:
                st.metric("Carbs", f"{food_series['carbs']} g")
                st.metric("Fats", f"{food_series['fat']} g")
            st.caption(f"Portion: {food_series['portion']}")
else:
    st.info("No food item selected.")