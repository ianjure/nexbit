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
if "symbol" not in st.session_state:
    st.session_state.symbol = "BTC"
if "total_supply" not in st.session_state:
    st.session_state.total_supply = "100000"

info, prediction = st.columns([1, 2])

with info:
    # CRYPTO NAME
    st.markdown(f"<h1 style='text-align: left; font-size: 3rem; font-weight: 500; line-height: 1.2;'>{st.session_state.crypto}</h1>", unsafe_allow_html=True)
    symbol, supply = st.columns([1, 2])
    with symbol:
        st.markdown(f"<h4 style='text-align: left; font-size: 1.5rem; font-weight: 500; line-height: 1.2;'>{st.session_state.symbol}</h4>", unsafe_allow_html=True)
    with supply:
        st.markdown(f"<h4 style='text-align: left; font-size: 1.5rem; font-weight: 500; line-height: 1.2;'>{st.session_state.total_supply}</h4>", unsafe_allow_html=True)
with prediction:
    # MODEL PREDICTION
    st.success('This is a success message!', icon=":material/expand_circle_up:")

# [STREAMLIT] CRYPTO OPTIONS
float_init()

@st.dialog("Dashboard Settings", width="small")
def open_options():
    select, export = st.columns(2)
    with select:
        options = ["Bitcoin", "Ethereum", "Solana"]
        selection = st.segmented_control(label="**CHOOSE A CRYPTOCURRENCY**",
                                         options=options,
                                         selection_mode="single",
                                         default=st.session_state.crypto)
        if selection == st.session_state.crypto:
            print("None")
        else:
            st.session_state.crypto = selection
            if selection == "Bitcoin":
                st.session_state.symbol = "BTC"
            elif selection == "Ethereum":
                st.session_state.symbol = "ETH"
            else:
                st.session_state.symbol = "SOL"
            st.rerun()
    with export:
        export_btn = st.download_button(label="**EXPORT DASHBOARD**",
                                        data=None,
                                        file_name="large_df.pdf",
                                        mime="text/csv",
                                        use_container_width=True)
        
button_container = st.container()
with button_container:
    if st.button(label="⚙️",
                 type="secondary"):
        open_options()
    
button_css = float_css_helper(width="1.8rem", height="2rem", right="3rem", top="2rem", transition=0)
button_container.float(button_css)
