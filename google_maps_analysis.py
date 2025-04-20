# DO NOT LEAVE API KEY IN
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import requests
import random
import h5py
import heapq

angle = 0.008333333333333333333# / 5



def get_google_data(origins, destinations):
    api_key = 1##

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
        results = data['rows']
        v = [r['elements'][0]['duration']['value'] for r in results]
        return v[0] #get rid of 0. this is in seconds
    else:
        print(f"Request failed with status code: {response.status_code}")




import heapq
import heapq
import math

def shortest_path_cost(friction_map, start, end):
    rows, cols = len(friction_map), len(friction_map[0])
    visited = [[False] * cols for _ in range(rows)]
    costs = [[float('inf')] * cols for _ in range(rows)]

    queue = [(0, start)]
    costs[start[0]][start[1]] = 0

    # Directions and movement cost multipliers
    directions = [
        (-1, 0, 1.0), (1, 0, 1.0), (0, -1, 1.0), (0, 1, 1.0),        # N, S, W, E
        (-1, -1, math.sqrt(2)), (-1, 1, math.sqrt(2)),              # NW, NE
        (1, -1, math.sqrt(2)), (1, 1, math.sqrt(2))                 # SW, SE
    ]

    while queue:
        current_cost, (r, c) = heapq.heappop(queue)

        if visited[r][c]:
            continue
        visited[r][c] = True

        if (r, c) == end:
            return current_cost

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
non_zero_indices = [(i, j) for i in range(data.shape[0]) for j in range(data.shape[1]) if data[i, j] != 0]
selected_indices = random.sample(non_zero_indices,  10)

cost = []
truth = []

for i in range(0,len(selected_indices)-1):
    p1 = selected_indices[i]
    p2 = selected_indices[i+1]

    p1_string = str(58 - p1[0] * angle) + ',' + str(-6 + p1[1]* angle)
    p2_string = str(58 - p2[0] * angle) + ',' + str(-6 + p2[1]* angle)

    cost.append(shortest_path_cost(friction_map,p1,p2)*60)
    truth.append(get_google_data(p1_string,p2_string)/60)



import matplotlib.pyplot as plt


plt.scatter(truth, cost)
plt.plot(truth, truth, linestyle='-', color='gray')  # x = y line

plt.xlabel('truth')
plt.ylabel('cost')

plt.show()