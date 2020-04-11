# Module & Libraries Import
import pandas as pd
from pandas_datareader import data as pdr


# Function to get tickers data from Yahoo! Finance
def get(tick, start_date, end_date=None, r='d'):
    def stock_data(ticker):
        tk = pdr.get_data_yahoo(ticker,
                                start=start_date,
                                end=end_date,
                                interval=r)
        return tk.dropna()

    datas = map(stock_data, tick)
    return pd.concat(datas, keys=tickers, names=['Ticker', 'Date'])
