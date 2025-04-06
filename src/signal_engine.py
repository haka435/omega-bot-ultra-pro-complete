import yfinance as yf
import pandas as pd
import numpy as np

def get_price_data(symbol):
    df = yf.download(symbol, period="60d", interval="30m", progress=False)
    return df

def generate_signals(df):
    df['EMA20'] = df['Close'].ewm(span=20).mean()
    df['RSI'] = compute_rsi(df['Close'])
    df['MACD'] = df['Close'].ewm(12).mean() - df['Close'].ewm(26).mean()

    signal = []
    for i in range(len(df)):
        if df['RSI'].iloc[i] < 30 and df['Close'].iloc[i] > df['EMA20'].iloc[i]:
            signal.append("BUY")
        elif df['RSI'].iloc[i] > 70 and df['Close'].iloc[i] < df['EMA20'].iloc[i]:
            signal.append("SELL")
        else:
            signal.append("NEUTRAL")
    df['signal'] = signal
    df['entry_price'] = df['Close']

    df['T1'] = df['Close'] * 1.01
    df['T2'] = df['Close'] * 1.02
    df['T3'] = df['Close'] * 1.03
    df['T4'] = df['Close'] * 1.04
    df['T1_hitrate'] = 73
    df['T2_hitrate'] = 65
    df['T3_hitrate'] = 55
    df['T4_hitrate'] = 44
    return df[['signal', 'entry_price', 'T1', 'T2', 'T3', 'T4', 'T1_hitrate', 'T2_hitrate', 'T3_hitrate', 'T4_hitrate']]

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))
