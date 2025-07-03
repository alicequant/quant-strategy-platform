import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "watchdog"

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from backtest.runner import run_backtest
import matplotlib.pyplot as plt
from data.yahoo_data import get_data, get_pair_data
from strategies.pairs_trading import test_cointegration, generate_zscore_signals


st.set_page_config(page_title="Quant Strategy Platform", layout="wide")
st.title("📈 US Stock Quant Strategy Platform - SMA & Pairs Trading")

strategy = st.selectbox("Select Strategy", ["SMA Crossover", "Pairs Trading", "LSTM Prediction"])

if strategy == "SMA Crossover":
    symbol = st.text_input("Stock Symbol", "AAPL")
    sma1 = st.slider("Short-Term SMA", 5, 50, 20)
    sma2 = st.slider("Long-Term SMA", 10, 200, 50)

    if st.button("Run Backtest"):
        st.info(f"Running backtest for: {symbol}, SMA({sma1}, {sma2})")

        try:
            df, buy_signals, sell_signals = run_backtest(symbol=symbol, sma1=sma1, sma2=sma2)

            # 自定义绘图
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(df.index, df['Close'], label='Close Price')

            # Buy signals: green arrow ↑
            for date, price in buy_signals:
                ax.scatter(date, price, marker='^', color='green', label='Buy', zorder=5)

            # Sell signals: red arrow ↓
            for date, price in sell_signals:
                ax.scatter(date, price, marker='v', color='red', label='Sell', zorder=5)

            # 避免图例重复
            handles, labels = ax.get_legend_handles_labels()
            by_label = dict(zip(labels, handles))
            ax.legend(by_label.values(), by_label.keys())

            ax.set_title(f'{symbol} Close Price + Trade Signals')
            st.pyplot(fig)

        except Exception as e:
            st.error(f"运行出错：{e}")

elif strategy == "Pairs Trading":
    s1 = st.text_input("Stock 1", "KO")
    s2 = st.text_input("Stock 2", "PEP")

    if st.button("Run Pairs Trading Test"):
        df = get_pair_data(s1, s2)
        pval, spread = test_cointegration(df)

        if pval < 0.05:
            st.success(f"Cointegration test passed (p={pval:.4f}) ✅")
            signals = generate_zscore_signals(spread)

            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(signals.index, signals['z'], label="Z-Score")
            ax.axhline(1, color='red', linestyle='--')
            ax.axhline(-1, color='green', linestyle='--')
            ax.axhline(0, color='black', linestyle=':')
            ax.legend()
            st.pyplot(fig)
        else:
            st.warning(f"Cointegration test failed (p={pval:.4f}) ❌")
            
elif strategy == "LSTM Prediction":
    symbol = st.text_input("Stock Symbol", "AAPL")

    if st.button("Run LSTM Forecast"):
        import torch
        import sys
        import asyncio
        if sys.platform == "darwin":
            try:
                asyncio.set_event_loop(asyncio.new_event_loop())
            except RuntimeError:
                pass
        from strategies.lstm_strategy import train_and_predict
        df = get_data(symbol)
        result = train_and_predict(df)

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(result.index, result['Actual Close'], label='Actual')
        ax.plot(result.index, result['Predicted Close'], label='Predicted')
        ax.set_title(f'{symbol} - LSTM Forecast')
        ax.legend()
        st.pyplot(fig)
