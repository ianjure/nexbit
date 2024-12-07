import pandas as pd
import re
import nltk
nltk.download('stopwords')
import contractions
from nltk.corpus import stopwords
from textblob import TextBlob
from sklearn.preprocessing import MinMaxScaler

def AV_daily_sentiment(data, crypto_id):
    date_range = pd.date_range(start="2022-03-02", end="2024-10-31")
    date_series = pd.DataFrame({"date": date_range})
    filtered_news = data[data["crypto_id"] == crypto_id]

    daily_aggregation = filtered_news.groupby("date")["sentiment"].mean().reset_index()
    daily_aggregation.rename(columns={"sentiment": "AV_average_sentiment"}, inplace=True)
    daily_aggregation["date"] = pd.to_datetime(daily_aggregation["date"])

    result = pd.merge(date_series, daily_aggregation, on="date", how="left")
    result["AV_average_sentiment"] = result["AV_average_sentiment"].fillna(0.0)
    result = result.sort_values(by="date")

    def classify_sentiment(score):
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

    result['AV_sentiment_category'] = result['AV_average_sentiment'].apply(classify_sentiment)
    return result

def TB_daily_sentiment(data, crypto_id):
    date_range = pd.date_range(start="2022-03-02", end="2024-10-31")
    date_series = pd.DataFrame({"date": date_range})
    filtered_news = data[data["crypto_id"] == crypto_id].copy()

    filtered_news["date"] = pd.to_datetime(filtered_news["date"])
    result = pd.merge(date_series, filtered_news[["date", "summary"]], on="date", how="left")
    result["summary"] = result["summary"].fillna("None")
    result = result.sort_values(by="date")

    def clean_calculate(df):
        df['summary'] = df['summary'].apply(lambda x: x.lower() if x.lower() != 'none' else None)
        df['summary'] = df['summary'].apply(lambda x: x.lower() if x is not None else x)
        stop_words = set(stopwords.words('english'))
        df['summary'] = df['summary'].apply(lambda x: ' '.join([word for word in x.split(' ') if word not in stop_words]) if x is not None else x)
        df['summary'] = df['summary'].apply(lambda x: contractions.fix(x) if x is not None else x)
        df['summary'] = df['summary'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii') if x is not None else x)
        df['summary'] = df['summary'].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', x) if x is not None else x)
        df['sentiment'] = df['summary'].apply(lambda x: TextBlob(x).sentiment.polarity if x is not None else 0)
        df['TB_average_sentiment'] = df.groupby('date')['sentiment'].transform('mean')
        df['TB_average_sentiment'] = df['TB_average_sentiment'].fillna(0)
        return df

    df = clean_calculate(result)

    def classify_sentiment(score):
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

    df['TB_sentiment_category'] = df['TB_average_sentiment'].apply(classify_sentiment)
    df = df[['date', 'TB_average_sentiment', 'TB_sentiment_category']]
    df = df.drop_duplicates(subset=['date']).reset_index(drop=True)
    return df

def calculate_PR_TI(data, crypto_id):
    filtered_price = data[data["crypto_id"] == crypto_id]
    df = filtered_price[["date", "open_price", "close_price", "high_price", "low_price"]].sort_values(by="date")
    df["date"] = pd.to_datetime(df["date"])

    df['price_range'] = df['high_price'] - df['low_price']

    df['SMA_5'] = df['close_price'].rolling(window=5).mean()
    df['SMA_10'] = df['close_price'].rolling(window=10).mean()
    df['SMA_25'] = df['close_price'].rolling(window=25).mean()
    df['SMA_50'] = df['close_price'].rolling(window=50).mean()

    df['price_change'] = df['close_price'].diff()
    df['gain'] = df['price_change'].apply(lambda x: x if x > 0 else 0)
    df['loss'] = df['price_change'].apply(lambda x: -x if x < 0 else 0)
    df['avg_gain'] = df['gain'].rolling(window=7, min_periods=1).mean()
    df['avg_loss'] = df['loss'].rolling(window=7, min_periods=1).mean()
    df['rs'] = df['avg_gain'] / df['avg_loss']
    df['RSI'] = 100 - (100 / (1 + df['rs']))

    df = df[['date', 'price_range', 'SMA_5', 'SMA_10', 'SMA_25', 'SMA_50', 'RSI']]
    return df

def create_target(data, crypto_id):
    filtered_price = data[data["crypto_id"] == crypto_id].copy()
    filtered_price = filtered_price.sort_values(by="date")
    filtered_price["date"] = pd.to_datetime(filtered_price["date"])
    filtered_price["next_day"] = filtered_price["close_price"].shift(-1)
    filtered_price["target"] = (filtered_price["next_day"] > filtered_price["close_price"]).astype(int)
    result = filtered_price[["date", "close_price", "next_day", "target"]]
    return result

def final_transform(news_data, price_data, crypto_id):
    AV_sentiment_df = AV_daily_sentiment(news_data, crypto_id)
    TB_sentiment_df = TB_daily_sentiment(news_data, crypto_id)
    PR_TI_df = calculate_PR_TI(price_data, crypto_id)
    target_df = create_target(price_data, crypto_id)
    pre_df = pd.merge(AV_sentiment_df, TB_sentiment_df, on='date')
    pre_df = pd.merge(pre_df, PR_TI_df, on='date')
    pre_df = pd.merge(pre_df, target_df, on='date')

    numerical_columns = ['AV_average_sentiment', 'TB_average_sentiment', 'price_range',
                        'SMA_5', 'SMA_10', 'SMA_25', 'SMA_50', 'RSI', 'close_price']
    categorical_columns = ['AV_sentiment_category', 'TB_sentiment_category']

    scaler = MinMaxScaler()
    pre_df[numerical_columns] = scaler.fit_transform(pre_df[numerical_columns])

    final_df = pd.get_dummies(pre_df, columns=categorical_columns, dtype=int)

    all_categories = ['Moderate Negative', 'Moderate Positive', 'Neutral', 'Strong Positive', 'Strong Negative']
    for category in all_categories:
        column_name = f'AV_sentiment_category_{category}'
        if column_name not in final_df.columns:
            final_df[column_name] = 0
        column_name = f'TB_sentiment_category_{category}'
        if column_name not in final_df.columns:
            final_df[column_name] = 0

    final_df = final_df.drop(['next_day'], axis=1)

    column_order = ['date',
                    'close_price',
                    'price_range',
                    'SMA_5',
                    'SMA_10',
                    'SMA_25',
                    'SMA_50',
                    'RSI',
                    'AV_average_sentiment',
                    'TB_average_sentiment',
                    'AV_sentiment_category_Strong Negative',
                    'AV_sentiment_category_Strong Positive',
                    'AV_sentiment_category_Neutral',
                    'AV_sentiment_category_Moderate Negative',
                    'AV_sentiment_category_Moderate Positive',
                    'TB_sentiment_category_Strong Negative',
                    'TB_sentiment_category_Strong Positive',
                    'TB_sentiment_category_Neutral',
                    'TB_sentiment_category_Moderate Negative',
                    'TB_sentiment_category_Moderate Positive',
                    'target']
    final_df = final_df[column_order]
    final_df = final_df.dropna().reset_index(drop=True)
    final_df['date'] = pd.to_datetime(final_df['date'])
    final_df.set_index('date', inplace=True)
    return final_df
