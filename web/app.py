import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from backtest.runner import run_backtest
import matplotlib.pyplot as plt

st.set_page_config(page_title="Quant Strategy Platform", layout="wide")
st.title("📈 美股量化策略平台 - 双均线策略")

symbol = st.text_input("股票代码", "AAPL")
sma1 = st.slider("短期均线（SMA1）", 5, 50, 20)
sma2 = st.slider("长期均线（SMA2）", 10, 200, 50)

if st.button("开始回测"):
    st.info(f"开始回测：{symbol}, SMA({sma1}, {sma2})")

    try:
        df, buy_signals, sell_signals = run_backtest(symbol=symbol, sma1=sma1, sma2=sma2)

        # 自定义绘图
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df.index, df['Close'], label='收盘价')

        # 买入点：绿箭头 ↑
        for date, price in buy_signals:
            ax.scatter(date, price, marker='^', color='green', label='买入', zorder=5)

        # 卖出点：红箭头 ↓
        for date, price in sell_signals:
            ax.scatter(date, price, marker='v', color='red', label='卖出', zorder=5)

        # 避免图例重复
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys())

        ax.set_title(f'{symbol} 收盘价 + 买卖信号')
        st.pyplot(fig)

    except Exception as e:
        st.error(f"运行出错：{e}")