import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV files as DataFrames
df = pd.read_csv('land_algo_comparison_amazon.csv',  header=None, skiprows=1, names=["g1",'g2','best_algo_speed','worse_algo_speed','shit_algo_speed'])

# Calculate percentage difference
filtered_df = df[
    (df['best_algo_speed'] > 5.2) | 
    (df['best_algo_speed'] < 4.8) | 
    (df['worse_algo_speed'] > 5.2) | 
    (df['worse_algo_speed'] < 4.8)
]

df = filtered_df
percentage_diff = abs(df["best_algo_speed"] - df["shit_algo_speed"]) / ((df["best_algo_speed"] + df["shit_algo_speed"]) / 2) * 100

# Plot histogram
plt.figure(figsize=(8, 6))
#plt.scatter(df["best_algo_speed"], df["worse_algo_speed"], alpha=0.1)

#"""
plt.hist(percentage_diff, bins=range(0, 101, 1), edgecolor='black', alpha=0.7)
plt.xlabel("Percentage Difference")
plt.ylabel("Frequency")
plt.title("Histogram of Percentage Differences")
plt.grid(axis='y', linestyle='--', alpha=0.7)
#"""
plt.show()


