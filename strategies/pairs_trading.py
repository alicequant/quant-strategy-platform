import numpy as np
import statsmodels.api as sm
import pandas as pd

def test_cointegration(df):
    y = df.iloc[:, 0]
    x = df.iloc[:, 1]
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    spread = y - model.predict(x)
    adf_result = sm.tsa.adfuller(spread)
    return adf_result[1], spread  # 返回 p-value 和价差序列

def generate_zscore_signals(spread, entry=1.0, exit=0.2):
    zscore = (spread - spread.mean()) / spread.std()
    signals = pd.DataFrame(index=spread.index)
    signals['z'] = zscore
    signals['long'] = zscore < -entry
    signals['short'] = zscore > entry
    signals['exit'] = zscore.abs() < exit
    return signals