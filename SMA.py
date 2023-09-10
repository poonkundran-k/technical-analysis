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


## Creating SMA
sma = ta.SMA(price_data['Adj Close'], timeperiod=25)
sma = pd.DataFrame(sma)
sma = sma.set_index(price_data.index)
sma = pd.concat([sma, price_data], axis = 1)
sma = sma.dropna()
sma = sma.rename(columns = {0:"SMA"})

#Creating a plot
plt.figure(figsize=(12, 6))
plt.plot(sma.index, sma['Adj Close'], label='Adj Close', color='blue', linewidth=2)
plt.plot(sma.index, sma['SMA'], label='25-Day SMA', color='red', linestyle='--', linewidth=2)
plt.title('Adjusted Close Price and SMA')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()





