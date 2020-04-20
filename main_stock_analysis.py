# ------------------------------------------------------ #
# Module & Libraries Import
# ------------------------------------------------------ #
from datetime import date, timedelta
import matplotlib.dates as m_dates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tech_indicators import macd
from yahoo_fin_scrap import most_active_sp500
import stock

# ------------------------------------------------------ #
# Variables initialization
# ------------------------------------------------------ #
yrs = 5
start_date = date.today() - timedelta(365 * yrs)
end_date = date.today()
years = m_dates.YearLocator()
months = m_dates.MonthLocator()
years_fmt = m_dates.DateFormatter('%Y')

# ------------------------------------------------------ #
# Get tickers of top traded stocks in the S&P500
# ------------------------------------------------------ #
tickers = most_active_sp500()
# ------------------------------------------------------ #
# Instantiate stock objects
# ------------------------------------------------------ #
my_stocks = stock.Stock(tickers[0:2], start_date, end_date)

# ------------------------------------------------------ #
# Get data of Stocks
# ------------------------------------------------------ #
stocks_data = my_stocks.get_data()

# Isolate most traded stock
stock_1 = stocks_data.iloc[stocks_data.index.get_level_values('Ticker') == tickers[0]]
stock_1.reset_index(level=0, drop=True, inplace=True)

# ------------------------------------------------------ #
# Various line codes for basic technical analysis
# ------------------------------------------------------ #
pct_chg = stock_1['Close'].pct_change(fill_method='ffill')
pct_chg_log = np.log(pct_chg)
cum_return = (1 + pct_chg_log).cumprod()

# MACD Calculation
macd_df = macd(stock_1['Close'])

# ------------------------------------------------------ #
# Basic stocks plots
# ------------------------------------------------------ #
plt.style.use('seaborn')

# MACD plot + time-series Data
fig1 = plt.figure(figsize=(12, 6))
fig1.autofmt_xdate()

gs = plt.GridSpec(3, 1, height_ratios=[4, 1, 1], hspace=.05)
ax = fig1.add_subplot(gs[0, :])
others_ax = [fig1.add_subplot(gs[i, :], sharex=ax) for i in range(1, 3)]
all_ax = [ax] + others_ax

for ax in all_ax[:-1]:
    plt.setp(ax.get_xticklabels(), visible=False)

all_ax[0].plot(stock_1['Close'], color='black', lw=.5, ls='-')
all_ax[0].set_ylabel('Close Price (USD)')
all_ax[0].set_title(tickers[0])

all_ax[1].bar(x=stock_1.index, height=stock_1['Volume'])
all_ax[1].set_ylabel('Volume')
y_ticks = all_ax[1].yaxis.get_major_ticks()
y_ticks[-1].label1.set_visible(False)

all_ax[2].plot(macd_df.index, macd_df.iloc[:, 2], label='Slow')
all_ax[2].plot(macd_df.index, macd_df.iloc[:, 3], label='Fast')
all_ax[2].bar(x=macd_df.index, height=macd_df['MACD'] - macd_df['Signal'])
all_ax[2].set_ylabel('MACD')
all_ax[2].legend()
all_ax[2].grid(True)
all_ax[2].set_xlabel('Year')
all_ax[2].xaxis.set_major_locator(years)
all_ax[2].xaxis.set_major_formatter(years_fmt)
all_ax[2].xaxis.set_minor_locator(months)
y_ticks = all_ax[2].yaxis.get_major_ticks()
y_ticks[-1].label1.set_visible(False)

# Plots display
plt.show()
