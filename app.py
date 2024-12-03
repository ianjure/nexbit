import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_float import *

# [STREAMLIT] PAGE CONFIGURATION
icon = Image.open("assets/nexbit-icon.png")
st.set_page_config(page_title="Nexbit", page_icon=icon, layout="wide")
st.logo("assets/nexbit-logo.svg")

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

# [STREAMLIT] HIDE IMAGE ZOOM
hide_zoom = """
    <style>
    [data-testid="stBaseButton-elementToolbar"] {
        display: none;
    }
    </style>
    """
st.markdown(hide_zoom, unsafe_allow_html=True)

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
    st.session_state.total_supply = "21,000,000"
if "website" not in st.session_state:
    st.session_state.website = "https://bitcoin.org/en/"

info, chart = st.columns([1,2])

with info:
    # CRYPTO INFO
    if st.session_state.crypto == "Bitcoin":
        st.image("assets/btc-logo.png")
    elif st.session_state.crypto == "Ethereum":
        st.image("assets/eth-logo.png")
    else:
        st.image("assets/sol-logo.png")
    st.markdown(f"<h1 style='text-align: left; font-size: 3.5rem; font-weight: 600; line-height: 0.8; padding-top: 3px;'>$96,188.43</h1>", unsafe_allow_html=True)
    # MODEL PREDICTION
    increase = """
        <div style='width: auto; height: auto; padding: 12px; margin: 0px; margin-bottom: 15px; border: 2px solid #AFFD86; border-radius: 0.8rem; background-color: #8DFB4E40;'>
            The price will increase.
        </div>
        """
    st.markdown(increase, unsafe_allow_html=True)
    total_supply = f"""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
            <span style='text-align: left; font-size: 1rem; font-weight: 500;'>TOTAL SUPPLY:</span>
            <span style='text-align: left; font-size: 1rem; font-weight: 500; text-align: right'>{st.session_state.total_supply}</span>
        </div>
        """
    st.markdown(total_supply, unsafe_allow_html=True)
    website = f"""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
            <span style='text-align: left; font-size: 1rem; font-weight: 500;'>WEBSITE:</span>
            <span style='text-align: left; font-size: 1rem; font-weight: 500; text-align: right'>
                <a href='{st.session_state.website}' style='color: #AFFD86'>{st.session_state.website}
                </a>
            </span>
        </div>
        """
    st.markdown(website, unsafe_allow_html=True)
with chart:
    # PRICE CHART
    import altair as alt
    from vega_datasets import data
    
    source = data.stocks()
    
    chart = alt.Chart(source).transform_filter(
        'datum.symbol==="GOOG"'
    ).mark_area(
        line={'color':'darkgreen'},
        color=alt.Gradient(
            gradient='linear',
            stops=[alt.GradientStop(color='white', offset=0),
                   alt.GradientStop(color='darkgreen', offset=1)],
            x1=1,
            x2=1,
            y1=1,
            y2=0
        )
    ).encode(
        alt.X('date:T'),
        alt.Y('price:Q')
    )
    st.altair_chart(chart, use_container_width=True)

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
