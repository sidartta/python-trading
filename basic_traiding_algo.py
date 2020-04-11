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
tickers = ['AAPL', 'C', 'GS', 'BBD-B.TO']

# Read Equity data
all_data = bat.get(tickers, start_date, r='d')

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
