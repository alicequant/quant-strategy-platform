import pandas as pd
import yfinance as yf

def get_data(symbol='AAPL', start='2020-01-01', end='2024-01-01'):
    df = yf.download(symbol, start=start, end=end, auto_adjust=False)

    # 有时候会返回 multi-index 列，手动处理为普通 DataFrame
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    df.dropna(inplace=True)
    return df