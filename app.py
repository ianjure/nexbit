import requests
import altair as alt
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
from PIL import Image
from streamlit_float import *
from supabase import create_client, Client

# [STREAMLIT] PAGE CONFIGURATION
icon = Image.open("assets/nexbit-icon.png")
st.set_page_config(page_title="Nexbit: Analytics & Forecasting", page_icon=icon, layout="wide")
st.logo("assets/nexbit-logo.svg")

# [SUPABASE] SECRETS CONFIGURATION
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# [STREAMLIT] COLOR PALETTE
color1_dark = "#8DFB4E"
color1_light = "#AFFD86"
color2_dark = "#3a1a1d"
color2_light = "#e2352f"
text_light = "#becbdc"
text_dark = "#8293a7"
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
        color: """ + color1_dark + """;
    }
    </style>
        """
st.markdown(primary, unsafe_allow_html=True)

# [STREAMLIT] ADJUST SETTINGS BUTTON
set_btn = """
    <style>
    [data-testid="stBaseButton-secondary"] {
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
        color: """ + text_light + """;
        margin-bottom: 10px;
    }
    .news-card .meta-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.7rem;
        font-weight: 400;
        color: """ + text_dark + """;
    }
    </style>
    """
st.markdown(hover_card, unsafe_allow_html=True)

# [STREAMLIT] INFO EFFECT
info_hover = """
    <style>
    .info-icon {
        position: relative;
        cursor: default;
    }
    .info-tooltip {
        display: none;
        cursor: default;
        position: absolute;
        top: 75%;
        left: 50%;
        transform: translateX(-50%);
        background-color: """ + black_light + """;
        color: """ + text_dark + """;
        padding-top: 20px;
        padding-bottom: 15px;
        padding-left: 20px;
        padding-right: 20px;
        border-radius: 6px;
        font-size: 0.8rem;
        box-shadow: 0px 8px 8px rgba(0, 0, 0, 0.2);
        z-index: 10;
        white-space: normal;
        width: 250px;
        word-wrap: break-word;
        text-align: left;
    }
    .info-icon:hover .info-tooltip {
        display: block;
        cursor: default;
    }
    </style>
    """
st.markdown(info_hover, unsafe_allow_html=True)

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
#pass = lSwEVpkPlxYq9kls

# [SUPABASE] FETCHING DATA FROM THE DATABASE
def fetch_data(table, url, key):
    supabase: Client = create_client(url, key)
    response = supabase.table(table).select('*').execute()
    if response.data:
        data = pd.DataFrame(response.data)
        return data
        
crypto_info = fetch_data('Cryptocurrency', SUPABASE_URL, SUPABASE_KEY)
crypto_price = fetch_data('Price', SUPABASE_URL, SUPABASE_KEY)
crypto_news = fetch_data('News', SUPABASE_URL, SUPABASE_KEY)

# [STREAMLIT] CATEGORIZE SCORE FOR NEWS CARD
def categorize_score(score, color=False):
    if color:
        if score > 0.5:
            return color1_light
        elif 0 < score <= 0.5:
            return color1_light
        elif score == 0:
            return text_light
        elif -0.5 <= score < 0:
            return color2_light
        else:
            return color2_light
    else:
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
        color = color1_light
        margin = "-6px"
        arrow = "arrow_drop_up"
    else:
        color = color2_light
        margin = "-2px"
        arrow = "arrow_drop_down"
    price_change = f"""
        <div style="display: flex; justify-content: flex-start; align-items: center;">
            <h1 style="font-size: 3.5rem; font-weight: 600; line-height: 0.8; padding-top: 3px;">
                {"${:,.1f}".format(float(st.session_state.price))}
            </h1>
            <span>
                <i class="material-icons" style="font-size: 2rem; position: relative; top: {margin}; color: {color};">{arrow}</i> 
            </span>
            <h4 style="font-size: 1.2rem; font-weight: 700; margin: 0; position: relative; top: -5px; color: {color};">{"{:.2f}".format(float(pct_change))}%</h4>
        </div>
        <style>
            @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
        </style>
        """
    st.markdown(price_change, unsafe_allow_html=True)
    # MODEL PREDICTION
    date_acc = f"""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
            <span style='text-align: left; font-size: 0.7rem; font-weight: 500; color: {text_light};'>Date: {datetime.now().strftime("%b %d, %Y")}</span>
            <span style='text-align: center; font-size: 0.7rem; font-weight: 500; color: {text_light};'>Accuracy: {st.session_state.accuracy}</span>
            <span style='text-align: right; font-size: 0.7rem; font-weight: 500; color: {text_light};'>Confidence: {st.session_state.accuracy}</span>
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
            <span style='text-align: left; font-size: 1rem; font-weight: 500; color: {text_dark};'>Market Cap</span>
            <span style='text-align: right; font-size: 1rem; font-weight: 500;'>{"${:,.2f}".format(float(st.session_state.market_cap))}</span>
        </div>
        """
    st.markdown(market_cap, unsafe_allow_html=True)
    total_supply = f"""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
            <span style='text-align: left; font-size: 1rem; font-weight: 500; color: {text_dark};'>Total Supply</span>
            <span style='text-align: right; font-size: 1rem; font-weight: 500;'>{"${:,.2f}".format(float(st.session_state.total_supply))}</span>
        </div>
        """
    st.markdown(total_supply, unsafe_allow_html=True)
    website = f"""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
            <span style='text-align: left; font-size: 1rem; font-weight: 500; color: {text_dark};'>Website</span>
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
        alt.Y('close_price:Q', title=None, axis=alt.Axis(orient='right',  grid=True, gridColor=f'{text_dark}')),
        tooltip=[
            alt.Tooltip("date:T", title="Date"),
            alt.Tooltip("close_price:Q", title="Closing Price")]
    ).properties(
        height=315,
        padding={'top': 20, 'bottom': 20, 'left': 2, 'right': 2}
    ).configure_axis(
        labelColor=f'{text_dark}',
        gridWidth=0.2
    )
    st.altair_chart(price_chart, use_container_width=True)

sentiment_section, news_section = st.columns([3,2])

with sentiment_section:
    # DAILY AVERAGE SENTIMENT
    ave_sentiment_title = f"""
        <div style='display: flex; align-items: center; gap: 6px; margin-top: -10px;'>
            <h4 style='text-align: left; font-size: 1rem; font-weight: 600; color: {text_light};'>
                DAILY AVERAGE SENTIMENT
            </h4>
            <span class="info-icon" style="cursor: default;">
                <i class="material-symbols-outlined" style="font-size: 1rem; color: {text_light}; cursor: default;">info</i>
                <div class="info-tooltip">
                    The daily aggregated sentiment scores are sourced from Alpha Vantage.
                    <br>
                    <br>
                    Positive Sentiment > 0
                    <br>
                    Negative Sentiment < 0
                </div>
            </span>
            <style>
                @import url('https://fonts.googleapis.com/icon?family=Material+Symbols+Outlined');
            </style>
        </div>
        """
    st.markdown(ave_sentiment_title, unsafe_allow_html=True)
    
    news_df = st.session_state.news
    news_df = news_df.copy()
    
    news_df['date'] = pd.to_datetime(news_df['date'])
    news_df['day_of_week'] = news_df['date'].dt.dayofweek
    
    avg_sentiment_by_day = news_df.groupby('day_of_week')['sentiment'].mean().reset_index()
    avg_sentiment_by_day['day_name'] = avg_sentiment_by_day['day_of_week'].map({
        0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'})
    max_score_day = avg_sentiment_by_day.loc[avg_sentiment_by_day['sentiment'].idxmax(), 'day_name']
    
    ave_sent_chart = alt.Chart(avg_sentiment_by_day).mark_bar(
        opacity=0.7,
        cornerRadiusTopLeft=5,
        cornerRadiusTopRight=5,
        color=alt.Gradient(
            gradient='linear',
            stops=[alt.GradientStop(color=f'{black_dark}', offset=0),
                   alt.GradientStop(color='#0a2f1e', offset=1)],
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
                axis=alt.Axis(grid=True, gridColor=f'{text_dark}')),
        tooltip=[
            alt.Tooltip("day_name:N", title="Day"),
            alt.Tooltip("sentiment:Q", title="Avg Score")]
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
                   alt.GradientStop(color=f'{color1_light}', offset=1)],
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
                axis=alt.Axis(grid=True, gridColor=f'{text_dark}')),
        tooltip=[
            alt.Tooltip("day_name:N", title="Day"),
            alt.Tooltip("sentiment:Q", title="Avg Score")]
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
        font='Roboto',
        fontWeight='bold',
        dy=-5,
        color=f'{color1_light}'
    ).transform_filter(
        alt.datum.day_name == max_score_day
    ).encode(
        x=alt.X('day_name:N',
               sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
        y=alt.Y('sentiment:Q'),
        text=alt.Text('sentiment:Q', format='.2f'),
        tooltip=[
            alt.Tooltip("day_name:N", title="Day"),
            alt.Tooltip("sentiment:Q", title="Avg Score")]
    )
    
    final_ave_sent_chart = alt.layer(ave_sent_chart, highlighted_bar, text_format).resolve_scale(
        color='independent'
    ).configure_axis(
        labelColor=f'{text_dark}',
        gridWidth=0.2
    )
    st.altair_chart(final_ave_sent_chart, use_container_width=True)

    # SENTIMENT STATISTIC
    sentiment_stat_title = f"<h4 style='text-align: left; font-size: 1rem; font-weight: 600; margin-top: -10px; color: {text_light};'>SENTIMENT STATISTIC</h4>"
    st.markdown(sentiment_stat_title, unsafe_allow_html=True)

    chart_1, chart_2 = st.columns(2)
    
    if st.session_state.symbol == "BTC":
        sent_count_data = pd.read_excel('btc.xlsx')
    elif st.session_state.symbol == "ETH":
        sent_count_data = pd.read_excel('eth.xlsx')
    else:
        sent_count_data = pd.read_excel('sol.xlsx')
        
    sent_count_AV = sent_count_data[['AV_sentiment_category_Strong Positive',
                                     'AV_sentiment_category_Moderate Positive',
                                     'AV_sentiment_category_Neutral',
                                     'AV_sentiment_category_Moderate Negative',
                                     'AV_sentiment_category_Strong Negative']]
    sent_count_AV.rename(columns={'AV_sentiment_category_Strong Positive': 'Strong Positive',
                                  'AV_sentiment_category_Moderate Positive': 'Moderate Positive',
                                  'AV_sentiment_category_Neutral': 'Neutral',
                                  'AV_sentiment_category_Moderate Negative': 'Moderate Negative',
                                  'AV_sentiment_category_Strong Negative': 'Strong Negative'}, inplace=True)
    sent_count_TB = sent_count_data[['TB_sentiment_category_Strong Positive',
                                     'TB_sentiment_category_Moderate Positive',
                                     'TB_sentiment_category_Neutral',
                                     'TB_sentiment_category_Moderate Negative',
                                     'TB_sentiment_category_Strong Negative']]
    sent_count_TB.rename(columns={'TB_sentiment_category_Strong Positive': 'Strong Positive',
                                  'TB_sentiment_category_Moderate Positive': 'Moderate Positive',
                                  'TB_sentiment_category_Neutral': 'Neutral',
                                  'TB_sentiment_category_Moderate Negative': 'Moderate Negative',
                                  'TB_sentiment_category_Strong Negative': 'Strong Negative'}, inplace=True)
    sent_count_AV = sent_count_AV.sum(axis=0)
    sent_count_TB = sent_count_TB.sum(axis=0)
    sentiment_counts_AV = sent_count_AV.reset_index()
    sentiment_counts_TB = sent_count_TB.reset_index()
    sentiment_counts_AV.columns = ['sentiment', 'count']
    sentiment_counts_TB.columns = ['sentiment', 'count']
    max_count_AV = sentiment_counts_AV.loc[sentiment_counts_AV['count'].idxmax(), 'sentiment']
    max_count_TB = sentiment_counts_TB.loc[sentiment_counts_TB['count'].idxmax(), 'sentiment']
    
    with chart_1:
        av_title = f"<h4 style='text-align: left; font-size: 0.9rem; font-weight: 500; margin-top: -15px; color: {text_dark};'>Alpha Vantage Sentiment Score</h4>"
        st.markdown(av_title, unsafe_allow_html=True)

        AV_chart = alt.Chart(sentiment_counts_AV).mark_bar(
            opacity=0.7,
            cornerRadiusBottomRight=5,
            cornerRadiusTopRight=5,
            color=alt.Gradient(
                gradient='linear',
                stops=[
                    alt.GradientStop(color=f'{black_dark}', offset=0),
                    alt.GradientStop(color=f'{black_light}', offset=1)
                ],
                x1=0,
                x2=1,
                y1=0,
                y2=0)
        ).encode(
            x=alt.X('count:Q', axis=alt.Axis(grid=True, gridColor=f'{text_dark}')),
            y=alt.Y('sentiment:O', title=None, sort=['Strong Positive', 'Moderate Positive', 'Neutral', 'Moderate Negative', 'Strong Negative']),
            tooltip=[
                alt.Tooltip("count:Q", title="Count"),
                alt.Tooltip("sentiment:O", title="Category")]
        ).properties(
            height=300,
            width='container'
        )

        highlighted_bar_AV = alt.Chart(sentiment_counts_AV).mark_bar(
            cornerRadiusBottomRight=5,
            cornerRadiusTopRight=5,
            color=alt.Gradient(
                gradient='linear',
                stops=[
                    alt.GradientStop(color=f'{black_dark}', offset=0),
                    alt.GradientStop(color='#4a6382', offset=1)
                ],
                x1=0,
                x2=1,
                y1=0,
                y2=0)
        ).encode(
            x=alt.X('count:Q', axis=alt.Axis(grid=True, gridColor=f'{text_dark}')),
            y=alt.Y('sentiment:O', title=None, sort=['Strong Positive', 'Moderate Positive', 'Neutral', 'Moderate Negative', 'Strong Negative']),
            tooltip=[
                alt.Tooltip("count:Q", title="Count"),
                alt.Tooltip("sentiment:O", title="Category")]
        ).transform_filter(
            alt.datum.sentiment == max_count_AV
        ).properties(
            height=300,
            width='container'
        )
        
        final_AV_chart = alt.layer(AV_chart, highlighted_bar_AV).configure_axis(
            labels=False,
            ticks=False,
            title=None,
            offset=0,
            gridWidth=0.2
        ).configure_legend(
            labelFontSize=0,
            symbolSize=0,
            title=None,
            offset=0
        ).configure_view(
            step=0
        )

        st.altair_chart(final_AV_chart, use_container_width=True)
        
        # TOTAL SENTIMENT COUNT (AV)
        total_sentiment_count_AV = f"""
        <div style='margin-top: -30px; margin-bottom: 25px;'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='text-align: left; font-size: 1rem; font-weight: 500; color: {text_dark};'>Strong Positive Count</span>
                <span style='text-align: right; font-size: 1rem; font-weight: 500;'>{sentiment_counts_AV[sentiment_counts_AV['sentiment'] == 'Strong Positive']['count'].iloc[0]}</span>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='text-align: left; font-size: 1rem; font-weight: 500; color: {text_dark};'>Moderate Positive Count</span>
                <span style='text-align: right; font-size: 1rem; font-weight: 500;'>{sentiment_counts_AV[sentiment_counts_AV['sentiment'] == 'Moderate Positive']['count'].iloc[0]}</span>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='text-align: left; font-size: 1rem; font-weight: 500; color: {text_dark};'>Neutral Count</span>
                <span style='text-align: right; font-size: 1rem; font-weight: 500;'>{sentiment_counts_AV[sentiment_counts_AV['sentiment'] == 'Neutral']['count'].iloc[0]}</span>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='text-align: left; font-size: 1rem; font-weight: 500; color: {text_dark};'>Moderate Negative Count</span>
                <span style='text-align: right; font-size: 1rem; font-weight: 500;'>{sentiment_counts_AV[sentiment_counts_AV['sentiment'] == 'Moderate Negative']['count'].iloc[0]}</span>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='text-align: left; font-size: 1rem; font-weight: 500; color: {text_dark};'>Strong Negative Count</span>
                <span style='text-align: right; font-size: 1rem; font-weight: 500;'>{sentiment_counts_AV[sentiment_counts_AV['sentiment'] == 'Strong Negative']['count'].iloc[0]}</span>
            </div>
        </div>
        """
        st.markdown(total_sentiment_count_AV, unsafe_allow_html=True)

    with chart_2:
        tb_title = f"<h4 style='text-align: left; font-size: 0.9rem; font-weight: 500; margin-top: -15px; color: {text_dark};'>TextBlob Sentiment Score</h4>"
        st.markdown(tb_title, unsafe_allow_html=True)
        
        TB_chart = alt.Chart(sentiment_counts_TB).mark_bar(
            opacity=0.7,
            cornerRadiusBottomRight=5,
            cornerRadiusTopRight=5,
            color=alt.Gradient(
                gradient='linear',
                stops=[
                    alt.GradientStop(color=f'{black_dark}', offset=0),
                    alt.GradientStop(color=f'{black_light}', offset=1)
                ],
                x1=0,
                x2=1,
                y1=0,
                y2=0)
        ).encode(
            x=alt.X('count:Q', axis=alt.Axis(grid=True, gridColor=f'{text_dark}')),
            y=alt.Y('sentiment:O', title=None, sort=['Strong Positive', 'Moderate Positive', 'Neutral', 'Moderate Negative', 'Strong Negative']),
            tooltip=[
                alt.Tooltip("count:Q", title="Count"),
                alt.Tooltip("sentiment:O", title="Category")]
        ).properties(
            height=300,
            width='container'
        )

        highlighted_bar_TB = alt.Chart(sentiment_counts_TB).mark_bar(
            cornerRadiusBottomRight=5,
            cornerRadiusTopRight=5,
            color=alt.Gradient(
                gradient='linear',
                stops=[
                    alt.GradientStop(color=f'{black_dark}', offset=0),
                    alt.GradientStop(color='#4a6382', offset=1)
                ],
                x1=0,
                x2=1,
                y1=0,
                y2=0)
        ).encode(
            x=alt.X('count:Q', axis=alt.Axis(grid=True, gridColor=f'{text_dark}')),
            y=alt.Y('sentiment:O', title=None, sort=['Strong Positive', 'Moderate Positive', 'Neutral', 'Moderate Negative', 'Strong Negative']),
            tooltip=[
                alt.Tooltip("count:Q", title="Count"),
                alt.Tooltip("sentiment:O", title="Category")]
        ).transform_filter(
            alt.datum.sentiment == max_count_TB
        ).properties(
            height=300,
            width='container'
        )
        
        final_TB_chart = alt.layer(TB_chart, highlighted_bar_TB).configure_axis(
            labels=False,
            ticks=False,
            title=None,
            offset=0,
            gridWidth=0.2
        ).configure_legend(
            labelFontSize=0,
            symbolSize=0,
            title=None,
            offset=0
        ).configure_view(
            step=0
        )

        st.altair_chart(final_TB_chart, use_container_width=True)
        
        # TOTAL SENTIMENT COUNT (TB)
        total_sentiment_count_TB = f"""
        <div style='margin-top: -30px; margin-bottom: 25px;'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='text-align: left; font-size: 1rem; font-weight: 500; color: {text_dark};'>Strong Positive Count</span>
                <span style='text-align: right; font-size: 1rem; font-weight: 500;'>{sentiment_counts_TB[sentiment_counts_TB['sentiment'] == 'Strong Positive']['count'].iloc[0]}</span>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='text-align: left; font-size: 1rem; font-weight: 500; color: {text_dark};'>Moderate Positive Count</span>
                <span style='text-align: right; font-size: 1rem; font-weight: 500;'>{sentiment_counts_TB[sentiment_counts_TB['sentiment'] == 'Moderate Positive']['count'].iloc[0]}</span>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='text-align: left; font-size: 1rem; font-weight: 500; color: {text_dark};'>Neutral Count</span>
                <span style='text-align: right; font-size: 1rem; font-weight: 500;'>{sentiment_counts_TB[sentiment_counts_TB['sentiment'] == 'Neutral']['count'].iloc[0]}</span>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='text-align: left; font-size: 1rem; font-weight: 500; color: {text_dark};'>Moderate Negative Count</span>
                <span style='text-align: right; font-size: 1rem; font-weight: 500;'>{sentiment_counts_TB[sentiment_counts_TB['sentiment'] == 'Moderate Negative']['count'].iloc[0]}</span>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='text-align: left; font-size: 1rem; font-weight: 500; color: {text_dark};'>Strong Negative Count</span>
                <span style='text-align: right; font-size: 1rem; font-weight: 500;'>{sentiment_counts_TB[sentiment_counts_TB['sentiment'] == 'Strong Negative']['count'].iloc[0]}</span>
            </div>
        </div>
        """
        st.markdown(total_sentiment_count_TB, unsafe_allow_html=True)
        
with news_section:
    # NEWS STATISTIC
    news_stat_title = f"<h4 style='text-align: left; font-size: 1rem; font-weight: 600; margin-top: -10px; color: {text_light};'>NEWS STATISTIC</h4>"
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
            <span style='text-align: left; font-size: 1rem; font-weight: 500; color: {text_dark};'>Monthly News Count</span>
            <span style='text-align: right; font-size: 1rem; font-weight: 500;'>{current_month_news_count}</span>
        </div>
        """
    st.markdown(news_count_m, unsafe_allow_html=True)
    
    current_year_news = news_df[news_df['date'].dt.year == current_year]
    current_year_news_count = current_year_news.shape[0]
    news_count_y = f"""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;'>
            <span style='text-align: left; font-size: 1rem; font-weight: 500; color: {text_dark};'>Annual News Count</span>
            <span style='text-align: right; font-size: 1rem; font-weight: 500;'>{current_year_news_count}</span>
        </div>
        """
    st.markdown(news_count_y, unsafe_allow_html=True)
    
    top_news_source_name = news_df['source'].value_counts().idxmax()
    top_news_source = f"""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;'>
            <span style='text-align: left; font-size: 1rem; font-weight: 500; color: {text_dark};'>Top News Source</span>
            <span style='text-align: right; font-size: 1rem; font-weight: 500;'>{top_news_source_name}</span>
        </div>
        """
    st.markdown(top_news_source, unsafe_allow_html=True)
    
    # LATEST NEWS
    latest_news_title = f"<h4 style='text-align: left; font-size: 1rem; font-weight: 600; margin-top: -10px; color: {text_light};'>LATEST NEWS</h4>"
    st.markdown(latest_news_title, unsafe_allow_html=True)
    news_df = st.session_state.news
    news_1 = f"""
    <a class='news-card' target='_blank' href='{news_df["url"].iloc[-1]}'>
        <span class='title'>{news_df["title"].iloc[-1].title()}</span>
        <span class='summary'>{news_df["summary"].iloc[-1]}</span>
        <div class='meta-info'>
            <span>Source: {news_df["source"].iloc[-1]}</span>
            <span style='color: {categorize_score(news_df["sentiment"].iloc[-1], color=True)};'>{categorize_score(news_df["sentiment"].iloc[-1])}</span>
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
            <span style='color: {categorize_score(news_df["sentiment"].iloc[-2], color=True)};'>{categorize_score(news_df["sentiment"].iloc[-2])}</span>
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
            <span style='color: {categorize_score(news_df["sentiment"].iloc[-3], color=True)};'>{categorize_score(news_df["sentiment"].iloc[-3])}</span>
        </div>
    </a>
    """
    st.markdown(news_3, unsafe_allow_html=True)
    
    # ANNUAL SENTIMENT HEATMAP
    heatmap_title = f"<h4 style='text-align: left; font-size: 1rem; font-weight: 600; margin-top: -10px; color: {text_light};'>ANNUAL SENTIMENT HEATMAP</h4>"
    st.markdown(heatmap_title, unsafe_allow_html=True)
    
    heatmap_df = st.session_state.news
    heatmap_df = heatmap_df.copy()

    heatmap_df['date'] = pd.to_datetime(heatmap_df['date'])
    daily_sentiment = heatmap_df.groupby(heatmap_df['date'].dt.date).agg({'sentiment': 'mean'}).reset_index()
    daily_sentiment['date'] = pd.to_datetime(daily_sentiment['date'])

    heatmap = alt.Chart(daily_sentiment).mark_rect().encode(
        alt.X("date(date):O").axis(format="%e", labelAngle=0, title=None),
        alt.Y("month(date):O").axis(title=None),
        alt.Color("sentiment:Q", title="Sentiment Score", scale=alt.Scale(scheme="viridis"), legend=alt.Legend(orient="bottom", labelAlign="center", title=None, padding=0, symbolSize=150)),
        tooltip=[
            alt.Tooltip("date(date):T", title="Date"),
            alt.Tooltip("sentiment:Q", title="Sentiment Score")]
    ).configure_view(
        width='container', 
        step=13,
        strokeWidth=0
    ).configure_axis(
        domain=False,
        labelColor=f'{text_dark}',
        tickColor=f'{text_dark}',
        offset=0,
        tickWidth=0.2
    )

    st.altair_chart(heatmap, use_container_width=True)

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
