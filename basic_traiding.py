# ------------------------------------------------------ #
# Module & Libraries Import
# ------------------------------------------------------ #
from datetime import date, timedelta
import matplotlib.dates as m_dates
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
import get_stock_data as gsd
from tech_indicators import macd

# ------------------------------------------------------ #
# Variables instantiation
# ------------------------------------------------------ #
yrs = 5
start_date = date.today() - timedelta(365 * yrs)
end_date = date.today()
tickers = ['AAPL', 'AMZN']
years = m_dates.YearLocator()
months = m_dates.MonthLocator()
years_fmt = m_dates.DateFormatter('%Y')

# ------------------------------------------------------ #
# Read Equity data
# ------------------------------------------------------ #
close_data, tickers, volume_data = gsd.get_stock_data(tickers,
                                                      start_date,
                                                      end_date,
                                                      r='d')

# ------------------------------------------------------ #
# Various line codes for basic technical analysis
# ------------------------------------------------------ #
pct_chg = pd.DataFrame((close_data[x].pct_change(fill_method='ffill') for x in tickers)).T
pct_chg_log = np.log(pct_chg)
cum_return = (1 + pct_chg_log).cumprod()
stock_under_study = tickers[0]

# MACD Calculation
macd_df = macd(close_data[stock_under_study])

# ------------------------------------------------------ #
# Basic stocks plots
# ------------------------------------------------------ #
plt.style.use('ggplot')

# Multi-plot of time-series with SMAs
fig1, ax1 = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
fig1.subplots_adjust(hspace=1)

for axes, tick in zip(ax1.flatten(), tickers):
    SMA_50 = close_data[tick].rolling(window=50).mean()
    SMA_150 = close_data[tick].rolling(window=150).mean()
    axes.plot(close_data[tick], color='black', lw=1, ls='-', label='Close price')
    axes.plot(SMA_50, lw=1, color='blue', ls='-', label='SMA 50')
    axes.plot(SMA_150, lw=1, color='red', ls='-', label='SMA 150')
    axes.set_xlabel('Year')
    axes.set_ylabel('Price (USD)')
    axes.legend()
    axes.set_title(tick)
    axes.xaxis.set_major_locator(years)
    axes.xaxis.set_major_formatter(years_fmt)
    axes.xaxis.set_minor_locator(months)
    axes.set_xlim(np.datetime64(close_data.index[0], 'Y'),
                  np.datetime64(close_data.index[-1], 'Y') + np.timedelta64(1, 'Y'))
    axes.grid(True)
    fig1.autofmt_xdate()

# MACD plot + time-series Data
fig2 = plt.figure(figsize=(12, 10))
fig2.autofmt_xdate()

gs = plt.GridSpec(3, 1, height_ratios=[3, 1, 1], hspace=.0)
ax = fig2.add_subplot(gs[0, :])
others_ax = [fig2.add_subplot(gs[i, :], sharex=ax) for i in range(1, 3)]
all_ax = [ax] + others_ax

for ax in all_ax[:-1]:
    plt.setp(ax.get_xticklabels(), visible=False)

all_ax[0].plot(close_data[stock_under_study], color='black', lw=.5, ls='-')
all_ax[0].set_ylabel('Close Price (USD)')
all_ax[0].set_title(stock_under_study)

all_ax[1].bar(x=volume_data.index, height=volume_data[stock_under_study])
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
###################################################
