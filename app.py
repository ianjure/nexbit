import streamlit as st
from PIL import Image
from streamlit_float import *

# [STREAMLIT] PAGE CONFIGURATION
icon = Image.open("icon.png")
st.set_page_config(page_title="Nexbit", page_icon=icon)
st.logo("logo.svg")

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
    [data-testid="stToolbar"] {
        display: none;
    }
    </style>
    """
st.markdown(hide_menu, unsafe_allow_html=True)

# [STREAMLIT] ADJUST HEADER
header = """
    <style>
    [data-testid="stHeader"] {
        height: 7rem;
        width: auto;
        z-index: 1;
    }
    </style>
        """
st.markdown(header, unsafe_allow_html=True)

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

# [STREAMLIT] ADJUST LOGO SIZE
logo = """
    <style>
    [data-testid="stLogo"] {
        width: 10rem;
        height: auto;
    }
    </style>
        """
st.markdown(logo, unsafe_allow_html=True)

# [STREAMLIT] ADJUST SETTINGS BUTTON
set_btn = """
    <style>
    [class="st-emotion-cache-11t4yo9 ef3psqc19"] {
        border-radius: 5rem;
        width: 3rem;
        height: 3rem;
    }
    </style>
        """
st.markdown(set_btn, unsafe_allow_html=True)

# [STREAMLIT] SESSION STATE FOR CRYPTO SELECTED
if "crypto" not in st.session_state:
    st.session_state.crypto = "Bitcoin"

col1, col2, col3 = st.columns(3)

with col1:
    # CRYPTO NAME
    st.markdown(f"<h1 style='text-align: center; font-size: 3rem; font-weight: 500; line-height: 1.2;'>{st.session_state.crypto}</p>", unsafe_allow_html=True)
with col2:
    with st.popover("Change Crypto"):
        st.markdown("Hello World 👋")
        name = st.text_input("What's your name?")
with col3:
    st.metric("Prediction", "70 °F", "1.2 °F")

# [STREAMLIT] CRYPTO OPTIONS
float_init()

@st.dialog("Change Crypto")
def open_options():
    options = ["Bitcoin", "Ethereum", "Solana"]
    selection = st.segmented_control("Cryptocurrency", options, default=st.session_state.crypto, selection_mode="single")
    if selection == st.session_state.crypto:
        print("None")
    else:
        st.session_state.crypto = selection
        st.rerun()
                
button_container = st.container()
with button_container:
    if st.button("💱", type="secondary"):
        open_options()
    
button_css = float_css_helper(width="1.8rem", height="2rem", right="3rem", top="2rem", transition=0)
button_container.float(button_css)
