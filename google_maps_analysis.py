# DO NOT LEAVE API KEY IN
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#this road must have fewer than the other.

"""
theres 3 sources of data

uk_roads[??]:
uing weisses global values

uk_roads_other: [?????]
using weises values for uk values

uk2_roads_other:
using speed limits. if data isnt available, increased speed limit - forced to fit.

"""
import requests
import random
import h5py
import heapq
import pandas as pd
import matplotlib.pyplot as plt
import math


from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")


angle = 0.008333333333333333333



def get_google_data(origins, destinations):

    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origins, 
        "destinations": destinations,
        "travelMode": 'DRIVING',
        "key": api_key
    }

    response = requests.get(url, params=params)

    # Check for a successful response
    if response.status_code == 200:
        data = response.json()
        try:
            results = data['rows']
            v = [r['elements'][0]['duration']['value'] for r in results]
            return v[0] #get rid of 0. this is in seconds
        except:
            print(results)
            return -100
    else:
        print(f"Request failed with status code: {response.status_code}")





def shortest_path_cost(friction_map, start, end):
    rows, cols = len(friction_map), len(friction_map[0])
    visited = [[False] * cols for _ in range(rows)]
    costs = [[float('inf')] * cols for _ in range(rows)]

    queue = [(0, start)]
    costs[start[0]][start[1]] = 0

    # Directions and movement cost multipliers
    directions = [
        (-1, 0, 0.93), (1, 0, 0.93),        # N, S
        (0, -1, 0.53), (0, 1, 0.53),        # W, E
        (-1, -1, 1.05), (-1, 1,1.05),              # NW, NE
        (1, -1, 1.05), (1, 1, 1.05)                 # SW, SE
    ]

    while queue:
        current_cost, (r, c) = heapq.heappop(queue)

        if visited[r][c]:
            continue
        visited[r][c] = True

        if (r, c) == end:
            return current_cost * 60 #delet the * 60

        for dr, dc, multiplier in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                move_cost = friction_map[nr][nc] * multiplier
                new_cost = current_cost + move_cost
                if new_cost < costs[nr][nc]:
                    costs[nr][nc] = new_cost
                    heapq.heappush(queue, (new_cost, (nr, nc)))

    return float('inf')  # Unreachable

















with h5py.File('uk_roads.h5', 'r') as f:
    # Get the first dataset in the file
    dataset = next(iter(f.values()))
    data = dataset[:]


friction_map = 1/(data)

# Randomly select 10 indices from the non-zero ones (or fewer if there aren’t 10)
#non_zero_indices = [(i, j) for i in range(data.shape[0]) for j in range(data.shape[1]) if data[i, j] != 0]
#selected_indices = random.sample(non_zero_indices,  10)





#kill---------------------------------------


import ast

# Load the CSV file
df = pd.read_csv("comparison_to_google.csv")  # Replace with your actual file path

# Convert 'start_indices' and 'destination_indices' from strings to tuples
df['start_indices'] = df['start_indices'].apply(ast.literal_eval)
df['desitnation_indices'] = df['desitnation_indices'].apply(ast.literal_eval)



df['values'] = df.apply(lambda row: shortest_path_cost(friction_map,row['start_indices'], row['desitnation_indices']), axis=1)

print(len(df['truth']))
print(len(df['values']))
#---------------------------------------------------

"""


table = {
    'start_indices': [],
    'desitnation_indices' : [],
    'start_loc' : [],
    'end_loc' : [],
    'cost' : [],
    'truth':[]
}

df = pd.DataFrame(table)

for i in range(0,len(selected_indices)-1):
    p1 = selected_indices[i]
    p2 = selected_indices[i+1]

    p1_string = str(58 - p1[0] * angle) + ',' + str(-6 + p1[1]* angle)
    p2_string = str(58 - p2[0] * angle) + ',' + str(-6 + p2[1]* angle)

    cost = (shortest_path_cost(friction_map,p1,p2))
    truth = (get_google_data(p1_string,p2_string)/60)

    new_row = pd.DataFrame({
    'start_indices': [p1],
    'desitnation_indices': [p2],
    'start_loc': [p1_string],
    'end_loc': [p2_string],
    'cost': [cost],
    'truth': [truth]
    })

    df = pd.concat([df, new_row], ignore_index=True)


#df.to_csv('comparison_to_google.csv', mode='a', index=False, header=False)

#"""
print(df['values'])
plt.scatter(df['truth'], df['values'])
plt.plot(df['truth'], df['truth'], linestyle='-', color='gray')  # x = y line

plt.xlabel('truth')
plt.ylabel('cost')

plt.show()
