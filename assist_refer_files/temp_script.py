import pandas as pd

# 读取数据
data = pd.read_csv('2023_silver_data.csv')

# 计算收盘价的波动性
volatility = data['Close'].std()

volatility