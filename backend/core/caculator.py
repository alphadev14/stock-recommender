import pandas as pd
import ta

# 5. Tính toán các chỉ báo kỹ thuật
def calculate_indicators(df: pd.DataFrame):
    if df.empty:
        return df
    df["EMA20"] = ta.trend.EMAIndicator(df["priceclose"], window=20).ema_indicator()
    df["EMA50"] = ta.trend.EMAIndicator(df["priceclose"], window=50).ema_indicator()
    df["RSI"] = ta.momentum.RSIIndicator(df["priceclose"], window=14).rsi()
    return df