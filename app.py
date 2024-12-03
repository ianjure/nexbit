import sqlite3
import requests
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
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
        border: 2px solid #FFFFFF;
        width: 3rem;
        height: 3rem;
    }
    </style>
        """
st.markdown(set_btn, unsafe_allow_html=True)

# [CRYPTOCOMPARE API] FETCH CURRENT CRYPTO PRICE
def get_crypto_price(api_key):
    crypto_symbols = ['BTC', 'ETH', 'SOL']
    url = f'https://min-api.cryptocompare.com/data/price'
    price_list = []
    for symbol in crypto_symbols:
        params = {
            'fsym': symbol,
            'tsyms': 'USD',
            "api_key": api_key
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(data)
            #price_list.append(price)
        else:
            print("Error fetching data from CryptoCompare API")
            return None
    #return price_list
prices = get_crypto_price('29f6b8bc885d1ec56c7612acdd69a9a9f1c4575666aa752220805a7a8dd01df9')

# [SQLITE3] FETCHING DATA FROM THE DATABASE
def fetch_data(database, table):
    conn = sqlite3.connect(database)
    result = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    conn.close()
    return result

crypto_info = fetch_data('nexbit.db', 'Cryptocurrency')

# [STREAMLIT] SESSION STATE FOR CRYPTO SELECTED
if "crypto" not in st.session_state:
    st.session_state.crypto = crypto_info["name"][0]
if "symbol" not in st.session_state:
    st.session_state.symbol = crypto_info["symbol"][0]
if "market_cap" not in st.session_state:
    st.session_state.market_cap = crypto_info["market_cap"][0]
if "total_supply" not in st.session_state:
    st.session_state.total_supply = crypto_info["total_supply"][0]
if "website" not in st.session_state:
    st.session_state.website = crypto_info["website"][0]
if "accuracy" not in st.session_state:
    st.session_state.accuracy = "54.07%"

info, chart = st.columns([1,2])

with info:
    # CRYPTO LOGO AND NAME
    if st.session_state.crypto == "Bitcoin":
        st.image("assets/btc-logo.png")
    elif st.session_state.crypto == "Ethereum":
        st.image("assets/eth-logo.png")
    else:
        st.image("assets/sol-logo.png")
    # CRYPTO PRICE
    st.markdown(f"<h1 style='text-align: left; font-size: 3.5rem; font-weight: 600; line-height: 0.8; padding-top: 3px;'>{prices}</h1>", unsafe_allow_html=True)
    # MODEL PREDICTION
    date_acc = f"""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
            <span style='text-align: left; font-size: 0.7rem; font-weight: 500;'>Date: {datetime.now().strftime("%b %d, %Y")}</span>
            <span style='text-align: center; font-size: 0.7rem; font-weight: 500;'>Accuracy: {st.session_state.accuracy}</span>
            <span style='text-align: right; font-size: 0.7rem; font-weight: 500;'>Confidence: {st.session_state.accuracy}</span>
        </div>
        """
    st.markdown(date_acc, unsafe_allow_html=True)
    increase = f"""
        <div style='width: auto; height: auto; padding: 12px; margin: 0px; margin-bottom: 15px; border: 2px solid #AFFD86; border-radius: 0.8rem; background-color: #8DFB4E1A;'>
            <span style='text-align: left; font-size: 1rem; font-weight: 500;'>The price will increase tomorrow.</span>
        </div>
        """
    st.markdown(increase, unsafe_allow_html=True)
    # CRYPTO INFO
    market_cap = f"""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
            <span style='text-align: left; font-size: 1rem; font-weight: 500;'>Market Cap:</span>
            <span style='text-align: right; font-size: 1rem; font-weight: 500;'>{"${:,.2f}".format(float(st.session_state.market_cap))}</span>
        </div>
        """
    st.markdown(market_cap, unsafe_allow_html=True)
    total_supply = f"""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
            <span style='text-align: left; font-size: 1rem; font-weight: 500;'>Total Supply:</span>
            <span style='text-align: right; font-size: 1rem; font-weight: 500;'>{"${:,.2f}".format(float(st.session_state.total_supply))}</span>
        </div>
        """
    st.markdown(total_supply, unsafe_allow_html=True)
    website = f"""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
            <span style='text-align: left; font-size: 1rem; font-weight: 500;'>Website:</span>
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
        line={'color': '#8DFB4E'},
        color=alt.Gradient(
            gradient='linear',
            stops=[alt.GradientStop(color='#1A1C1B', offset=0),
                   alt.GradientStop(color='darkgreen', offset=1)],
            x1=1,
            x2=1,
            y1=1,
            y2=0
        )
    ).encode(
        alt.X('date:T', title=None),
        alt.Y('price:Q', title=None)
    ).properties(
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
    

# [STREAMLIT] CRYPTO OPTIONS
float_init()

@st.dialog("Dashboard Settings", width="small")
def open_options():
    select, export = st.columns(2)
    with select:
        st.markdown(f"<h4 style='text-align: left; font-size: 1rem; font-weight: 500; line-height: 0.8;'>Choose a Cryptocurrency</h4>", unsafe_allow_html=True)
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
                st.session_state.symbol = crypto_info["symbol"][0]
                st.session_state.market_cap = crypto_info["market_cap"][0]
                st.session_state.total_supply = crypto_info["total_supply"][0]
                st.session_state.website = crypto_info["website"][0]
            elif selection == "Ethereum":
                st.session_state.symbol = crypto_info["symbol"][1]
                st.session_state.market_cap = crypto_info["market_cap"][1]
                st.session_state.total_supply = crypto_info["total_supply"][1]
                st.session_state.website = crypto_info["website"][1]
            else:
                st.session_state.symbol = crypto_info["symbol"][2]
                st.session_state.market_cap = crypto_info["market_cap"][2]
                st.session_state.total_supply = crypto_info["total_supply"][2]
                st.session_state.website = crypto_info["website"][2]
            st.rerun()
    with export:
        st.markdown(f"<h4 style='text-align: left; font-size: 1rem; font-weight: 500; line-height: 0.8;'>Export Dashboard as PDF</h4>", unsafe_allow_html=True)
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
