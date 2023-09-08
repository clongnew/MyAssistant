import pandas as pd

# Load the data
data = pd.read_csv('2023_silver_data.csv')

# Perform statistical analysis
silver_stats = data.describe()

# Calculate the correlation between silver and gold
correlation = data['Silver'].corr(data['Gold'])

silver_stats, correlation