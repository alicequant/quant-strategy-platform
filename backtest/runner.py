import backtrader as bt
from data.yahoo_data import get_data
from strategies.moving_average import MovingAverageStrategy

def run_backtest(symbol='AAPL', sma1=20, sma2=50):
    cerebro = bt.Cerebro()
    strategy = cerebro.addstrategy(MovingAverageStrategy, sma1=sma1, sma2=sma2)

    df = get_data(symbol)
    data = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data)
    cerebro.broker.set_cash(100000)

    result = cerebro.run()
    strat = result[0]
    
    # 提取信号点
    buy_signals = getattr(strat, 'buy_signals', [])
    sell_signals = getattr(strat, 'sell_signals', [])

    return df, buy_signals, sell_signals