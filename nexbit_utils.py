import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE

def predict(train, test, predictors, model):
    model.fit(train[predictors], train["target"])
    preds = model.predict_proba(test[predictors])[:,1]
    conf = pd.Series(preds, index=test.index, name="confidence")
    binary_preds = (preds >= 0.6).astype(int)
    binary_preds = pd.Series(binary_preds, index=test.index, name="prediction")
    combined = pd.concat([test["target"], binary_preds, conf], axis=1)
    return combined

def backtest(data, model, predictors):
    all_predictions = []
    for i in range(365, data.shape[0], 1):
        train = data.iloc[0:i].copy()
        test = data.iloc[i:(i+1)].copy()
        predictions = predict(train, test, predictors, model)
        all_predictions.append(predictions)
    combined = pd.concat(all_predictions)
    return combined

def feature_selection(data, predictors, target_column, threshold=0.8):
    data = data[predictors + [target_column]]
    corr_matrix = data.corr()
    target_corr = corr_matrix[target_column].drop(target_column)
    target_corr_sorted = target_corr.abs().sort_values(ascending=False)
    selected_features = list(target_corr_sorted.index)
    to_remove = set()
    for i in range(len(selected_features)):
        if selected_features[i] in to_remove:
            continue
        for j in range(i + 1, len(selected_features)):
            if abs(corr_matrix[selected_features[i]][selected_features[j]]) > threshold:
                to_remove.add(selected_features[j])
    selected_features = [feature for feature in selected_features if feature not in to_remove]
    return selected_features

def add_features(data):
    lags = [1, 2, 3]
    for lag in lags:
        data[f'close_price_lag_{lag}'] = data['close_price'].shift(lag)
        data[f'AV_sentiment_lag_{lag}'] = data['AV_average_sentiment'].shift(lag)
        data[f'TB_sentiment_lag_{lag}'] = data['TB_average_sentiment'].shift(lag)
    data['date'] = pd.to_datetime(data.index)
    data['day_of_week'] = data['date'].dt.dayofweek
    data['month'] = data['date'].dt.month
    data['is_weekend'] = data['day_of_week'].isin([5, 6]).astype(int)
    data_copy = data.drop(columns=['date'])
    horizons = [4,13,26,52,208]
    for horizon in horizons:
      rolling_averages = data_copy.rolling(horizon).mean()
      ratio_column = f"close_ratio_{horizon}"
      data[ratio_column] = data["close_price"] / rolling_averages["close_price"]
      trend_column = f"trend_{horizon}"
      data[trend_column] = data_copy.shift(1).rolling(horizon).sum()["target"]
    data = data.dropna().reset_index(drop=True)
    data.set_index('date', inplace=True)
    scaler = MinMaxScaler()
    columns_to_scale = ['day_of_week', 'month']
    data[columns_to_scale] = data[columns_to_scale].astype(float)
    data[columns_to_scale] = scaler.fit_transform(data[columns_to_scale])

    return data

def backtest_with_oversampling(data, model, predictors):
    all_predictions = []
    smote = SMOTE(random_state=42)
    for i in range(365, data.shape[0], 1):
        train = data.iloc[0:i].copy()
        test = data.iloc[i:(i+1)].copy()
        X_train = train[predictors]
        y_train = train["target"]
        X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
        train_resampled = X_train_resampled.copy()
        train_resampled["target"] = y_train_resampled
        predictions = predict(train_resampled, test, predictors, model)
        all_predictions.append(predictions)
    combined = pd.concat(all_predictions)
    return combined

# Generating Predictions for Bitcoin
def predict_btc(data):
    knn_model = KNeighborsClassifier(n_neighbors=10)
    TB_new_predictors = add_features(data).drop(['target', 'AV_average_sentiment', 'AV_sentiment_category_Strong Negative',
                                                 'AV_sentiment_category_Strong Positive', 'AV_sentiment_category_Neutral',
                                                 'AV_sentiment_category_Moderate Negative', 'AV_sentiment_category_Moderate Positive',
                                                 'AV_sentiment_lag_1', 'AV_sentiment_lag_2', 'AV_sentiment_lag_3'], axis=1).columns.to_list()
    data = add_features(data)
    preds = backtest_with_oversampling(data, knn_model, feature_selection(data, TB_new_predictors, 'target'))
    accuracy = accuracy_score(preds["target"], preds["prediction"])
    if preds['prediction'].iloc[-1] > 0:
        prediction = 1
        confidence = round(preds['confidence'].iloc[-1] * 100)
    else:
        prediction = 0
        confidence = 100 - round(preds['confidence'].iloc[-1] * 100)
    return prediction, accuracy, confidence

# Generating Predictions for Ethereum
def predict_eth(data):
    xgb_model = XGBClassifier(random_state=42, learning_rate=.1, n_estimators=200)
    AV_predictors = final_df_btc.drop(['target', 'TB_average_sentiment', 'TB_sentiment_category_Strong Negative',
                                       'TB_sentiment_category_Strong Positive', 'TB_sentiment_category_Neutral',
                                       'TB_sentiment_category_Moderate Negative', 'TB_sentiment_category_Moderate Positive'], axis=1).columns.to_list()
    preds = backtest(data, xgb_model, feature_selection(data, AV_predictors, 'target'))
    accuracy = accuracy_score(preds["target"], preds["prediction"])
    if preds['prediction'].iloc[-1] > 0:
        prediction = 1
        confidence = round(preds['confidence'].iloc[-1] * 100)
    else:
        prediction = 0
        confidence = 100 - round(preds['confidence'].iloc[-1] * 100)
    return prediction, accuracy, confidence

# Generating Predictions for Solana
def predict_sol(data):
    knn_model = KNeighborsClassifier(n_neighbors=10)
    AV_new_predictors = add_features(data).drop(['target', 'TB_average_sentiment', 'TB_sentiment_category_Strong Negative',
                                                 'TB_sentiment_category_Strong Positive', 'TB_sentiment_category_Neutral',
                                                 'TB_sentiment_category_Moderate Negative', 'TB_sentiment_category_Moderate Positive',
                                                 'TB_sentiment_lag_1', 'TB_sentiment_lag_2', 'TB_sentiment_lag_3'], axis=1).columns.to_list()
    data = add_features(data)
    preds = backtest_with_oversampling(data, knn_model, feature_selection(data, AV_new_predictors, 'target'))
    accuracy = accuracy_score(preds["target"], preds["prediction"])
    if preds['prediction'].iloc[-1] > 0:
        prediction = 1
        confidence = round(preds['confidence'].iloc[-1] * 100)
    else:
        prediction = 0
        confidence = 100 - round(preds['confidence'].iloc[-1] * 100)
    return prediction, accuracy, confidence
