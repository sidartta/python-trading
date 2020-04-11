'''
# Module & Libraries Import
from datetime import date, timedelta
from time import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix
from pandas_datareader import data as pdr

# Variables instantiation
yrs = 3
start_time = time()
start_date = date.today() - timedelta(365 * yrs)
end_date = date.today()
tickers = ['AAPL', 'C', 'GS', 'BBD-B.TO']


# Function to get tickers data from Yahoo! Finance
def get(tick, startdate, enddate=None, r='d'):
    def stock_data(ticker):
        tk = pdr.get_data_yahoo(ticker, start=startdate, end=enddate, interval=r)
        return tk.dropna()

    datas = map(stock_data, tick)
    return pd.concat(datas, keys=tickers, names=['Ticker', 'Date'])


# Read Equity data
all_data = get(tickers, start_date, r='m')

# Save Initial data to an excel file
# eq_df.to_excel("stock_data.xlsx", sheet_name='Initial Data')

# Various line codes for basic technical analysis
pct_chg = pd.DataFrame()
for x in tickers:
    pct_chg[x] = all_data.loc[(x, 'Close')].pct_change(fill_method='ffill')
pct_chg_log = np.log(pct_chg)

# Basic stocks plots
pct_chg.hist(bins=50, sharex=True)
scatter_matrix(pct_chg, diagonal='kde', alpha=0.1)
plt.tight_layout()
plt.show()
###################################################
print("--- %s seconds ---" % (time() - start_time))
'''
