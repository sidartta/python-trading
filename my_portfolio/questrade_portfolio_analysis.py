# ---------------------------------------------------------------------------- #
# Module & Libraries Import
# ---------------------------------------------------------------------------- #
import json
import stock
from datetime import date, timedelta
import pandas as pd
import perf_kpi as kpi

# ---------------------------------------------------------------------------- #
# Variables initialization
# ---------------------------------------------------------------------------- #
yrs = 5
num_days = 365 * yrs
start_date = date.today() - timedelta(num_days)
end_date = date.today()
window = round(num_days / 4)
risk_free = 0.025
# ---------------------------------------------------------------------------- #
# Read Questrade portfolio from Json data
# ---------------------------------------------------------------------------- #
with open('questrade.json', 'r') as j:
    p = json.load(j)

portfolio = pd.DataFrame(p['RRSP']['2020-04-25']['Positions'])
portfolio.set_index('Ticker', inplace=True)
tickers = list(portfolio.index.values)

# ---------------------------------------------------------------------------- #
# Instantiate equities objects & price data frames
# ---------------------------------------------------------------------------- #
my_stocks = {}

col = pd.MultiIndex.from_product([tickers, ['Close', 'Market Value']])
price_data = pd.DataFrame(columns=col)

for tk in tickers:
    my_stocks[tk] = stock.Stock(tk, portfolio.loc[tk, 'Name'],
                                start_date, end_date)
    price_data[(tk, 'Close')] = my_stocks[tk].close
    price_data[(tk, 'Market Value')] = price_data[(tk, 'Close')] \
                                       * portfolio.loc[tk, 'Shares']

mrkt_val = price_data.xs('Market Value', axis=1, level=1, drop_level=True)
price_data['Total Value'] = mrkt_val.sum(axis=1)

# ---------------------------------------------------------------------------- #
# Portfolio Analysis
# ---------------------------------------------------------------------------- #
# Cost Basis :
cost_basis = 0
for val in tickers:
    shares = portfolio.loc[val, 'Shares']
    cost_per_share = portfolio.loc[val, 'Cost/Share']
    cost_basis += cost_per_share * shares

CAGR = kpi.cagr(price_data['Total Value'])
volatility = kpi.volatility(price_data['Total Value'])
sharpe_ratio = kpi.sharpe(price_data['Total Value'], risk_free)
sortino_ratio = kpi.sortino(price_data['Total Value'], risk_free)
