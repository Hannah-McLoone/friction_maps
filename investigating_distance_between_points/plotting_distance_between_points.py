import pandas as pd
import random

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast

import math

def haversine(points):
    # Convert degrees to radians

    try:
        (p1,p2) = ast.literal_eval(points)
        (lat1, lon1) = p1
        (lat2, lon2) = p2
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        # Earth's radius in kilometres
        R = 6371.0

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Distance in kilometres
        distance = R * c
        return distance
    except:
        return None



def euclidean(points):
    # Convert degrees to radians

    try:
        (p1,p2) = ast.literal_eval(points)
        (lat1, lon1) = p1
        (lat2, lon2) = p2

        return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 111
    except:
        return None
    


def get_x(points):
    try:
        (p1,p2) = ast.literal_eval(points)
        return p1[0]
    except:
        return None

def get_y(points):
    try:
        (p1,p2) = ast.literal_eval(points)
        return p1[1]
    except:
        return None

# File path

file_path = 'experimentaltest.csv'
df = pd.read_csv(file_path)
df = df[df['class'] == 'unclassified']

df['distance_km'] = df['geometry'].map(haversine)
df['x'] = df['geometry'].map(get_x)
df['y'] = df['geometry'].map(get_y)






max_value = 0.5
import numpy as np
bins = np.linspace(0, max_value, 50)
df['distance_km'] = df['distance_km'].apply(lambda x: min(x, max_value))
                                            
sns.histplot(df['distance_km'], bins=bins)
plt.title('distance - unclassified', fontsize=16)
plt.xlabel('Distance', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
#for every pair apply haversine



"""
#this is the code for visualising how area plays a factor
# plots the points on global map

from matplotlib.colors import Normalize
plt.figure(figsize=(15, 6))
norm = Normalize(vmin=0, vmax=0.5)
scatter = plt.scatter(df['x'], df['y'], c=df['distance_km'], s = 15, cmap='viridis', norm = norm)

# Add colour bar
plt.colorbar(scatter, label='Value')

# Set labels
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')

# Show plot
plt.show()

"""