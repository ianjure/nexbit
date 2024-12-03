import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_float import *

# [STREAMLIT] PAGE CONFIGURATION
icon = Image.open("assets/icon.png")
st.set_page_config(page_title="Nexbit", page_icon=icon, layout="wide")
st.logo("assets/logo.svg")

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

#  [STEAMLIT] CHANGE FONT STYLE
with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

# [STREAMLIT] ADJUST HEADER
header = """
    <style>
    [data-testid="stHeader"] {
        height: 4rem;
        width: auto;
        z-index: 1;
    }
    </style>
        """
st.markdown(header, unsafe_allow_html=True)

# [STREAMLIT] HIDE TEXT ANCHOR
hide_anchor = """
    <style>
    [data-testid="stHeaderActionElements"] {
        display: none;
    }
    </style>
    """
st.markdown(hide_anchor, unsafe_allow_html=True)

# [STREAMLIT] ADJUST TOP PADDING
top = """
    <style>
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        margin-top: -5rem;
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

# [STREAMLIT] PRIMARY BUTTON COLOR
primary = """
    <style>
    [data-testid="stBaseButton-primary"] {
        color: #1A1C1B;
    }
    </style>
        """
st.markdown(primary, unsafe_allow_html=True)

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

info, chart = st.columns([1,2])

with info:
    # CRYPTO INFO
    logo, name = st.columns([1,3])
    with logo:
        if st.session_state.crypto == "Bitcoin":
            st.image("assets/btc-logo.svg")
    with name:
        st.markdown(f"<h1 style='text-align: left; font-size: 3.5rem; font-weight: 900; line-height: 0.5;'>{st.session_state.crypto}</h1>", unsafe_allow_html=True)
    symbol, supply = st.columns([1,3])
    with symbol:
        st.markdown(f"<h4 style='text-align: left; font-size: 1rem; font-weight: 500; line-height: 0.2;'>{st.session_state.symbol}</h4>", unsafe_allow_html=True)
    with supply:
        st.markdown(f"<h4 style='text-align: left; font-size: 1rem; font-weight: 500; line-height: 0.2;'>TOTAL SUPPLY: {st.session_state.total_supply}</h4>", unsafe_allow_html=True)
    # MODEL PREDICTION
    st.success('Price will increase.', icon=":material/expand_circle_up:")
with chart:
    # PRICE CHART
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    st.line_chart(chart_data)

# [STREAMLIT] CRYPTO OPTIONS
float_init()

@st.dialog("Dashboard Settings", width="small")
def open_options():
    select, export = st.columns(2)
    with select:
        st.write("**CHOOSE A CRYPTOCURRENCY**")
        options = ["Bitcoin", "Ethereum", "Solana"]
        selection = st.selectbox(label="",
                                 options=options,
                                 index=options.index(st.session_state.crypto),
                                 label_visibility="collapsed")
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
        st.write("**EXPORT DASHBOARD AS PDF**")
        st.button(label="**Export**",
                  type="primary",
                  use_container_width=True)
    #export_btn = st.download_button(label="**EXPORT**", data=None, file_name="large_df.pdf", mime="text/csv", use_container_width=True)
        
button_container = st.container()
with button_container:
    if st.button(label="⚙️",
                 type="secondary"):
        open_options()
    
button_css = float_css_helper(width="1.8rem", height="2rem", right="3rem", top="2rem", transition=0)
button_container.float(button_css)
