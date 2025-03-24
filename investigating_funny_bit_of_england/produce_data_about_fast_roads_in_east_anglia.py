#this code takes 10 min for 1 file!!!!!!!!

from shapely import wkb

import pandas as pd
import paramiko
import os
import re
import pyarrow.parquet as pq
import pyarrow.dataset as ds
import io
import time
from values import Values, water_values#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import math


def temp(entry):
    point_set = list(entry.coords)
    return (point_set[0][0] // 0.008333333333333333333 < 220)



def get_speed_lim(row):
    if row['speed_limits'] is None or type(row['speed_limits']) == 'NoneType' : 
        return 0
    max_speed = row['speed_limits'][0].get('max_speed', {})  # Safely get 'max_speed' dictionary

    if max_speed is not None:
        value = max_speed.get('value')
        unit = max_speed.get('unit')

        if unit == 'kph':
            return value
        else:
            return value * 1.60934
        
    return 0



def get_road_surface(row):
    if row['road_surface'] is not None:
        return row['road_surface'][0].get('value', {})

def filter():
    pass

# Assuming `table` is a PyArrow Table read earlie

# Add the 'xmin' column to the table


def extract_speed(row):
    if row['speed_limits'] is None or type(row['speed_limits']) == 'NoneType' :  # Check if speed is None or empty
        # implicit speed - on types of road
        if row['class'] is not None:
            if row['class'] != 'unknown' and row['class'] != 'unclassified':
                return Values.country_road_values[row['class']]
        
        

        if row['subtype'] is not None:
            if row['subtype'] != 'road':
                t = {'rail':Values.railspeed,'water':Values.waterspeed}
                return t[row['subtype']]
        

        #implicit speed on road surface
        if row['road_surface'] is not None:
            surface = row['road_surface'][0].get('value', {})
            return Values.speeds_of_features[surface]

            #KeyError: 'unknown'
        
        return 0




    max_speed = row['speed_limits'][0].get('max_speed', {})  # Safely get 'max_speed' dictionary

    if max_speed is not None:
        value = max_speed.get('value')
        unit = max_speed.get('unit')

        if unit == 'kph':
            return value
        else:
            return value * 1.60934
        
    return 0









def make_csv_for_grid(remote_directory,query_type,coord_file):

    df = pd.read_csv(coord_file)
    names_list = df['file_name'].tolist()

    # Loop through each file in the names_list
    for file_name in [names_list[35]]:
        client = create_connection()
        sftp = client.open_sftp()


        print('Processing:', file_name)
        file_path = remote_directory + '/' + file_name
        print(file_path)
        remote_file = sftp.file(file_path, 'rb')

        # Use PyArrow to read the dataset and filter it
        with remote_file as f:

            table = pq.read_table(f,columns=['id','geometry','subtype','road_surface','speed_limits','class'], filters=[[('class', 'in', list(Values.country_road_values.keys()))], [('subtype', 'in', ['rail','water'])]])
            table = table.to_pandas()
            client.close()

        #only use ones in england
        table['geometry'] = table['geometry'].map(wkb.loads)
        table['bool'] = table['geometry'].map(temp)
        table = table[table['bool'] == True]



        table['speed_kph'] = table.apply(extract_speed, axis=1)#change this to a series of .map ?
        table = table[table['speed_kph'] >= 96]

        table['road_surface'] = table.apply(get_road_surface, axis=1)
        table['speed_limits'] = table.apply(get_speed_lim, axis=1)
        table.to_csv(f'data_about_fast_roads_in_East_Anglia.csv', index=False)

#finished n = 24

# Configuration
hostname = 'sherwood.cl.cam.ac.uk'  # or 'kinabalu.cl.cam.ac.uk'
port = 22  # Default SSH port
username = 'hm708'  # Replace with your actual CSRid
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




start_time = time.time()

make_csv_for_grid('/maps/sj514/overture/theme=transportation/type=segment','transport', "file_cords_of_transport.csv")

end_time = time.time()

print(end_time - start_time)
