import yfinance as yf

# 获取白银数据
silver = yf.download('SI=F', start='2023-01-01', end='2023-12-31')

# 打印数据
print(silver.head())
print(silver.tail())

# 进行数据分析
analysis = silver.describe()

analysis