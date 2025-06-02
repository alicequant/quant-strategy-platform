# strategies/moving_average.py
import backtrader as bt

class MovingAverageStrategy(bt.Strategy):
    params = dict(sma1=20, sma2=50)

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.sma1)
        sma2 = bt.ind.SMA(period=self.p.sma2)
        self.crossover = bt.ind.CrossOver(sma1, sma2)
        self.buy_signals = []
        self.sell_signals = []

    def next(self):
        if self.crossover > 0:
            self.buy(size=1)
            self.buy_signals.append((self.datas[0].datetime.datetime(0), self.datas[0].close[0]))
        elif self.crossover < 0:
            self.sell(size=1)
            self.sell_signals.append((self.datas[0].datetime.datetime(0), self.datas[0].close[0]))