#uses land_cover. do i want land cover or land???
# creating the files

"""
this code can be used to create 2 files:
pixel_to_id
and id_to_info
"""


import pandas as pd
import paramiko
import os
import re
import pyarrow.parquet as pq
import pyarrow.dataset as ds
import io
import time
from filter_x_y import filter_xy, filter_by_area_deprecated
from values import Values, water_values
import numpy as np

from values import Land_values


def generate_coordinates(bbox):
    x_values = np.arange(bbox['xmin']//0.008333333333333333333, bbox['xmax']//0.008333333333333333333)
    y_values = np.arange(bbox['ymin']//0.008333333333333333333, bbox['ymax']//0.008333333333333333333)

    # Stack and reshape into a list of coordinate pairs
    x_grid, y_grid = np.meshgrid(x_values, y_values, indexing="ij")
    geometries = np.stack([x_grid, y_grid], axis=-1)
    flat_geometries = [f"[{x}, {y}]" for x, y in geometries.reshape(-1, 2)]


    return flat_geometries



def land_speed(subtype):#,given_class):
    return Land_values.land_type_speeds.get(subtype, 1)



def make_csv_for_grid(remote_directory,coord_file, output_file):

    df = pd.read_csv(coord_file)

    # select files that have points in the box (according to bounding coord file) 
    names_list = df['file_name'].tolist()


    # Loop through each file in the names_list
    n = 50
    for file_name in names_list[50:]:
        print(n)
        print('Processing:', file_name)

        client = create_connection()
        sftp = client.open_sftp()
        file_path = remote_directory + '/' + file_name
        print(file_path)
        remote_file = sftp.file(file_path, 'rb')

        # Use PyArrow to read the dataset and filter it
        with remote_file as f:
            table = pq.read_table(f,columns=['id','bbox', 'geometry', 'subtype'])#geometry, subtype
        client.close()
        table = table.to_pandas()

        table['subtype'] = table['subtype'].map(land_speed)
        #table['bbox'] = table['bbox'].map(generate_coordinates)

        df['pix_coverage'] = np.vectorize(generate_coordinates)(df['bbox'], df['geometry'])
        #drop geometry column

        table.rename(columns={'subtype': 'speed'}, inplace=True)

        table = table.explode('bbox')

        table.to_parquet(output_file +str(n)+ '.parquet', index=False)
        n = n+1


# Configuration
hostname = 'sherwood.cl.cam.ac.uk'  # or 'kinabalu.cl.cam.ac.uk'
port = 22  # Default SSH port
username = 'hm708' 
private_key_path = '/Users/hanna/.ssh/id_rsa'  # Path to your private key file

def create_connection():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
        client.connect(hostname, port=port, username=username, pkey=private_key)
        return client
    except Exception as e:
        print(f'An error occurred: {e}')



client = create_connection()
start_time = time.time()
make_csv_for_grid('/maps/sj514/overture/theme=base/type=land_cover', "file_cords_of_land.csv",'pixel_to_id')
end_time = time.time()
print(end_time - start_time)

