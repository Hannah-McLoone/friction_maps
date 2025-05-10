import numpy as np
from scipy.optimize import least_squares
import duckdb
import rasterio
import random
import csv
import pandas as pd
from sklearn.model_selection import train_test_split


"""
extension:
choose specific sub areas
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
    result = result[result['subtype'] != 'land']
    pivot_df = result.pivot(index='pixel', columns='subtype', values='total_coverage').fillna(0)
    for col in ["barren", "crop", "forest", "grass", "mangrove", "moss", "shrub", "snow", "urban", "wetland","desert","glacier", "physical", "reef", "rock","sand","tree"]:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
    
    pivot_df.fillna(0, inplace=True)
    pivot_df = pivot_df.loc[cord_list].reset_index()

    #if 'land' in pivot_df['pixel'].values:
    #    pivot_df = pivot_df[pivot_df['pixel'] != 'land']

    return(pivot_df)


def toblers_walking_speed(slope):
    slope_rad = np.radians(slope)
    adjusted_slope = np.abs(np.tan(slope_rad) + 0.05)
    return min(5,6 * np.exp(-3.5 * adjusted_slope))

def elevation_adjustment(elevation):
    return 1.016 * np.exp(-0.0001072 * elevation)



def get_weiss_value(coords): # these are float coords
    values = []
    resolution = 0.008333333333333333333

    with rasterio.open('2020_walking_only_friction_surface.geotiff') as src:
        band1 = src.read(1)
        index = src.index
        for x, y in coords:
            col, row = index(x * resolution, y * resolution)
            values.append(band1[col,row])#


    with rasterio.open('/maps/hm708/slope_1KMmd_SRTM.tif') as src:
        band1 = src.read(1)
        index = src.index
        for i in range(0, len(coords)):
            x,y = coords[i]
            col, row = index(x * resolution, y * resolution)
            slope_scaling = toblers_walking_speed(band1[col, row]) / 5
            values[i] = values[i] * slope_scaling

    with rasterio.open('/maps/hm708/elevation_1KMmd_SRTM.tif') as src:
        band1 = src.read(1)
        index = src.index
        for i in range(0, len(coords)):
            x,y = coords[i]
            col, row = index(x * resolution, y * resolution)
            elevation_scaling = elevation_adjustment(band1[col,row])
            values[i] = values[i] * elevation_scaling
    print('finished creating weiss values')
    return values


def calculate_speed(table, params):
    #sum of speed * coverage / sum of coverage
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
        "wetland": params[9],   


        "desert": params[10],
        "glacier": params[11],
        "physical": params[12],
        "reef": params[13],
        "rock": params[14],
        "sand": params[15],
        "tree": params[16]
    }
    speed_series = pd.Series(landtype_to_speed)

    # Select only land type columns
    land_columns = list(landtype_to_speed.keys())

    # Calculate weighted sum and total coverage
    weighted_sum = table[land_columns].mul(speed_series)
    coverage_sum = table[land_columns].sum(axis=1)
    weighted_avg_speed = np.where(coverage_sum == 0, 0, weighted_sum.sum(axis=1) / coverage_sum)#call this something better now it is min per mitre
    weighted_avg_speed[weighted_avg_speed == 0] = 0.1
    weighted_avg_speed = 60 / (weighted_avg_speed* 1000)
    return weighted_avg_speed
    

resolution = 0.008333333333333333
coordinates = []

# Generate 100,000 random coordinates
for _ in range(5000000):
    x = random.uniform(60,110)#(-179.9, 179.9)
    y = random.uniform(40,60)#(-59.9, 84.9)
    coordinates.append((x // resolution, y // resolution))

for _ in range(2000000):
    x = random.uniform(100,125)#(-179.9, 179.9)
    y = random.uniform(0,20)#(-59.9, 84.9)
    coordinates.append((x // resolution, y // resolution))


for _ in range(3000000):
    x = random.uniform(-80,-50)#(-179.9, 179.9)
    y = random.uniform(-10,10)#(-59.9, 84.9)
    coordinates.append((x // resolution, y // resolution))






# Get the corresponding truth values
truth = get_weiss_value(coordinates)

# Split into train and test sets
coords_train, coords_test, truth_train, truth_test = train_test_split(
    coordinates, truth, test_size=0.2, random_state=42
)

# Define residuals function using training data
def residuals(params):
    sample = np.array(calculate_speed(table_train, params))
    return sample - truth_train

# Optimization
initial_guess = np.ones(17)
table_train = create_table(coords_train)
table_test = create_table(coords_test)




print('starting least squares')
result = least_squares(residuals, initial_guess, loss='linear')

# Save result
print(result.x)

# Optionally: Evaluate on test set
predicted_test = calculate_speed(table_test, result.x)

df = pd.DataFrame({"predicted": predicted_test, "actual": truth_test})
df.to_csv("predicted_vs_actual.csv", index=False)

error = np.array(predicted_test) - np.array(truth_test)
print('Test RMSE:', np.sqrt(np.mean(error**2)))

pd.Series(result.x).to_csv("optimized_parameters.csv", index=False, header=False)
