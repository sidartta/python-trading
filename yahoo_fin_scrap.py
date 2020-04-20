# ------------------------------------------------------ #
# Module & Libraries Import
# ------------------------------------------------------ #
import requests
from bs4 import BeautifulSoup
import pandas as pd


# ------------------------------------------------------ #
# Function to import top traded stocks data from
# Yahoo! Finance website
# ------------------------------------------------------ #
def most_active_sp500():
    symbols = []
    names = []
    prices = []
    changes = []
    percent_changes = []
    market_caps = []
    total_volumes = []
    pe_ratios = []

    for i in range(0, 12):
        most_active_url = "https://finance.yahoo.com/most-active?count=0&offset=" + str(i * 25)
        r = requests.get(most_active_url)
        data = r.text
        soup = BeautifulSoup(data, features='lxml')
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
                percent_changes.append(percentChange.find('span').text)
            for marketCap in listing.find_all('td', attrs={'aria-label': 'Market Cap'}):
                market_caps.append(marketCap.find('span').text)
            for totalVolume in listing.find_all('td', attrs={'aria-label': 'Volume'}):
                total_volumes.append(totalVolume.find('span').text)
            for pe_ratio in listing.find_all('td', attrs={'aria-label': 'PE Ratio (TTM)'}):
                pe_ratios.append(pe_ratio.text)
    most_active_stocks = pd.DataFrame({'Symbol': symbols,
                                       'Name': names,
                                       'Price': prices,
                                       'Change': changes,
                                       '% Change': percent_changes,
                                       'Market Cap': market_caps,
                                       'Total Volume': total_volumes,
                                       'PE Ratio': pe_ratios},
                                      index=symbols)
    return list(most_active_stocks.index)


# ------------------------------------------------------ #
# Function to import crypto currency macro data from
# Yahoo! Finance website
# ------------------------------------------------------ #
def crypto_macro_data():
    names = []
    prices = []
    changes = []
    percent_changes = []
    market_caps = []
    total_volumes = []
    circulating_supplies = []

    for i in range(0, 4):
        crypto_currencies_url = "https://finance.yahoo.com/cryptocurrencies?count=0&offset=" + str(i * 25)
        r = requests.get(crypto_currencies_url)
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
                percent_changes.append(percentChange.text)
            for marketCap in listing.find_all('td', attrs={'aria-label': 'Market Cap'}):
                market_caps.append(marketCap.text)
            for totalVolume in listing.find_all('td', attrs={'aria-label': 'Total Volume All Currencies (24Hr)'}):
                total_volumes.append(totalVolume.text)
            for circulatingSupplies in listing.find_all('td', attrs={'aria-label': 'Circulating Supply'}):
                circulating_supplies.append(circulatingSupplies.text)

    crypto = pd.DataFrame({'Price': prices,
                           'Change': changes,
                           '% Change': percent_changes,
                           'Market Cap': market_caps,
                           'Total Volume': total_volumes,
                           'Circulating Supply': circulating_supplies},
                          index=names)
    return crypto
