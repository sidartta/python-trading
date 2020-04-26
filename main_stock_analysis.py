# ---------------------------------------------------------------------------- #
# Module & Libraries Import
# ---------------------------------------------------------------------------- #
from datetime import date, timedelta
import plot_stock
from fin_data_scrap import most_active_sp500
import stock

# ---------------------------------------------------------------------------- #
# Variables initialization
# ---------------------------------------------------------------------------- #
yrs = 2
num_days = 365 * yrs
start_date = date.today() - timedelta(num_days)
end_date = date.today()
window = round(num_days / 4)

# ---------------------------------------------------------------------------- #
# Get tickers of top traded stocks in the S&P500
# ---------------------------------------------------------------------------- #
top_tickers = most_active_sp500()

# ---------------------------------------------------------------------------- #
# Instantiate stock objects
# ---------------------------------------------------------------------------- #
ticker_pos = 20  # Select which ticker to analyze
my_stock = stock.Stock(
    top_tickers.index[ticker_pos], top_tickers.iloc[ticker_pos],
    start_date, end_date)

# ---------------------------------------------------------------------------- #
# Get data of Stocks
# ---------------------------------------------------------------------------- #
stock_data = my_stock.ticker_data

# ---------------------------------------------------------------------------- #
# Various line codes for basic technical analysis
# ---------------------------------------------------------------------------- #
# Calculate return of the stock
'''pct_chg = my_stock.pct_chg()
pct_chg_log = my_stock.pct_chg('log')
cum_return = my_stock.pct_chg('cumulative')'''

# Moving average calculation
mov_avg = {}
mov_avg['sma_50'] = my_stock.moving_avg(50, 'sma')
mov_avg['sma_150'] = my_stock.moving_avg(150, 'sma')
mov_avg['ema_20'] = my_stock.moving_avg(20, 'ema')
mov_avg['ema_40'] = my_stock.moving_avg(40, 'ema')

# MACD Calculation
stock_macd = my_stock.macd()

# ATR calculation
stock_atr = my_stock.atr()

# ---------------------------------------------------------------------------- #
# Basic stocks plots
# ---------------------------------------------------------------------------- #
plot_stock.stock_plot(
    my_stock.ticker, my_stock.name, my_stock.ticker_data,
    stock_macd, mov_avg, 100
)
