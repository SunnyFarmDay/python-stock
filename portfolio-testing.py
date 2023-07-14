import os
import pandas as pd
import numpy as np
import requests

# Define Alpha Vantage API key and stock symbols
api_key = 'J5HX8UOWONGT57TB'
symbols = ['AAPL', 'GOOG', 'MSFT', 'AMZN']

# Define function to get historical data from Alpha Vantage
def get_historical_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=full&apikey={api_key}'
    response = requests.get(url, proxies={'http': 'http://pyy261:26IamTHEbest!@proxy.ha.org.hk:8080', 'https': 'https://pyy261:26IamTHEbest!@proxy.ha.org.hk:8080'})
    data = response.json()['Time Series (Daily)']
    df = pd.DataFrame(data).T
    df.index = pd.to_datetime(df.index)
    df = df.loc[:, ['4. close']].astype(float)
    df.columns = [symbol]
    return df

# Load historical stock prices from Alpha Vantage
prices = pd.concat([get_historical_data(symbol) for symbol in symbols], axis=1)

# Define portfolio allocation
allocation = {'AAPL': 0.4, 'GOOG': 0.3, 'MSFT': 0.2, 'AMZN': 0.1}

# Calculate daily returns for each stock
returns = prices.pct_change()
# Calculate daily returns for the portfolio
portfolio_returns = (returns * allocation).sum(axis=1)

# Calculate performance metrics
cumulative_returns = (1 + portfolio_returns).cumprod() - 1
annual_returns = portfolio_returns.mean() * 252
volatility = portfolio_returns.std() * np.sqrt(252)
sharpe_ratio = annual_returns / volatility

# Print results
print('Cumulative returns:', cumulative_returns[-1])
print('Annual returns:', annual_returns)
print('Volatility:', volatility)
print('Sharpe ratio:', sharpe_ratio)