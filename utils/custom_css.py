import streamlit as st

def load_css():

    APP_GRADIENT_START = "#2E3141"
    APP_GRADIENT_END = "#121212"
    SIDEBAR_BOX_BG = "#54555E"
    SIDEBAR_BOX_TITLE_COLOR = "#FFFFFF"
    
    SIDEBAR_ACTIVE_LINK_BG = "#F0F2F6" 
    SIDEBAR_ACTIVE_LINK_TEXT = "#31333F"
    
    custom_css = f"""
    <style>
    
    /* === APP BACKGROUND GRADIENT === */
    
    [data-testid="stAppViewContainer"] {{
        background-image: linear-gradient(
            to bottom right, 
            {APP_GRADIENT_START}, 
            {APP_GRADIENT_END}
        );
        color: white; /* Default text color on dark bg */
    }}
    
    [data-testid="stMain"], [data-testid="stSidebar"] {{
        background-color: transparent;
    }}
    
    /* === SIDEBAR INFO BOX === */
    
    .colored-container {{
        background-color: {SIDEBAR_BOX_BG}; 
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 9px; 
    }}
    
    .colored-container h3 {{
        color: {SIDEBAR_BOX_TITLE_COLOR}; 
        font-family: 'Times New Roman', Times, serif;
        font-size: 16px; 
        font-weight: bold;
        margin: 0;
        padding: 0;
        text-align: center; /* Centered title */
    }}

    /* === SIDEBAR ACTIVE PAGE HIGHLIGHT === */
    /* This styles the link for the page you are on */
    
    [data-testid="stSidebarNav"] a[aria-selected="true"] {{
        background-color: {SIDEBAR_ACTIVE_LINK_BG}; 
        color: {SIDEBAR_ACTIVE_LINK_TEXT}; 
        border-radius: 8px; 
        font-weight: 600;
    }}
    [data-testid="stSidebarNav"] a[aria-selected="true"] .st-emotion-cache-1rqb3w6 {{
        color: {SIDEBAR_ACTIVE_LINK_TEXT};
    }}
    
    </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)