# ---------------------------------------------------------------------------- #
# Module & Libraries Import
# ---------------------------------------------------------------------------- #
import get_stock_data as gsd
import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------- #
# Create the stock class
# ---------------------------------------------------------------------------- #
class Stock:
    interval = '1d'

    def __init__(self, ticker, name, startdate, enddate):
        self.ticker = ticker
        self.name = name
        self.startdate = startdate
        self.enddate = enddate

        self.ticker_data = gsd.from_yahoo(
            self.ticker, self.startdate,
            self.enddate, Stock.interval)

        self.close = self.ticker_data['Adj Close']
        self.high = self.ticker_data['High']
        self.low = self.ticker_data['Low']
        self.volume = self.ticker_data['Volume']

    def pct_chg(self, type='standard'):
        log_chg = np.log(self.close) - np.log(self.close.shift(1))

        chg = {
            'standard': self.close.pct_change(fill_method='ffill'),
            'log': log_chg,
            'cumulative': (1 + log_chg).cumprod()
        }
        return chg[type]

    def macd(self, short_p=12, long_p=20, mean_p=9):
        macd_df = pd.DataFrame(index=self.close.index)

        macd_df['MA Fast'] = self.close.ewm(
            span=short_p, min_periods=short_p).mean()

        macd_df['MA Slow'] = self.close.ewm(
            span=long_p, min_periods=long_p).mean()

        macd_df['MACD'] = macd_df['MA Fast'] - macd_df['MA Slow']

        macd_df['Signal'] = macd_df['MACD'].ewm(
            span=mean_p, min_periods=mean_p).mean()

        return macd_df

    def moving_avg(self, wind, type='sma'):
        ma = {
            'sma': self.close.rolling(window=wind).mean(),
            'ema': self.close.ewm(span=wind, min_periods=wind).mean()
        }
        return ma[type]

    def atr(self, window=20):
        df = pd.DataFrame(index=self.ticker_data.index)
        df['H-L'] = abs(self.high - self.low)
        df['H-PC'] = abs(self.high - self.close.shift(1))
        df['L-PC'] = abs(self.low - self.close.shift(1))
        df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)
        df['ATR'] = df['TR'].rolling(window).mean()
        # df['ATR'] = df['TR'].ewm(span=n,adjust=False,min_periods=n).mean()
        df.drop(['H-L', 'H-PC', 'L-PC'], axis=1, inplace=True)
        return df
