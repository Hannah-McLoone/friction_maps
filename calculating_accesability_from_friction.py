import numpy as np
import heapq
import h5py
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
import heapq

ANGLE = 0.008333333333333333333

def marching_wavefront(friction_map, goals):
    height, width = friction_map.shape
    cost_map = np.full((height, width), np.inf)
    visited = np.full((height, width), False)

    # Initialize wavefront with all goals
    wavefront = []
    for goal_y, goal_x in goals:
        cost_map[goal_y, goal_x] = 0
        heapq.heappush(wavefront, (0, goal_y, goal_x))  # (cost, y, x)

    # 4-connected grid movement
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while wavefront:
        current_cost, y, x = heapq.heappop(wavefront)

        if visited[y, x]:
            continue
        visited[y, x] = True

        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny < height and 0 <= nx < width and not visited[ny, nx]:
                travel_cost = friction_map[ny, nx]
                new_cost = current_cost + travel_cost
                if new_cost < cost_map[ny, nx]:
                    cost_map[ny, nx] = new_cost
                    heapq.heappush(wavefront, (new_cost, ny, nx))

    return cost_map


import numpy as np
import heapq

def arcsecond_wavefront(friction_map, goals, lat_start_deg, arcsec_resolution=1):
    height, width = friction_map.shape
    cost_map = np.full((height, width), np.inf)
    visited = np.full((height, width), False)

    # Convert arcsecond resolution to degrees
    deg_resolution = arcsec_resolution / 3600.0
    earth_radius_km = 6371.0

    # Precompute per-row distances in km
    row_latitudes = lat_start_deg - np.arange(height) * deg_resolution
    row_lat_radians = np.radians(row_latitudes)

    # Distance per arcsecond in each direction
    dlat_km = earth_radius_km * np.pi / 648000  # constant ~30.87 m
    dlon_km = earth_radius_km * np.cos(row_lat_radians) * np.pi / 648000  # varies with latitude

    wavefront = []
    for goal_y, goal_x in goals:
        cost_map[goal_y, goal_x] = 0
        heapq.heappush(wavefront, (0, goal_y, goal_x))

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # N, S, W, E

    while wavefront:
        current_cost, y, x = heapq.heappop(wavefront)

        if visited[y, x]:
            continue
        visited[y, x] = True

        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny < height and 0 <= nx < width and not visited[ny, nx]:
                # Adjust step distance depending on direction and location
                if dx != 0:
                    step_km = dlon_km[y]
                else:
                    step_km = dlat_km

                travel_cost = friction_map[ny, nx] * step_km
                new_cost = current_cost + travel_cost
                if new_cost < cost_map[ny, nx]:
                    cost_map[ny, nx] = new_cost
                    heapq.heappush(wavefront, (new_cost, ny, nx))

    return cost_map



#take sample of my road map
def get_map(x,y,width,height, land_scaling = 1):
    start_row =  int((90-y) / ANGLE )
    end_row = start_row + height
    start_col =  int((180+x) / ANGLE )
    end_col = start_col + width


    # Open the existing HDF5 file in read mode
    with h5py.File('land_friction_map.h5', 'r') as hdf5_file:
        data_var = hdf5_file['data']
        land_sample = data_var[start_row:end_row, start_col:end_col]
        #land_sample = land_sample[::10,::10]
        land_sample = land_sample / land_scaling

    with h5py.File('road_fricion_map.h5', 'r') as hdf5_file:
        data_var = hdf5_file['data']
        road_sample = data_var[start_row:end_row, start_col:end_col]
        #road_sample = road_sample[::10,::10]


    return np.maximum(land_sample, road_sample), land_sample == 0



#y then x from top left hand corner
def turn_coord_into_position(x,y, x2, y2):
    y =  int((y2-y) / ANGLE )
    x =  int((x-x2) / ANGLE )
    return (y,x)


speed_map, mask = get_map(-80,10,6000,6000,3)
friction_map = 1/speed_map


#the 5 biggiest cities in south america. all with population> 10 million
sao_paulo = turn_coord_into_position(-46.5, -23.5, -80, 10)
buenos_aires = turn_coord_into_position(-58.5, -34.6, -80, 10)
rio = turn_coord_into_position(-43.5, -23, -80, 10)
bogota = turn_coord_into_position(-74, 4.5, -80, 10)
lima = turn_coord_into_position(-77, -12, -80, 10)

cost_map = arcsecond_wavefront(friction_map, [sao_paulo, buenos_aires, rio, bogota, lima], 10)

#this is to make the values that are not land into nan
cost_map[mask] = np.nan


np.save('cost_map2.npy', cost_map)