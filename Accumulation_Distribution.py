## import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import linear_model
from sklearn.linear_model import LinearRegression as lm
import yfinance as yf
import talib as ta

## Download historic prices 
ticker = "TANLA.NS"

price_data = yf.download(ticker, period="5y")

# Calculate ADL
price_data['MoneyFlowMultiplier'] = ((price_data['Close'] - price_data['Low']) - (price_data['High'] - price_data['Close'])) / (price_data['High'] - price_data['Low'])
price_data['MoneyFlowVolume'] = price_data['MoneyFlowMultiplier'] * price_data['Volume']
price_data['ADL'] = price_data['MoneyFlowVolume'].cumsum()

# Define buy and sell thresholds (you can adjust these thresholds)
buy_threshold = 4000000  # ADL value above which to generate a buy signal
sell_threshold = -4000000  # ADL value below which to generate a sell signal

# Initialize the Signal column
price_data['Signal'] = ''

# Generate buy and sell signals based on ADL thresholds
for i in range(1, len(price_data)):
    if price_data['ADL'][i] > buy_threshold and price_data['ADL'][i - 1] <= buy_threshold:
        price_data.at[price_data.index[i], 'Signal'] = 'Buy'
    elif price_data['ADL'][i] < sell_threshold and price_data['ADL'][i - 1] >= sell_threshold:
        price_data.at[price_data.index[i], 'Signal'] = 'Sell'

# Plot the ADL indicator
plt.figure(figsize=(12, 6))
plt.plot(price_data.index, price_data['ADL'], label='Accumulation Distribution Line (ADL)', color='blue')
plt.title('Accumulation Distribution Line (ADL)')
plt.xlabel('Date')
plt.ylabel('ADL Value')
plt.legend()
plt.grid(True)
plt.show()
