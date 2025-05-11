import rasterio
from rasterio import Affine
from rasterio.enums import Resampling
import numpy as np
from rasterio.transform import from_origin
from rasterio.crs import CRS
import sys

def toblers_walking_speed(slope):
    slope_rad = np.radians(slope)
    adjusted_slope = np.abs(np.tan(slope_rad) + 0.05)
    return min(5,6 * np.exp(-3.5 * adjusted_slope))

def elevation_adjustment(elevation):
    return 1.016 * np.exp(-0.0001072 * elevation)


def apply_scaling_to_data(my_data_path = 'land_friction_map.tif'
, slope_file = 'slope_1KMmd_SRTM.tif', elevation_file = 'elevation_1KMmd_SRTM.tif', output_file = 'scaled_land_friction_map.tif'):

    with rasterio.open(slope_file) as src:
        profile = src.profile
        slope_data = src.read(1)  # there is only one band

    with rasterio.open(elevation_file) as src:
        profile = src.profile
        elevation_data = src.read(1)

    with rasterio.open(my_data_path) as src:
        profile = src.profile
        my_data = src.read(1)

    walking_speed = toblers_walking_speed(slope_data)
    slope_adjustment_factor = walking_speed/5

    elevation_factor = elevation_adjustment(elevation_data)


    scale = 1 / (slope_adjustment_factor * elevation_factor)

    #the elevation and slope data i am using only has data between the latitudes of 60 and -60
    # this assumes my_data is same shape as elevation
    #need other data source for other resolutions
    total_rows = my_data.shape[0]
    rows_per_degree = total_rows // 180 
    start_row = 30 * rows_per_degree  # 90°N to 60°N = 30°
    end_row = 150 * rows_per_degree   # 90°N to 60°S = 150°

    # add 1's to array (to be no scaling) outside the limits of the dad
    full_scale = np.ones_like(my_data, dtype=np.float32)
    full_scale[start_row:end_row, :] = scale

    # Apply scaling
    data = my_data * full_scale



    res = 1 / 120
    top_left_lon = -180
    top_left_lat = 90
    transform = from_origin(top_left_lon, top_left_lat, res, res)
    crs = CRS.from_epsg(4326)

    # Write the GeoTIFF
    with rasterio.open(
        output_file,
        "w",
        driver="GTiff",
        height=data.shape[0],
        width=data.shape[1],
        count=1,
        dtype=data.dtype,
        crs=crs,
        transform=transform,
    ) as dst:
        dst.write(data, 1)



if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script <my_data_path> <slope_file> <elevation_file> <output_file>")
    else:
        my_data_path, slope_file, elevation_file, output_file = sys.argv[1], sys.argv[2],  sys.argv[3],  sys.argv[4]
        apply_scaling_to_data(my_data_path, slope_file, elevation_file, output_file)
