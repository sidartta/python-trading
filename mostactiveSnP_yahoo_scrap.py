# Module & Libraries Import
import requests
from bs4 import BeautifulSoup
import pandas as pd

symbols = []
names = []
prices = []
changes = []
percentChanges = []
marketCaps = []
totalVolumes = []
pe_ratios = []

for i in range(0, 12):
    MostActiveUrl = "https://finance.yahoo.com/most-active?count=0&offset=" + str(i * 25)
    r = requests.get(MostActiveUrl)
    data = r.text
    soup = BeautifulSoup(data)
    for listing in soup.find_all('tr', attrs={'class': 'simpTblRow'}):
        for symbol in listing.find_all('td', attrs={'aria-label': 'Symbol'}):
            symbols.append(symbol.find('a').text)
        for name in listing.find_all('td', attrs={'aria-label': 'Name'}):
            names.append(name.text)
        for price in listing.find_all('td', attrs={'aria-label': 'Price (Intraday)'}):
            prices.append(price.find('span').text)
        for change in listing.find_all('td', attrs={'aria-label': 'Change'}):
            changes.append(change.find('span').text)
        for percentChange in listing.find_all('td', attrs={'aria-label': '% Change'}):
            percentChanges.append(percentChange.find('span').text)
        for marketCap in listing.find_all('td', attrs={'aria-label': 'Market Cap'}):
            marketCaps.append(marketCap.find('span').text)
        for totalVolume in listing.find_all('td', attrs={'aria-label': 'Volume'}):
            totalVolumes.append(totalVolume.find('span').text)
        for pe_ratio in listing.find_all('td', attrs={'aria-label': 'PE Ratio (TTM)'}):
            pe_ratios.append(pe_ratio.text)

most_active_stocks = pd.DataFrame({'Name': names,
                                   'Price': prices,
                                   'Change': changes,
                                   '% Change': percentChanges,
                                   'Market Cap': marketCaps,
                                   'Total Volume': totalVolumes,
                                   'PE Ratio': pe_ratios},
                                  index=symbols)
print(most_active_stocks)

# Save Initial data to an excel file
# most_active_stocks.to_excel("most_active_SnP.xlsx", sheet_name="Most Active Stocks")
