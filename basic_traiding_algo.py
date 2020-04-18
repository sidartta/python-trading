# Module & Libraries Import
from datetime import date, timedelta
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix

import base_algo_trade as bat

# Variables instantiation
yrs = 10
start_date = date.today() - timedelta(365 * yrs)
end_date = date.today()
tickers = ['AAPL', 'AMZN', 'TSLA', 'SPY']

# Read Equity data
close_data, tickers = bat.get_close(tickers, start_date, end_date, r='d')

# Various line codes for basic technical analysis
stock_observed = 'SPY'
pct_chg = pd.DataFrame()
for x in tickers:
    pct_chg[x] = close_data[x].pct_change(fill_method='ffill')
pct_chg_log = np.log(pct_chg)
cum_return = (1 + pct_chg_log).cumprod()

# Basic stocks plots

fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(12, 6))
fig.subplots_adjust(hspace=1)
fig.suptitle('Stock Prices Evolution', y=0.04)

for axes, tick in zip(ax.flatten(), tickers):
    SMA_50 = close_data[tick].rolling(window=50).mean()
    SMA_150 = close_data[tick].rolling(window=150).mean()
    axes.plot(close_data[tick],
              color='black',
              lw=1,
              ls='-',
              label='Close price')
    axes.plot(SMA_50,
              lw=1,
              color='blue',
              ls='-',
              label='SMA 50')
    axes.plot(SMA_150,
              lw=1,
              color='red',
              ls='-',
              label='SMA 150')
    axes.set_xlabel('Year')
    axes.set_ylabel('Price (USD)')
    axes.legend()
    fig.autofmt_xdate()

# pct_chg.hist(bins=50, sharex=True)
# scatter_matrix(pct_chg, diagonal='kde', alpha=0.1)

plt.tight_layout()
plt.show()
###################################################
