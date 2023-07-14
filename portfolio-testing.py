import os
import pandas as pd
import numpy as np
import requests
import datetime
import time
from alpha_vantage.timeseries import TimeSeries
# Define Alpha Vantage API key and stock symbols
api_key = 'J5HX8UOWONGT57TB'
# symbols
symbols = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA', 'JPM', 'JNJ', 'PG', 'KO', 'V', 'MA', 'PYPL', 'DIS', 'NFLX', 'NKE', 'SBUX', 'HD', 'LOW', 'TGT', 'WMT', 'VZ', 'T', 'XOM', 'CVX', 'PLD', 'AMT', 'NEE', 'UNH', 'MRNA']

# Define portfolio allocation
market_cap_weighted= [0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.005, 0.005, 0.005, 0.005, 0.0025, 0.0025, 0.0025, 0.0025, 0.0025]
allocation = {}
for index, stock in enumerate(symbols):
    allocation[f'{stock}'] = market_cap_weighted[index]
# Define function to get historical data from Alpha Vantage

def get_historical_data(symbol):
    now = datetime.date.today()
    data_file_name = f'./cache/{now}_{symbol}.csv'
    if os.path.exists(data_file_name):
        with open(data_file_name, "r"):
            df = pd.read_csv(data_file_name, header=0, index_col=0, parse_dates=True)
            return df
    else:
        retreiving = True
        while retreiving:
            try:
                ts = TimeSeries(key='YOUR_API_KEY', output_format='pandas')
                df, _ = ts.get_daily_adjusted(symbol=symbol, outputsize='full')
                retreiving = False
            except ValueError as e:
                print(e)
                print('Waiting for 61 seconds')
                time.sleep(61)
                continue
        df.index = pd.to_datetime(df.index)
        df = df.loc[:, ['4. close']].astype(float)
        df.columns = [f'{symbol}_close'] # Set unique column name for each stock
        df.to_csv(data_file_name)
        return df

symbols = ['AAPL']
allocation = {'APPL': 1}
def limit_date_period(start, end, df):
    mask = (df.index >= start) & (df.index <= end)
    return df.loc[mask]

# Load historical stock prices from Alpha Vantage
prices = pd.concat([limit_date_period('2015-12-30', '2015-12-31', get_historical_data(symbol)) for symbol in symbols], axis=1)
# prices = pd.concat([limit_date_period('2015-12-30', '2015-12-31', get_historical_data(symbol)) for symbol in symbols], axis=1)
print(prices)
prices = prices.fillna(100)
print(prices)
# Calculate daily returns for each stock
returns = prices.pct_change()
print(returns)
# Calculate daily returns for the portfolio
portfolio_returns = (returns * allocation).sum(axis=1)
print(portfolio_returns)

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