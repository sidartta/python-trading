# Module & Libraries Import
from pandas.plotting import scatter_matrix
from pandas_datareader import data as pdr
from datetime import date
from time import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Variables instantiation
start_time = time()
start_date = date(2015, 1, 1)
tickers = ['AAPL', 'C', 'GS', 'AMZN']


# Function to get tickers data from Yahoo! Finance
def get(tickers, startdate, enddate=None, r='D'):
    def stock_data(ticker):
        tick = pdr.get_data_yahoo(ticker, start=startdate, end=enddate)
        if r is not None:
            tick = tick.resample(rule=r, axis=0, closed='right').mean()
        return tick.dropna()

    datas = map(stock_data, tickers)
    return pd.concat(datas, keys=tickers, names=['Ticker', 'Date'])


# Read Equity data
all_data = get(tickers, start_date)

# Save Initial data to an excel file
# eq_df.to_excel("stock_data.xlsx", sheet_name='Initial Data')

# Various line codes for basic technical analysis
pct_chg = pd.DataFrame()
for x in tickers:
    pct_chg[x] = all_data.loc[(x, 'Close')].pct_change(fill_method='ffill')
pct_chg_log = np.log(pct_chg)
cum_return = (1 + pct_chg).cumprod()

# Basic stocks plots
pct_chg.hist(bins=50, sharex=True)
scatter_matrix(pct_chg, diagonal='kde', alpha=0.1)
plt.show()
###################################################
print("--- %s seconds ---" % (time() - start_time))
