import duckdb
import pandas as pd
import numpy as np
import time
import h5py


"""
need to rotate this 90 degrees anticlockwise!!!!!!!
reformat my arrays rows and columns?
"""

def create_friction_map_for_section(x_n, y_n,xangle,yangle,filename):
    resolution = 1 # how many km in square #########change back to 1
    angle = 0.008333333333333333333 / resolution
    duckdb.query("PRAGMA threads=8") 



    i_vals = np.arange(int(xangle //angle), int(xangle //angle + x_n))
    j_vals = np.arange(int(yangle //angle), int(yangle //angle + y_n))
    x_grid, y_grid = np.meshgrid(i_vals, j_vals, indexing="ij")

    geometries = np.stack([x_grid, y_grid], axis=-1)
    geometries = np.rot90(geometries)#**********



    flat_geometries = [f"[{x}, {y}]" for x, y in geometries.reshape(-1, 2)] # this is the slow line!

    df = pd.DataFrame({"geometry": flat_geometries})
    df['original_index'] = df.index

    duckdb.query("DROP TABLE IF EXISTS input_geometries; CREATE TEMP TABLE input_geometries (geometry TEXT, original_index INTEGER)")
    duckdb.query("INSERT INTO input_geometries SELECT geometry, original_index FROM df")

    #change to higher granularity output if i want that
    query = f"""
    SELECT input_geometries.geometry, COALESCE(MAX(read_parquet.speed_kph), 0) AS max_speed
    FROM input_geometries
    LEFT JOIN read_parquet('{filename}*.parquet') AS read_parquet
    ON input_geometries.geometry = read_parquet.pixel
    GROUP BY input_geometries.geometry, input_geometries.original_index
    ORDER BY input_geometries.original_index
    """

    result = duckdb.query(query).df()
    #print(flat_geometries)

    def break_list_into_sublists_numpy(array, n):
        return np.array_split(array, n)

    result = break_list_into_sublists_numpy(np.array(result['max_speed']), y_n)


    return np.array(result)


if __name__ == "__main__":

    start_time = time.time()

    resolution = 1 # how many km in square#########################change
    angle = 0.008333333333333333333 / resolution

    y_angle = 58 - 500 * angle #delete the change 58 to 90!!!!!!!!!!!!!!!!!!
    y2_angle = y_angle - 500 * angle
    print(y2_angle)

    rows = int(180 / angle)
    cols = int(360 / angle)

    # Create HDF5 file
    with h5py.File('final_roads.h5', 'w') as hdf5_file:
        # Create datasets with specified dimensions and chunking
        var = hdf5_file.create_dataset('data', (0, cols), maxshape=(None, cols), dtype='f4', chunks=(500, cols), compression='gzip')

        while y2_angle > 49:#meant to be -90!!!!!!!!!!!!!!!!!!!!
            print(y2_angle)
            #result_array = create_friction_map_for_section(360 / angle,500, -180, y_angle,'output2/increased_resolution_pixel_to_road_speed')  # Assuming this function is defined elsewhere
            result_array = create_friction_map_for_section(8 / angle, 500, -6, y_angle,'output/pixel_to_road_speed') 
            #print(result_array)
            result_rows, cols = result_array.shape
            y_angle = y2_angle
            y2_angle = y2_angle - 500 * angle

            # Append result_array to the dataset
            var.resize((var.shape[0] + result_rows, cols))  # Resize the dataset to accommodate new data
            var[-result_rows:, :] = result_array  # Append without full read

    print(time.time() - start_time)





#58 to 50n
#6 west to 2 east