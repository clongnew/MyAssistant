import yfinance as yf

# 获取A股数据
data = yf.download('^GSPC', start='2022-01-01', end='2022-12-31')
data.head()