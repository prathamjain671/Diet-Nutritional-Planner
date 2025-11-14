import streamlit as st

def render_sidebar_info(title, text_lines):
    title_box_html = f"""
    <div class="colored-container">
        <h3>{title}</h3>
    </div>
    """

    with st.sidebar.container(border=True):
        st.markdown(title_box_html, unsafe_allow_html=True)
        
        for line in text_lines:
            st.text(line)

def render_sidebar_footer():
    st.sidebar.divider()
    st.sidebar.markdown(
        """
        **Built by Pratham**
        [GitHub](https://github.com/prathamjain671) | [LinkedIn](www.linkedin.com/in/prathamjain671)
        """
    )