import pandas as pd

# Replace with the path to your Parquet file
file_path = 'output3/just_uk_my_own_values_to_force_it_to_look_good4.parquet'

# Load the Parquet file
df = pd.read_parquet(file_path)

# Print the first few rows
print(df.head())

#is this in it
'[210, 6959]'