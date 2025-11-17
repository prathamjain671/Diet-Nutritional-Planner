import streamlit as st
import base64
import pathlib

def image_to_base64(file_path: str):
    try:
        with open(file_path, "rb") as f:
            img_bytes = f.read()
        base64_str = base64.b64encode(img_bytes).decode("utf-8")
        
        file_extension = pathlib.Path(file_path).suffix.lower()
        if file_extension == ".svg":
            return f"data:image/svg+xml;base64,{base64_str}"
        else:
            return f"data:image/png;base64,{base64_str}"
            
    except FileNotFoundError:
        print(f"Error: Image file not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error converting {file_path}: {e}")
        return None


def render_sidebar_info(icon_path, title, text_lines):

    icon_b64 = image_to_base64(icon_path)
    if not icon_b64:
        icon_html = ""
    else:
        icon_html = f'<img src="{icon_b64}" style="width: 24px; height: 24px; margin-right: 8px; vertical-align: middle;">'

    info_box_html = f"""
    <div class="info-box-outer">
        <div class="info-box-inner">
            {icon_html} {title}
        </div>
        <div class="info-box-text">
            {'<br>'.join(text_lines)}
        </div>
    </div>
    """
    
    st.sidebar.markdown(info_box_html, unsafe_allow_html=True)