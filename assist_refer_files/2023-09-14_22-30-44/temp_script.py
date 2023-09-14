import pandas as pd

# 读取数据
data = pd.read_csv('2023_silver_data.csv')

# 转换日期格式
data['Date'] = pd.to_datetime(data['Date'])

# 计算移动平均线
data['MA_20'] = data['Close'].rolling(window=20).mean()
data['MA_50'] = data['Close'].rolling(window=50).mean()

# 计算波动性指标
data['Volatility'] = data['Close'].rolling(window=20).std()

# 输出分析结果
data[['Date', 'Close', 'MA_20', 'MA_50', 'Volatility']]