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


