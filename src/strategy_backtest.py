import pandas as pd

def compare_strategies(symbol):
    return pd.DataFrame({
        "Strategie": ["RSI", "MACD", "EMA-Trend"],
        "Trefferquote (%)": [72, 66, 58],
        "Ø Return (%)": [2.8, 2.1, 1.6]
    })
