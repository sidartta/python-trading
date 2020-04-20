# ------------------------------------------------------ #
# Module & Libraries Import
# ------------------------------------------------------ #
import get_stock_data as gsd


# ------------------------------------------------------ #
# Create the stock class
# ------------------------------------------------------ #
class Stock:

    def __init__(self, ticker, startdate, enddate):
        self.ticker = ticker
        self.startdate = startdate
        self.enddate = enddate

    def get_data(self, interval='d'):
        ticker_data = gsd.from_yahoo(self.ticker,
                                     self.startdate,
                                     self.enddate,
                                     interval)
        return ticker_data
