import duckdb
import pandas as pd
import numpy as np
import time
import h5py
from main_pipeline.values import ANGLE
import sys

"""
currently rotate this 90 degrees anticlockwis - reformat my arrays rows and columns?

polish up by making angle into ANGLE
"""

def create_friction_map_for_section(x_n, y_n,xangle,yangle,filename,selection):
    resolution = 1 # how many km in square
    angle = 0.008333333333333333333 / resolution

    duckdb.query("PRAGMA threads=8") 



    i_vals = np.arange(int(xangle //angle), int(xangle //angle + x_n))
    j_vals = np.arange(int(yangle //angle), int(yangle //angle + y_n))
    x_grid, y_grid = np.meshgrid(i_vals, j_vals, indexing="ij")

    pixels = np.stack([x_grid, y_grid], axis=-1)
    pixels = np.rot90(pixels)#***



    flat_pixels = [f"[{x}, {y}]" for x, y in pixels.reshape(-1, 2)] # this could be made faster by formatting x and y better

    df = pd.DataFrame({"pixel": flat_pixels})
    df['original_index'] = df.index

    duckdb.query("DROP TABLE IF EXISTS input_pixels; CREATE TEMP TABLE input_pixels (pixel TEXT, original_index INTEGER)")
    duckdb.query("INSERT INTO input_pixels SELECT pixel, original_index FROM df")

    #change to higher granularity output if i want that
    query = f"""
    {selection}
    FROM input_pixels
    LEFT JOIN read_parquet('{filename}*.parquet') AS read_parquet
    ON input_pixels.pixel = read_parquet.pixel
    GROUP BY input_pixels.pixel, input_pixels.original_index
    ORDER BY input_pixels.original_index
    """

    result = duckdb.query(query).df()

    def break_list_into_sublists_numpy(array, n):
        return np.array_split(array, n)

    result = break_list_into_sublists_numpy(np.array(result['speed']), y_n)


    return np.array(result)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script <input_suffix> <output_file> <type_of_friction_map>")
    else:
        input_suffix, output_file, type_of_friction_map = sys.argv[1], sys.argv[2]
        #example: input_suffix = 'output/pixel_to_road_speed' or 'maps/hm708/processed_land'
        #         type_of_friction_map = 'transportation'
        #output_file must be h5 - 'road_friction_map.h5'
        
        start_time = time.time()

        #change all of these to ANGLE
        resolution = 1 # how many km in square
        angle = 0.008333333333333333333 / resolution


        y_angle = 90 - 500 * 0.008333333333333333333

        rows = int(180 / 0.008333333333333333333)
        cols = int(360 / 0.008333333333333333333)

        if type_of_friction_map == 'transportation':
            selection = "SELECT input_pixels.pixel, COALESCE(MAX(read_parquet.speed_kph), 0) AS speed"
        else:
            selection = "SELECT input_pixels.pixel, COALESCE(SUM(read_parquet.speed * read_parquet.coverage) / NULLIF(SUM(read_parquet.coverage), 0), 0) AS speed"

        # Create HDF5 file
        with h5py.File(output_file, 'w') as hdf5_file:
            # Create datasets with specified dimensions and chunking
            var = hdf5_file.create_dataset('data', (0, cols), maxshape=(None, cols), dtype='f4', chunks=(500, cols), compression='gzip')

            while y_angle > -90:
                print(y_angle)
                result_array = create_friction_map_for_section(360 / angle,500, -180, y_angle, input_suffix , selection)
                result_rows, cols = result_array.shape

                # Append result_array to the dataset
                var.resize((var.shape[0] + result_rows, cols))  # Resize the dataset to accommodate new data
                var[-result_rows:, :] = result_array  # Append without full read

                y_angle = y_angle  - 500 * 0.008333333333333333333

            remainder = (500 - (-90-y_angle)//angle )
            result_array = create_friction_map_for_section(360 / angle,remainder, -180, -90, input_suffix, selection)
            result_rows, cols = result_array.shape
            var.resize((var.shape[0] + result_rows, cols))
            var[-result_rows:, :] = result_array 

        print(time.time() - start_time)
