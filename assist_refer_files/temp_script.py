import pandas as pd

# Assuming you have the historical data of gold prices
# in a CSV file named 'gold_prices.csv'

# Read the CSV file
df = pd.read_csv('gold_prices.csv')

# Filter the data for the year 2023
df_2023 = df[df['Year'] == 2023]

# Analyze the data
analysis = df_2023.describe()

# Get the mean price
mean_price = analysis.loc['mean', 'Price']

# Get the maximum price
max_price = analysis.loc['max', 'Price']

# Get the minimum price
min_price = analysis.loc['min', 'Price']

# Get the standard deviation
std_dev = analysis.loc['std', 'Price']

# Print the analysis results
analysis, mean_price, max_price, min_price, std_dev