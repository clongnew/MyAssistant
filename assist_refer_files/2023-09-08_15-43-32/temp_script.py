import yfinance as yf

# 获取A股数据
data = yf.download('^GSPC', start='2022-01-01', end='2022-12-31')

# 打印数据
print(data.head())

# 计算重要数据
max_price = data['Close'].max()
min_price = data['Close'].min()
avg_price = data['Close'].mean()

max_volume = data['Volume'].max()
min_volume = data['Volume'].min()
avg_volume = data['Volume'].mean()

{
    'max_price': max_price,
    'min_price': min_price,
    'avg_price': avg_price,
    'max_volume': max_volume,
    'min_volume': min_volume,
    'avg_volume': avg_volume
}