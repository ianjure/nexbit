from PIL import Image
import streamlit as st

# [STREAMLIT] PAGE CONFIGURATION
icon = Image.open("icon.png")
st.set_page_config(page_title="Nexbit", page_icon=icon)

# [STREAMLIT] HIDE MENU
hide_menu = """
    <style>
    #MainMenu {
        visibility: hidden;
    }
    footer {
        visibility: hidden;
    }
    div[data-testid="stDecoration"] {
        visibility: hidden;
        height: 0%;
        position: fixed;
    }
    div[data-testid="stStatusWidget"] {
        visibility: hidden;
        height: 0%;
        position: fixed;
    }
    </style>
    """
st.markdown(hide_menu, unsafe_allow_html = True)

# [STREAMLIT] ADJUST TOP PADDING
top = """
    <style>
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        margin-top: 0rem;
    }
    </style>
    """
st.markdown(top, unsafe_allow_html=True)

st.write("nexbit")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("Bitcoin")
with col2:
    with st.popover("Change Crypto"):
        st.markdown("Hello World 👋")
        name = st.text_input("What's your name?")
with col3:
    st.metric("Prediction", "70 °F", "1.2 °F")
