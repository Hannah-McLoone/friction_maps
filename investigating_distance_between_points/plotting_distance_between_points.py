import pandas as pd
import random

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast

import math
import numpy as np


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

file_path = 'investigating_distance_between_points/sample_of_road_points.csv' # depending on working directory get rid of the file name
#file_path = 'investigating_distance_between_points/amazon_sample.csv'
df = pd.read_csv(file_path)
df = df[df['class'] == 'unclassified']
print(len(df))
df['distance_km'] = df['geometry'].map(haversine)
df['x'] = df['geometry'].map(get_x)
df['y'] = df['geometry'].map(get_y)


df = df[df['x'] > -80]

#df = df[(df['x'] + 63)**2 + (df['y'] + 3)**2 < 100]
print(len(df))
max_value = 0.5
import numpy as np
bins = np.linspace(0, max_value, 50)
df['distance_km'] = df['distance_km'].apply(lambda x: min(x, max_value))


#"""
sns.histplot(df['distance_km'], bins=bins)

#plt.yscale('log') if i want the logged version

plt.title('Unclassified', fontsize=16)
plt.xlabel('Distance', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

#"""


"""
#this is the code for visualising how area plays a factor
# plots the points on global map

from matplotlib.colors import Normalize
#plt.figure(figsize=(15, 6))
plt.figure(figsize=(7, 6))
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
"""

import random
import math
import matplotlib.pyplot as plt
import numpy as np

log_display = False

num_trials = 1000#10000   # number of trials per resolution

if log_display:
    resolutions = np.logspace(-3, 0, num=20)  # From 0.001 to 1 (log scale)
else:
    resolutions = np.linspace(0, 1, num=21)  # Linear spacing from 0.001 to 1

resolutions[0] = 0.00001
results = []
resolutions  = [1]
for resolution in resolutions:
    count = 0
    for _ in range(num_trials):
        # Sample starting point in [0, resolution) x [0, resolution)
        p1 = (random.uniform(0, resolution), random.uniform(0, resolution))
        d = df['distance_km'].sample(n=1).item()

        theta = random.uniform(0, 2 * math.pi)

        # Compute p2
        x2 = p1[0] + d * math.cos(theta)
        y2 = p1[1] + d * math.sin(theta)
        p2 = (x2, y2)

        # Grid cell p2 lands in
        p2_box = (p2[0] // resolution, p2[1] // resolution)

        if p2_box in [(0, 0), (0, 1), (1, 0), (-1, 0), (0, -1)]:
            count += 1

    results.append(count / num_trials)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(resolutions, results, marker='o')
plt.ylabel('Proportion of points in neighbor boxes')
plt.axhline(y=0.95, color='red', linestyle='--', label='95% line')


if log_display:
    plt.xscale('log')#!!!!!
    plt.xlabel('Resolution (log scale)')
    plt.grid(True, which='both', ls='--')#!!!!!
else:
    plt.xlabel('Resolution')
    plt.grid(True)
    
plt.tight_layout()
plt.show()

print(results)


"""