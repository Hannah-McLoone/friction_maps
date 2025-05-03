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


def calculate_speed(coords, params):
    filename = '/maps/hm708/processed_land_without_speed'

    df = pd.DataFrame({"pixel": [f"[{x}, {y}]" for (x, y) in coords]})
    df['original_index'] = df.index

    duckdb.query("DROP TABLE IF EXISTS input_pixels; CREATE TEMP TABLE input_pixels (pixel TEXT, original_index INTEGER)")
    duckdb.query("INSERT INTO input_pixels SELECT pixel, original_index FROM df")

    #edit this to be the actual parameter types used!!!
    land_type_to_speed = {
        "barren": params[0],          
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

    # Convert the dictionary to a DataFrame
    mapping_df = pd.DataFrame(list(land_type_to_speed.items()), columns=['land_type', 'speed'])

    # Register it as a DuckDB table
    duckdb.register('land_speed_mapping', mapping_df)

    query = f"""
    SELECT 
        input_pixels.pixel, 
        COALESCE(SUM(mapping.speed * read_parquet.coverage) / NULLIF(SUM(read_parquet.coverage), 0), 0) AS weighted_avg_speed
    FROM input_pixels
    LEFT JOIN read_parquet('{filename}*.parquet') AS read_parquet
        ON input_pixels.pixel = read_parquet.pixel
    LEFT JOIN land_speed_mapping AS mapping
        ON read_parquet.subtype = mapping.land_type
    GROUP BY input_pixels.pixel, input_pixels.original_index
    ORDER BY input_pixels.original_index
    """

    result = duckdb.query(query).df()
    return result['weighted_avg_speed']


def create_table(coords):
    filename = '/maps/hm708/processed_land_without_speed'

    df = pd.DataFrame({"pixel": [f"[{x}, {y}]" for (x, y) in coords]})
    df['original_index'] = df.index

    duckdb.query("DROP TABLE IF EXISTS input_pixels; CREATE TEMP TABLE input_pixels (pixel TEXT, original_index INTEGER)")
    duckdb.query("INSERT INTO input_pixels SELECT pixel, original_index FROM df")


    query = f"""
    SELECT input_pixels.pixel, subtype, SUM(coverage) as total_coverage
    FROM input_pixels
    LEFT JOIN read_parquet('{filename}*.parquet') AS read_parquet
    ON input_pixels.pixel = read_parquet.pixel
    GROUP BY input_pixels.pixel, subtype
    """

    result = duckdb.query(query).df()
    pivot_df = result.pivot(index='pixel', columns='subtype', values='total_coverage').fillna(0)
    print(pivot_df)


def get_weiss_value(coords):
    values = []
    with rasterio.open('2020_walking_only_friction_surface.geotiff') as src:
        for (x,y) in coords:
            row, col = src.index(x, y)
            values.append(src.read(1)[row, col])
            print('*')
        return values


#__________________________________________________________________

#pick coords between 85 and -60
step = 0.008333333333333333333

# Calculate number of steps for x and y
x_steps = int((180 - (-180)) / step)
y_steps = int((85 - (-60)) / step)

# Generate 100 random step indices for x and y
coordinates = []
for _ in range(3):
    x_index = random.randint(0, x_steps)
    y_index = random.randint(0, y_steps)
    
    x = -180 + (x_index * step)
    y = -60 + (y_index * step)  # Note: y should go from -60 to 85
    
    coordinates.append((x,y))


#__________________________________________________________


#truth = get_weiss_value(coordinates)
print("----")
def residuals(params):
    #sample = np.array(calculate_speed(coordinates, params))
    return 1#sample - truth


# Initial guess: 30 parameters
initial_guess = np.ones(10)
create_table(coordinates)

#result = least_squares(residuals, initial_guess, loss='linear', max_nfev=1)  # use 'soft_l1' for robustness

print(result.x)
with open('optimized_parameters.csv', 'w', newline='') as f:
    csv.writer(f).writerow(result.x)


