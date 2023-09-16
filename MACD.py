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

## MACD Function
def MACD(DF, a=12 ,b=26, c=9):
    """function to calculate MACD
       typical values a(fast moving average) = 12; 
                      b(slow moving average) =26; 
                      c(signal line ma window) =9"""
    df = DF.copy()
    df["ma_fast"] = df["Adj Close"].ewm(span=a, min_periods=a).mean()
    df["ma_slow"] = df["Adj Close"].ewm(span=b, min_periods=b).mean()
    df["macd"] = df["ma_fast"] - df["ma_slow"]
    df["signal_line"] = df["macd"].ewm(span=c, min_periods=c).mean()
    df["hist"] = df["macd"] - df["signal_line"]
    return df.loc[:,["macd","signal_line","hist"]]


price_data[["MACD","SIGNAL_LINE","HIST"]] = MACD(price_data, a=12 ,b=26, c=9)

## Generate buy and sell signals
price_data['SIGNAL'] = 0  # Initialize the Signal column

for i in range(26 + 9, len(price_data)):
    if price_data['MACD'][i] > price_data['SIGNAL_LINE'][i] and price_data['MACD'][i - 1] <= price_data['SIGNAL_LINE'][i - 1]:
        price_data.at[price_data.index[i], 'SIGNAL'] = 'Buy'
    elif price_data['MACD'][i] < price_data['SIGNAL_LINE'][i] and price_data['MACD'][i - 1] >= price_data['SIGNAL_LINE'][i - 1]:
        price_data.at[price_data.index[i], 'SIGNAL'] = 'Sell'

## MACD Plot
plt.figure(figsize=(12, 6))
plt.plot(price_data.index, price_data['MACD'], label='MACD', color='blue')
plt.plot(price_data.index, price_data['SIGNAL_LINE'], label='Signal Line', color='red')
plt.title('MACD and Signal Line')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()

# Plot buy and sell signals
buy_signals = price_data[price_data['SIGNAL'] == 'Buy']
sell_signals = price_data[price_data['SIGNAL'] == 'Sell']
plt.scatter(buy_signals.index, buy_signals['MACD'], marker='^', color='green', label='Buy Signal', alpha=1)
plt.scatter(sell_signals.index, sell_signals['MACD'], marker='v', color='red', label='Sell Signal', alpha=1)

plt.legend()
plt.grid(True)
plt.show()