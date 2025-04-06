import pandas as pd

def compare_strategies(symbol):
    return pd.DataFrame({
        "Strategie": ["RSI", "MACD", "Trend"],
        "Trefferquote": [72, 66, 60],
        "Avg. Return": [3.2, 2.4, 1.8]
    })
