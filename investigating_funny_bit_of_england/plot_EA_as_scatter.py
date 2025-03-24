"""
code that produces the scatter plot

"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Specify the Parquet file path
file_path = "pixel_to_road_speed35.parquet"


df = pd.read_parquet(file_path, columns=['geometry'])


#df = df[df['speed_kph']>=95]
df = df[df['class']=='primary']


#df = df.sort_values(by='speed_kph')



x_values, y_values = zip(*df['geometry'])
#speeds = df['speed_kph'].values


# Filter points within the desired range
filtered_points = [(x, y) for x, y in zip(x_values, y_values) if 0 <= x < 220]


if filtered_points:
    x_values, y_values = zip(*filtered_points)
else:
    x_values, y_values = [], [], []


# Plot with colours based on speed
plt.scatter(x_values, y_values, cmap='viridis', s = 3, label='Data Points')#,c=speeds)
plt.colorbar(label='Speed')  # Add colour bar to indicate speed values

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Scatter Plot of (x, y) Pairs with Colour Based on Speed')
plt.legend()
plt.grid()
plt.show()
