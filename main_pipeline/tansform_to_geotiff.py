import h5py
import rasterio
from rasterio.transform import from_origin
from rasterio.crs import CRS
#change this so that it can work at different resolutions!!!!!!! change res to angle

def transform_to_geotiff(h5_file_name, tif_file_name):
    # Load the 2D array from the HDF5 file
    with h5py.File(h5_file_name, "r") as f:
        # Assuming the only dataset is the array
        dataset_name = list(f.keys())[0]
        data = f[dataset_name][()]

    # Resolution in degrees (30 arcseconds = 1/120 degrees)
    res = 1 / 120

    # Define the top-left corner. Assuming global coverage from (90N, -180W)
    top_left_lon = -180
    top_left_lat = 90

    # Create the geotransform
    transform = from_origin(top_left_lon, top_left_lat, res, res)

    # Define the CRS (WGS84)
    crs = CRS.from_epsg(4326)

    # Write the GeoTIFF
    with rasterio.open(
        tif_file_name,
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
