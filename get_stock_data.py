# ---------------------------------------------------------------------------- #
# Module & Libraries Import
# ---------------------------------------------------------------------------- #
from pandas_datareader import data as pdr
import yfinance as yf

yf.pdr_override()

# ---------------------------------------------------------------------------- #
# Function to get stocks data from Yahoo! Finance
# ---------------------------------------------------------------------------- #
def from_yahoo(
        tick, start_date,
        end_date=None, r='1d'
):
    tentative = 0
    while tentative < 5:
        try:
            data = pdr.get_data_yahoo(
                tick, start=start_date,
                end=end_date, interval=r
            )
        except:
            print(f'Failed to retrieve {tick} stock data... retrying')
            continue

        tentative = tentative + 1

    return data
