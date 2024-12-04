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

# [STREAMLIT] COLOR PALETTE
color1_dark = "#8DFB4E"
color1_light = "#AFFD86"
color2_dark = "#3a1a1d"
color2_light = "#e2352f"
black_dark = "#0d1216"
black_light = "#1b242d"

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
        background-color: """ + black_light + """;
        transition: background-color 0.3s ease, transform 0.2s ease;
        text-decoration: none;
        color: #FFFFFF;
    }
    .news-card:hover {
        background-color: """ + black_light + """;
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
        color: """ + color1_light + """;
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

# [STREAMLIT] CATEGORIZE SCORE FOR NEWS CARD
def categorize_score(score):
    if score > 0.5:
        return 'Strong Positive'
    elif 0 < score <= 0.5:
        return 'Moderate Positive'
    elif score == 0:
        return 'Neutral'
    elif -0.5 <= score < 0:
        return 'Moderate Negative'
    else:
        return 'Strong Negative'

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
    price_df = st.session_state.price_data
    pct_change = ((st.session_state.price - price_df["close_price"].iloc[-2]) / price_df["close_price"].iloc[-2]) * 100
    if pct_change > 0:
        margin = "-6px"
        arrow = "arrow_drop_up"
    else:
        margin = "-2px"
        arrow = "arrow_drop_down"
    price_change = f"""
        <div style="display: flex; justify-content: flex-start; align-items: center;">
            <h1 style="font-size: 3.5rem; font-weight: 600; line-height: 0.8; padding-top: 3px;">
                {"${:,.1f}".format(float(st.session_state.price))}
            </h1>
            <span>
                <i class="material-icons" style="font-size: 2rem; position: relative; top: {margin}; color: {color2_light};">{arrow}</i> 
            </span>
            <h4 style="font-size: 1.2rem; font-weight: 700; margin: 0; position: relative; top: -5px; color: {color2_light};">{"{:.2f}".format(float(pct_change))}%</h4>
        </div>
        <style>
            @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
        </style>
        """
    st.markdown(price_change, unsafe_allow_html=True)
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
        <div style='width: auto; height: auto; padding-top: 12px; padding-bottom: 12px; padding-left: 15px; padding-right: 15px; margin: 0px; margin-bottom: 15px; border: 2px solid {color1_light}; border-radius: 0.8rem; background-color: {color1_dark}1A;'>
            <span style='text-align: left; font-size: 1rem; font-weight: 500;'>The price will increase tomorrow.</span>
        </div>
        """
    st.markdown(increase, unsafe_allow_html=True)
    # CRYPTO INFO
    market_cap = f"""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
            <span style='text-align: left; font-size: 1rem; font-weight: 500; color: #C7C7C7;'>Market Cap:</span>
            <span style='text-align: right; font-size: 1rem; font-weight: 500;'>{"${:,.2f}".format(float(st.session_state.market_cap))}</span>
        </div>
        """
    st.markdown(market_cap, unsafe_allow_html=True)
    total_supply = f"""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
            <span style='text-align: left; font-size: 1rem; font-weight: 500; color: #C7C7C7;'>Total Supply:</span>
            <span style='text-align: right; font-size: 1rem; font-weight: 500;'>{"${:,.2f}".format(float(st.session_state.total_supply))}</span>
        </div>
        """
    st.markdown(total_supply, unsafe_allow_html=True)
    website = f"""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
            <span style='text-align: left; font-size: 1rem; font-weight: 500; color: #C7C7C7;'>Website:</span>
            <span style='text-align: left; font-size: 1rem; font-weight: 500; text-align: right'>
                <a href='{st.session_state.website}' style='text-decoration: none; color: {color1_light};'>{st.session_state.website.replace("https://", "").replace("/", "").replace("www.","")}
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
    
    price_chart = alt.Chart(df).mark_area(
        line={'color': f'{color2_light}'},
        color=alt.Gradient(
            gradient='linear',
            stops=[alt.GradientStop(color=f'{black_dark}', offset=0),
                   alt.GradientStop(color=f'{color2_dark}', offset=1)],
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
    st.altair_chart(price_chart, use_container_width=True)

sentiment_section, news_section = st.columns([3,2])

with sentiment_section:
    # DAILY AVERAGE SENTIMENT
    ave_sentiment_title = f"<h4 style='text-align: left; font-size: 1rem; font-weight: 600; margin-top: -10px; color: {color1_light};'>DAILY AVERAGE SENTIMENT</h4>"
    st.markdown(ave_sentiment_title, unsafe_allow_html=True)
    news_df = st.session_state.news
    news_df = news_df.copy()
    news_df['date'] = pd.to_datetime(news_df['date'])
    news_df['day_of_week'] = news_df['date'].dt.dayofweek
    avg_sentiment_by_day = news_df.groupby('day_of_week')['sentiment'].mean().reset_index()
    avg_sentiment_by_day['day_name'] = avg_sentiment_by_day['day_of_week'].map({
        0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'
    })
    max_score_day = avg_sentiment_by_day.loc[avg_sentiment_by_day['sentiment'].idxmax(), 'day_name']
    ave_sent_chart = alt.Chart(avg_sentiment_by_day).mark_bar(
        cornerRadiusTopLeft=5,
        cornerRadiusTopRight=5,
        color=alt.Gradient(
            gradient='linear',
            stops=[alt.GradientStop(color=f'{black_dark}', offset=0),
                   alt.GradientStop(color=f'{color1_dark}', offset=1)],
            x1=1,
            x2=1,
            y1=1,
            y2=0
        )
    ).encode(
        x=alt.X('day_name:N', 
                sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 
                title=None, 
                axis=alt.Axis(labelAngle=0)),
        y=alt.Y('sentiment:Q', 
                title=None, 
                axis=alt.Axis(grid=True, gridColor='#2C2E2D'))
    ).properties(
        height=300,
        width='container'
    )
    highlighted_bar = alt.Chart(avg_sentiment_by_day).mark_bar(
        cornerRadiusTopLeft=5,
        cornerRadiusTopRight=5,
        color=alt.Gradient(
            gradient='linear',
            stops=[alt.GradientStop(color=f'{black_dark}', offset=0),
                   alt.GradientStop(color=f'{color2_dark}', offset=1)],
            x1=1,
            x2=1,
            y1=1,
            y2=0
        )
    ).encode(
        x=alt.X('day_name:N', 
                sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 
                title=None, 
                axis=alt.Axis(labelAngle=0)),
        y=alt.Y('sentiment:Q', 
                title=None, 
                axis=alt.Axis(grid=True, gridColor='#2C2E2D')),
    ).transform_filter(
        alt.datum.day_name == max_score_day
    ).properties(
        height=300,
        width='container'
    )
    text_format = alt.Chart(avg_sentiment_by_day).mark_text(
        align='center',
        baseline='bottom',
        fontSize=14,
        dy=-5,
        color=f'{color2_dark}'
    ).transform_filter(
        alt.datum.day_name == max_score_day
    ).encode(
        x=alt.X('day_name:N',
               sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
        y=alt.Y('sentiment:Q'),
        text=alt.Text('sentiment:Q', format='.2f')
    )
    final_ave_sent_chart = alt.layer(ave_sent_chart, highlighted_bar, text_format).resolve_scale(
        color='independent'
    )
    st.altair_chart(final_ave_sent_chart, use_container_width=True)
    # SENTIMENT STATISTIC
    sentiment_stat_title = f"<h4 style='text-align: left; font-size: 1rem; font-weight: 600; margin-top: -10px; color: {color1_light};'>SENTIMENT STATISTIC</h4>"
    st.markdown(sentiment_stat_title, unsafe_allow_html=True)
with news_section:
    # NEWS STATISTIC
    news_stat_title = f"<h4 style='text-align: left; font-size: 1rem; font-weight: 600; margin-top: -10px; color: {color1_light};'>NEWS STATISTIC</h4>"
    st.markdown(news_stat_title, unsafe_allow_html=True)
    news_df = st.session_state.news
    news_df = news_df.copy()
    news_df['date'] = pd.to_datetime(news_df['date'])
    current_month = datetime.now().month
    current_year = datetime.now().year
    current_month_news = news_df[(news_df['date'].dt.year == current_year) & (news_df['date'].dt.month == current_month)]
    current_month_news_count = current_month_news.shape[0]
    news_count_m = f"""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-top: -5px; margin-bottom: 5px;'>
            <span style='text-align: left; font-size: 1rem; font-weight: 500; color: #C7C7C7;'>Monthly News Count:</span>
            <span style='text-align: right; font-size: 1rem; font-weight: 500;'>{current_month_news_count}</span>
        </div>
        """
    st.markdown(news_count_m, unsafe_allow_html=True)
    current_year_news = news_df[news_df['date'].dt.year == current_year]
    current_year_news_count = current_year_news.shape[0]
    news_count_y = f"""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;'>
            <span style='text-align: left; font-size: 1rem; font-weight: 500; color: #C7C7C7;'>Annual News Count:</span>
            <span style='text-align: right; font-size: 1rem; font-weight: 500;'>{current_year_news_count}</span>
        </div>
        """
    st.markdown(news_count_y, unsafe_allow_html=True)
    top_news_source_name = news_df['source'].value_counts().idxmax()
    top_news_source = f"""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;'>
            <span style='text-align: left; font-size: 1rem; font-weight: 500; color: #C7C7C7;'>Top News Source:</span>
            <span style='text-align: right; font-size: 1rem; font-weight: 500;'>{top_news_source_name}</span>
        </div>
        """
    st.markdown(top_news_source, unsafe_allow_html=True)
    # LATEST NEWS
    latest_news_title = f"<h4 style='text-align: left; font-size: 1rem; font-weight: 600; margin-top: -10px; color: {color1_light};'>LATEST NEWS</h4>"
    st.markdown(latest_news_title, unsafe_allow_html=True)
    news_df = st.session_state.news
    news_1 = f"""
    <a class='news-card' target='_blank' href='{news_df["url"].iloc[-1]}'>
        <span class='title'>{news_df["title"].iloc[-1].title()}</span>
        <span class='summary'>{news_df["summary"].iloc[-1]}</span>
        <div class='meta-info'>
            <span>Source: {news_df["source"].iloc[-1]}</span>
            <span class='sentiment'>{categorize_score(news_df["sentiment"].iloc[-1])}</span>
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
            <span class='sentiment'>{categorize_score(news_df["sentiment"].iloc[-2])}</span>
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
            <span class='sentiment'>{categorize_score(news_df["sentiment"].iloc[-3])}</span>
        </div>
    </a>
    """
    st.markdown(news_3, unsafe_allow_html=True)

# [STREAMLIT] CRYPTO OPTIONS
float_init()

@st.dialog("Dashboard Settings", width="small")
def open_options():
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

button_container = st.container()
with button_container:
    if st.button(label="⚙️",
                 type="secondary"):
        open_options()
    
button_css = float_css_helper(width="1.8rem", height="2rem", right="2rem", top="1.3rem", transition=0)
button_container.float(button_css)
