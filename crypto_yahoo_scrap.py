# Module & Libraries Import
import requests
from bs4 import BeautifulSoup
import pandas as pd

names = []
prices = []
changes = []
percentChanges = []
marketCaps = []
totalVolumes = []
circulatingSupplys = []

for i in range(0, 4):
    CryptoCurrenciesUrl = "https://finance.yahoo.com/cryptocurrencies?count=0&offset=" + str(i * 25)
    r = requests.get(CryptoCurrenciesUrl)
    data = r.text
    soup = BeautifulSoup(data)
    for listing in soup.find_all('tr', attrs={'class': 'simpTblRow'}):
        for name in listing.find_all('td', attrs={'aria-label': 'Name'}):
            names.append(name.text)
        for price in listing.find_all('td', attrs={'aria-label': 'Price (Intraday)'}):
            prices.append(price.find('span').text)
        for change in listing.find_all('td', attrs={'aria-label': 'Change'}):
            changes.append(change.text)
        for percentChange in listing.find_all('td', attrs={'aria-label': '% Change'}):
            percentChanges.append(percentChange.text)
        for marketCap in listing.find_all('td', attrs={'aria-label': 'Market Cap'}):
            marketCaps.append(marketCap.text)
        for totalVolume in listing.find_all('td', attrs={'aria-label': 'Total Volume All Currencies (24Hr)'}):
            totalVolumes.append(totalVolume.text)
        for circulatingSupply in listing.find_all('td', attrs={'aria-label': 'Circulating Supply'}):
            circulatingSupplys.append(circulatingSupply.text)

crypto = pd.DataFrame({'Price': prices,
                       'Change': changes,
                       '% Change': percentChanges,
                       'Market Cap': marketCaps,
                       'Total Volume': totalVolumes,
                       'Circulating Supply': circulatingSupplys},
                      index=names)
print(crypto)

# Save Initial data to an excel file
crypto.to_excel("crypto.xlsx", sheet_name='Crypto Data')
