from PIL import Image
import streamlit as st

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

# [STREAMLIT] CRYPTO OPTIONS
float_init()

@st.dialog("Change Crypto")
def open_options():
    options = ["Bitcoin", "Ethereum", "Solana"]
    selection = st.segmented_control("Cryptocurrency", options, default="Bitcoin", selection_mode="single")
                
button_container = st.container()
with button_container:
    if st.button("💱", type="secondary"):
        open_options()
    
button_css = float_css_helper(width="1.8rem", height="2rem", right="3rem", top="2rem", transition=0)
button_container.float(button_css)
