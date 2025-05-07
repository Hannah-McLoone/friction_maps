import rasterio
from rasterio import Affine
from rasterio.enums import Resampling
import numpy as np

def toblers_walking_speed(slope):
    slope_rad = np.radians(slope)
    adjusted_slope = np.abs(np.tan(slope_rad) + 0.05)
    return min(5,6 * np.exp(-3.5 * adjusted_slope))

def elevation_adjustment(elevation):
    return 1.016 * np.exp(-0.0001072 * elevation)



slope_file = 'slope_1KMmd_SRTM.tif'
elevation_file = 'elevation_1KMmd_SRTM.tif'
my_data_path = 'road_friction_map.tif'

with rasterio.open(slope_file) as src:
    profile = src.profile
    slope_data = src.read(1)  # there is only one band

with rasterio.open(elevation_file) as src:
    profile = src.profile
    elevation_data = src.read(1)  # there is only one band

with rasterio.open(my_data_path) as src:
    profile = src.profile
    my_data = src.read(1)  # there is only one band

# Apply the function to the slope data
walking_speed = toblers_walking_speed(slope_data)
slope_adjustment_factor = walking_speed/5

elevation_factor = elevation_adjustment(elevation_data)


scale = slope_adjustment_factor * elevation_factor

total_rows = my_data.shape[0]
rows_per_degree = total_rows // 180 
start_row = 30 * rows_per_degree  # 90°N to 60°N = 30°
end_row = 150 * rows_per_degree   # 90°N to 60°S = 150°

# Create a new scale array for the whole world
full_scale = np.ones_like(my_data, dtype=np.float32)
full_scale[start_row:end_row, :] = scale

# Apply scaling
data = my_data * full_scale
