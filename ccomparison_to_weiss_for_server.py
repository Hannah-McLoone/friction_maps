# push weisses
import numpy as np
from scipy.optimize import least_squares
import duckdb
import rasterio
import random
import csv
import pandas as pd

"""
extension:
split into training and testing
add scaling by elevation and slope
choose specific sub areas
use roads as mask
"""


def create_table(coords):
    filename = '/maps/hm708/processed_land_without_speed'
    cord_list = [f"[{x}, {y}]" for (x, y) in coords]

    df = pd.DataFrame({"pixel": cord_list})
    df['original_index'] = df.index

    duckdb.query("DROP TABLE IF EXISTS input_pixels; CREATE TEMP TABLE input_pixels (pixel TEXT, original_index INTEGER)")
    duckdb.query("INSERT INTO input_pixels SELECT pixel, original_index FROM df")


    query = f"""
    SELECT input_pixels.pixel, subtype, SUM(coverage) as total_coverage
    FROM input_pixels
    LEFT JOIN read_parquet('{filename}*.parquet') AS read_parquet
    ON input_pixels.pixel = read_parquet.pixel
    GROUP BY input_pixels.pixel, read_parquet.subtype
    """

    result = duckdb.query(query).df()
    pivot_df = result.pivot(index='pixel', columns='subtype', values='total_coverage').fillna(0)
    for col in ["barren", "crop", "forest", "grass", "mangrove", "moss", "shrub", "snow", "urban", "wetland"]:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
    
    pivot_df.fillna(0, inplace=True)
    pivot_df = pivot_df.loc[cord_list].reset_index()

    return(pivot_df)


def toblers_walking_speed(slope):
    slope_rad = np.radians(slope)
    adjusted_slope = np.abs(np.tan(slope_rad) + 0.05)
    return 6 * np.exp(-3.5 * adjusted_slope)

def elevation_adjustment(elevation):
    return 1.016 * np.exp(-0.0001072 * elevation)



def get_weiss_value(coords): # these are float coords
    values = []
    resolution = 0.008333333333333333333

    with rasterio.open('2020_walking_only_friction_surface.geotiff') as src:
        band1 = src.read(1)  # Read once instead of in the loop
        index = src.index
        for x, y in coords:
            col, row = index(x * resolution, y * resolution)
            values.append(band1[row, col])
    
    with rasterio.open('slope_1KMmd_SRTM.tif') as src:
        band1 = src.read(1)  # Read once instead of in the loop
        index = src.index
        for i in range in range (0, len(coords)):
            x,y = coords[i]
            col, row = index(x * resolution, y * resolution)
            slope_scaling = toblers_walking_speed(band1[row, col]) / 5
            values[i] = values[i] / slope_scaling

    with rasterio.open('elevation_1KMmd_SRTM.tif') as src:
        band1 = src.read(1)  # Read once instead of in the loop
        index = src.index
        for i in range in range (0, len(coords)):
            x,y = coords[i]
            col, row = index(x * resolution, y * resolution)
            elevation_scaling = elevation_adjustment(band1[row, col])
            values[i] = values[i] / elevation_scaling

def calculate_speed(coords, params):
    #sum of speed * coverage / sum of coverage
    print('-')
    landtype_to_speed = {
        "barren":params[0],
        "crop": params[1],
        "forest": params[2],
        "grass": params[3],
        "mangrove": params[4],
        "moss": params[5],
        "shrub": params[6],
        "snow": params[7],
        "urban": params[8],
        "wetland": params[9]   
    }

    speed_series = pd.Series(landtype_to_speed)

    # Select only land type columns
    land_columns = list(landtype_to_speed.keys())

    # Calculate weighted sum and total coverage
    weighted_sum = table[land_columns].mul(speed_series)
    coverage_sum = table[land_columns].sum(axis=1)
    weighted_avg_speed = np.where(coverage_sum == 0, 0, weighted_sum.sum(axis=1) / coverage_sum)
    return weighted_avg_speed
    


#pick coords between 85 and -60
resolution = 0.008333333333333333333
coordinates = []
for _ in range(3):
    x = random.randint(-180, 180)
    y = random.randint(-60, 85)# y should go from -60 to 85
    coordinates.append((x//resolution, y//resolution))


#create table no longer in same order as coordinates

truth = get_weiss_value(coordinates)

def residuals(params):
    sample = np.array(calculate_speed(coordinates, params))
    return sample - truth


# Initial guess: 30 parameters
initial_guess = np.ones(10)
table = create_table(coordinates)
print('-')
result = least_squares(residuals, initial_guess, loss='linear', max_nfev=3)  # use 'soft_l1' for robustness???

print(result.x)
with open('optimized_parameters.csv', 'w', newline='') as f:
    csv.writer(f).writerow(result.x)


