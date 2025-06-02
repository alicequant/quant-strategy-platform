import sys
import os
sys.path.insert(0, os.path.abspath("."))  # ✅ 项目根目录（更保险）

import matplotlib
matplotlib.use('TkAgg')

from backtest.runner import run_backtest

if __name__ == "__main__":
    print("✅ 开始执行策略回测...")
    cerebro = run_backtest(symbol="AAPL", sma1=20, sma2=50)
    print("✅ 回测完成，开始绘图...")
    fig = cerebro.plot(style='candlestick', iplot=False, volume=False)[0][0]
    st.pyplot(fig)