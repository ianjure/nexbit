import sqlite3
import requests
import altair as alt
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from PIL import Image
from streamlit_float import *

# [STREAMLIT] PAGE CONFIGURATION
icon = Image.open("assets/nexbit-icon.png")
st.set_page_config(page_title="Nexbit: Crypto Analysis and Forecasting Dashboard", page_icon=icon, layout="wide")
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
        height: 5.3rem;
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
        width: 2.5rem;
        height: 2.5rem;
    }
    </style>
        """
st.markdown(set_btn, unsafe_allow_html=True)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0&icon_names=currency_exchange');
    
    h1 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600;
    }
    .animated-price {
        font-family: 'Poppins', sans-serif !important;
        text-align: left;
        font-size: 3.5rem;
        font-weight: 600;
        line-height: 0.8;
        padding-top: -50px;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
        [data-testid="stIFrame"] {
            padding: 0 !important;
            margin: 0 !important;
            border: none; /* Remove any border, if present */
            display: block; /* Ensure full-width display */
        }
    </style>
    """,
   

# [STREAMLIT] HOVER EFFECT
hover_card = """
    <style>
    .news-card {
        display: block;
        width: auto;
        height: auto;
        padding-top: 12px;
        padding-bottom: 12px;
        padding-left: 15px;
        padding-right: 15px;
        margin: 0px;
        margin-bottom: 15px;
        border-radius: 0.8rem;
        background-color: #2C2E2D;
        transition: background-color 0.3s ease, transform 0.2s ease;
        text-decoration: none;
        color: #FFFFFF;
    }
    .news-card:hover {
        background-color: #575D59;
        transform: scale(1.02);
        text-decoration: none;
        color: #FFFFFF;
        cursor: pointer;
    }
    .news-card span {
        display: block;
    }
    .news-card .title {
        text-align: justify;
        font-size: 1rem;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 8px;
    }
    .news-card .summary {
        text-align: justify;
        font-size: 0.8rem;
        font-weight: 300;
        color: #FFFFFF;
        margin-bottom: 10px;
    }
    .news-card .meta-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.7rem;
        font-weight: 400;
        color: #8F8F8F;
    }
    .news-card .sentiment {
        color: #AFFD86;
    }
    </style>
    """
st.markdown(hover_card, unsafe_allow_html=True)

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
#prices = get_crypto_price('29f6b8bc885d1ec56c7612acdd69a9a9f1c4575666aa752220805a7a8dd01df9')

# [SQLITE3] FETCHING DATA FROM THE DATABASE
def fetch_data(database, table):
    conn = sqlite3.connect(database)
    result = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    conn.close()
    return result
crypto_info = fetch_data('nexbit.db', 'Cryptocurrency')
crypto_price = fetch_data('nexbit.db', 'Price')
crypto_news = fetch_data('nexbit.db', 'News')

# [STREAMLIT] SESSION STATE FOR CRYPTO SELECTED
if "price" not in st.session_state:
    st.session_state.price = crypto_price[crypto_price["crypto_id"]==1]["close_price"].iloc[-1]
if "price_data" not in st.session_state:
    st.session_state.price_data = crypto_price[crypto_price["crypto_id"]==1]
if "crypto" not in st.session_state:
    st.session_state.crypto = crypto_info["name"].iloc[0]
if "symbol" not in st.session_state:
    st.session_state.symbol = crypto_info["symbol"].iloc[0]
if "market_cap" not in st.session_state:
    st.session_state.market_cap = crypto_info["market_cap"].iloc[0]
if "total_supply" not in st.session_state:
    st.session_state.total_supply = crypto_info["total_supply"].iloc[0]
if "website" not in st.session_state:
    st.session_state.website = crypto_info["website"].iloc[0]
if "accuracy" not in st.session_state:
    st.session_state.accuracy = "54.07%"
if "news" not in st.session_state:
    st.session_state.news = crypto_news[crypto_news["crypto_id"]==1]

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
    #st.markdown(f"<h1 style='text-align: left; font-size: 3.5rem; font-weight: 600; line-height: 0.8; padding-top: 3px;'>{"${:,.2f}".format(float(st.session_state.price))}</h1>", unsafe_allow_html=True)
    # Display the animated number
    #st.markdown("<h1 style='text-align: left; font-size: 3.5rem; font-weight: 600; line-height: 0.8; padding-top: 3px;'>Animated Price</h1>", unsafe_allow_html=True)
    price_value = st.session_state['price']
    st.components.v1.html(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');
        #price-counter {
            font-family: 'Poppins', sans-serif !important;
            text-align: left;
            font-size: 3.5rem;
            font-weight: 600;
            line-height: 0.8;
            padding-top: 3px;
            color: white;
        }
        </style>
        <h1 class="animated-price" id="price-counter">$0.00</h1>
        <script>
            (function() {
                const targetPrice = """ + str(price_value) + """;
                const duration = 2000;  // Animation duration in milliseconds
                const frameRate = 60;   // Number of frames per second
                const totalFrames = Math.round((duration / 1000) * frameRate);
                const increment = targetPrice / totalFrames;
    
                let currentPrice = 0;
                let frame = 0;
    
                function updateCounter() {
                    if (frame < totalFrames) {
                        currentPrice += increment;
                        document.getElementById("price-counter").innerText = "$" + currentPrice.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
                        frame++;
                        requestAnimationFrame(updateCounter);
                    } else {
                        document.getElementById("price-counter").innerText = "$" + targetPrice.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
                    }
                }
    
                updateCounter();
            })();
        </script>
        """, height=80)
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
        <div style='width: auto; height: auto; padding-top: 12px; padding-bottom: 12px; padding-left: 15px; padding-right: 15px; margin: 0px; margin-bottom: 15px; border: 2px solid #AFFD86; border-radius: 0.8rem; background-color: #8DFB4E1A;'>
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
    df = st.session_state.price_data
    df = df[['date', 'close_price']]
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    
    chart = alt.Chart(df).mark_area(
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
        alt.Y('close_price:Q', title=None, axis=alt.Axis(orient='right',  grid=True, gridColor='#2C2E2D'))
    ).properties(
        height=315,
        padding={'top': 20, 'bottom': 20, 'left': 2, 'right': 2}
    )
    st.altair_chart(chart, use_container_width=True)

ave_sentiment, latest_news = st.columns([3,2])

with ave_sentiment:
    ave_sentiment_title = "<h4 style='text-align: left; font-size: 1rem; font-weight: 600; margin-top: -10px; color: #8DFB4E;'>DAILY AVERAGE SENTIMENT</h4>"
    st.markdown(ave_sentiment_title, unsafe_allow_html=True)
with latest_news:
    latest_news_title = "<h4 style='text-align: left; font-size: 1rem; font-weight: 600; margin-top: -10px; color: #8DFB4E;'>LATEST NEWS</h4>"
    st.markdown(latest_news_title, unsafe_allow_html=True)
    news_df = st.session_state.news
    news_1 = f"""
    <a class='news-card' target='_blank' href='{news_df["url"].iloc[-1]}'>
        <span class='title'>{news_df["title"].iloc[-1].title()}</span>
        <span class='summary'>{news_df["summary"].iloc[-1]}</span>
        <div class='meta-info'>
            <span>Source: {news_df["source"].iloc[-1]}</span>
            <span class='sentiment'>Score: {news_df["sentiment"].iloc[-1]}</span>
        </div>
    </a>
    """
    st.markdown(news_1, unsafe_allow_html=True)
    news_2 = f"""
    <a class='news-card' target='_blank' href='{news_df["url"].iloc[-2]}'>
        <span class='title'>{news_df["title"].iloc[-2].title()}</span>
        <span class='summary'>{news_df["summary"].iloc[-2]}</span>
        <div class='meta-info'>
            <span>Source: {news_df["source"].iloc[-2]}</span>
            <span class='sentiment'>Score: {news_df["sentiment"].iloc[-2]}</span>
        </div>
    </a>
    """
    st.markdown(news_2, unsafe_allow_html=True)
    news_3 = f"""
    <a class='news-card' target='_blank' href='{news_df["url"].iloc[-3]}'>
        <span class='title'>{news_df["title"].iloc[-3].title()}</span>
        <span class='summary'>{news_df["summary"].iloc[-3]}</span>
        <div class='meta-info'>
            <span>Source: {news_df["source"].iloc[-3]}</span>
            <span class='sentiment'>Score: {news_df["sentiment"].iloc[-3]}</span>
        </div>
    </a>
    """
    st.markdown(news_3, unsafe_allow_html=True)

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
                st.session_state.price = crypto_price[crypto_price["crypto_id"]==1]["close_price"].iloc[-1]
                st.session_state.price_data = crypto_price[crypto_price["crypto_id"]==1]
                st.session_state.symbol = crypto_info["symbol"].iloc[0]
                st.session_state.market_cap = crypto_info["market_cap"].iloc[0]
                st.session_state.total_supply = crypto_info["total_supply"].iloc[0]
                st.session_state.website = crypto_info["website"].iloc[0]
                st.session_state.news = crypto_news[crypto_news["crypto_id"]==1]
            elif selection == "Ethereum":
                st.session_state.price = crypto_price[crypto_price["crypto_id"]==2]["close_price"].iloc[-1]
                st.session_state.price_data = crypto_price[crypto_price["crypto_id"]==2]
                st.session_state.symbol = crypto_info["symbol"].iloc[1]
                st.session_state.market_cap = crypto_info["market_cap"].iloc[1]
                st.session_state.total_supply = crypto_info["total_supply"].iloc[1]
                st.session_state.website = crypto_info["website"].iloc[1]
                st.session_state.news = crypto_news[crypto_news["crypto_id"]==2]
            else:
                st.session_state.price = crypto_price[crypto_price["crypto_id"]==3]["close_price"].iloc[-1]
                st.session_state.price_data = crypto_price[crypto_price["crypto_id"]==3]
                st.session_state.symbol = crypto_info["symbol"].iloc[2]
                st.session_state.market_cap = crypto_info["market_cap"].iloc[2]
                st.session_state.total_supply = crypto_info["total_supply"].iloc[2]
                st.session_state.website = crypto_info["website"].iloc[2]
                st.session_state.news = crypto_news[crypto_news["crypto_id"]==3]
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
    
button_css = float_css_helper(width="1.8rem", height="2rem", right="2rem", top="1.3rem", transition=0)
button_container.float(button_css)
