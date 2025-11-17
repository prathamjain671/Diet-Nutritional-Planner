import streamlit as st

def load_css():

    SIDEBAR_INFO_OUTER_BG = "#232D27"     # Outer background
    SIDEBAR_INFO_OUTER_TEXT = "#E5E6E6"   # Outer text
    SIDEBAR_INFO_INNER_BG = "#4A544C"     # Inner background
    SIDEBAR_INFO_INNER_TEXT = "#E5E6E6"   # Inner text
    SIDEBAR_INFO_OUTER_BORDER = "#95bc9aff" # Outer border
    
    custom_css = f"""
    <style>
    
    /* This is the OUTER box */
    .info-box-outer {{
        background-color: {SIDEBAR_INFO_OUTER_BG};
        border-radius: 10px;
        padding: 15px;
        border: 1px solid {SIDEBAR_INFO_OUTER_BORDER};
    }}
    
    /* This is the INNER box */
    .info-box-inner {{
        background-color: {SIDEBAR_INFO_INNER_BG};
        color: {SIDEBAR_INFO_INNER_TEXT};
        padding: 5px 5px;
        border-radius: 8px;
        margin-bottom: 15px;
        
        /* For the icon and text */
        font-family: "Inter", sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    
    /* This is the text below the inner box */
    .info-box-text {{
        color: {SIDEBAR_INFO_OUTER_TEXT};
        font-family: "Inter", sans-serif;
        line-height: 1.6;
        font-size: 14px;
    }}
    
    </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)