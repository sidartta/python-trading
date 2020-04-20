# ------------------------------------------------------ #
# Module & Libraries Import
# ------------------------------------------------------ #
import pandas as pd
from pandas_datareader import data as pdr


# ------------------------------------------------------ #
# Function to get stocks data from Yahoo! Finance
# ------------------------------------------------------ #
def from_yahoo(tick, start_date, end_date=None, r='d'):
    if type(tick) != list:
        tick = list(tick)

    def stock_data(tk):
        tentative = 0
        while tentative < 5:
            try:
                return pdr.get_data_yahoo(tk, start=start_date, end=end_date, interval=r)
            except:
                print('Failed to retrieve {} stock data... retrying'.format(tk))
                tentative = tentative + 1
                continue

    datas = map(stock_data, tick)
    return pd.concat(datas, keys=tick, names=['Ticker', 'Date'])
