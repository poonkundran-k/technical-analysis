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

# Define the ATR period (typically 14 days)
atr_period = 14

# Calculate True Range (TR) for each day
price_data['H-L'] = price_data['High'] - price_data['Low']
price_data['H-PC'] = abs(price_data['High'] - price_data['Adj Close'].shift(1))
price_data['L-PC'] = abs(price_data['Low'] - price_data['Adj Close'].shift(1))
price_data['TR'] = price_data[['H-L', 'H-PC', 'L-PC']].max(axis=1)

# Calculate the ATR using the Wilder's smoothing method
price_data['ATR'] = price_data['TR'].rolling(window=atr_period).mean()

# Print the DataFrame with ATR values
print(price_data[['TR', 'ATR']])

# Define the ATR multiplier for buy and sell signals (adjust as needed)
buy_multiplier = 2.0
sell_multiplier = 1.5

# Initialize the Signal column
price_data['Signal'] = ''

# Generate buy and sell signals based on ATR
for i in range(atr_period, len(price_data)):
    if price_data['Adj Close'][i] > price_data['Adj Close'][i - 1] + (price_data['ATR'][i] * buy_multiplier):
        price_data.at[price_data.index[i], 'Signal'] = 'Buy'
    elif price_data['Adj Close'][i] < price_data['Adj Close'][i - 1] - (price_data['ATR'][i] * sell_multiplier):
        price_data.at[price_data.index[i], 'Signal'] = 'Sell'

# Plot the ATR
plt.figure(figsize=(12, 6))
plt.plot(price_data.index, price_data['ATR'], label='Average True Range (ATR)', color='blue')
plt.title('Average True Range (ATR)')
plt.xlabel('Date')
plt.ylabel('ATR Value')
plt.legend()
plt.grid(True)
plt.show()








