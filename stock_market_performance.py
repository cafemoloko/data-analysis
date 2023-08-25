import pandas as pd
import plotly.express as px
import yfinance as yf
from datetime import datetime


start_date = datetime.now() - pd.DateOffset(month=3)
end_date = datetime.now()

tickers = ['AMD', 'INTC', 'NVDA']

df_list = []

for ticker in tickers:
    data = yf.download(ticker, start=start_date, end=end_date)
    df_list.append(data)

df = pd.concat(df_list, keys=tickers, names=['Ticker', 'Date'])
print(df.head())

df = df.reset_index()
print(df.head())

fig_line = px.line(df, x='Date', y='Close', color='Ticker', title='Stock Market Performance (AMD, Intel and NVIDIA)')
fig_area = px.area(df, x='Date', y='Close', color='Ticker', facet_col='Ticker', 
                   labels={'Date':'Date', 'Close':'Closing Price', 'Ticker':'Company'},
                   title='Stock Prices for AMD, Intel and NVIDIA')

fig_line.show() # Stock rerformance for the last 3 months, line chart
fig_area.show() # Stock performance for the last 3 months, faceted area chart


# Moving averages (MA)

# When the MA10 crosses above the MA20, it indicates that the stock price will rise. Contrarily, if the MA10 crosses below 
# the MA20 - the stock price will fall. 


df['MA10'] = df.groupby('Ticker')['Close'].rolling(window=10).mean().reset_index(0, drop=True)
df['MA20'] = df.groupby('Ticker')['Close'].rolling(window=20).mean().reset_index(0, drop=True)

for ticker, group in df.groupby('Ticker'):
    print(f'Moving Averages for {ticker}')
    print(group[['MA10', 'MA20']])

for ticker, group in df.groupby('Ticker'):
    fig_ma = px.line(group, x='Date', y=['Close', 'MA10', 'MA20'],
                     title=f"{ticker} Moving Averages")
    fig_ma.show()


# Volatility (a measure of how much and how often the stock price fluctuates over a given period of time)

df['Volatility'] = df.groupby('Ticker')['Close'].pct_change().rolling(window=10).std().reset_index(0, drop=True)
fig_vol = px.line(df, x='Date', y='Volatility', 
              color='Ticker', 
              title='Volatility of All Companies')
fig_vol.show()


# Correlation between NVIDIA and AMD stock prices
# correlation (line): positive /, negative \, no correlation -

amd = df.loc[df['Ticker'] == 'AMD', ['Date', 'Close']].rename(columns={'Close': 'AMD'})
nvidia = df.loc[df['Ticker'] == 'NVDA', ['Date', 'Close']].rename(columns={'Close': 'NVDA'})

df_corr = pd.merge(amd, nvidia, on='Date')

fig_corr = px.scatter(df_corr, x='AMD', y='NVDA', trendline='ols',
                      title='Correlation between AMD and NVIDIA')
fig_corr.show()
