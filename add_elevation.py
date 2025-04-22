import rasterio
from rasterio import Affine
from rasterio.enums import Resampling
import numpy as np

def toblers_walking_speed(slope):
    slope_rad = np.radians(slope)
    adjusted_slope = np.abs(np.tan(slope_rad) + 0.05)
    return 6 * np.exp(-3.5 * adjusted_slope)

def elevation_adjustment(elevation):
    return 1.016 * np.exp(-0.0001072 * elevation)




slope_file = 'slope_1KMmd_SRTM.tif'
elevation_file = 'slope_1KMmd_SRTM.tif'

with rasterio.open(slope_file) as src:
    profile = src.profile
    slope_data = src.read(1)  # there is only one band

with rasterio.open(elevation_file) as src:
    profile = src.profile
    elevation_data = src.read(1)  # there is only one band

# Apply the function to the slope data
walking_speed = toblers_walking_speed(slope_data)
slope_adjustment_factor = walking_speed/5

elevation_factor = elevation_adjustment(elevation_data)

























# Get dimensions
height, width = data.shape

# Define window size (e.g., 10x10 pixels)
win_size = 10

# Calculate center position
center_y = height // 5
center_x = width // 5

# Calculate bounds of the window
start_y = center_y - win_size // 5
start_x = center_x - win_size // 5
end_y = start_y + win_size
end_x = start_x + win_size

# Extract center window (for the first band or all bands if needed)
center_window = walking_speed[start_y:end_y, start_x:end_x]  # Shape: (bands, 10, 10)

# For example, print the first band of the center window
print("Center window (Band 1):")
print(center_window)




#divide by elevation factor
#divide by slope factor