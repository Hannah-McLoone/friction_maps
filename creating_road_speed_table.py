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
ANGLE = 1#0.008333333333333333333

def grid_loc(entry):
    point_set = list(entry.coords)
    return set([(p[0] // ANGLE ,p[1]// ANGLE) for p in point_set])
#how many pixels it is from 0,0





# Assuming `table` is a PyArrow Table read earlie

# Add the 'xmin' column to the table


def extract_speed(row):
    if row['speed_limits'] is None or type(row['speed_limits']) == 'NoneType' or isinstance(row['speed_limits'], (list, dict)) and not row['speed_limits']:  # Check if speed is None or empty
        # implicit speed - on types of road
        if row['class'] is not None:
            return Values.country_road_values[row['class']]
        
        

        if row['subtype'] is not None:
            t = {'rail':Values.railspeed,'water':Values.waterspeed}
            return t[row['subtype']]
        

        #implicit speed on road surface
        if row['road_surface'] is not None:
            surface = row['road_surface'][0].get('value', {})
            return Values.speeds_of_features[surface]
        
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




def create_tables_for_all_files(remote_directory,coord_file):

    df = pd.read_csv(coord_file)
    names_list = df['file_name'].tolist()

    all_tables = []


    n = 0
    # Loop through each file in the names_list
    for file_name in names_list:
        client = create_connection()
        sftp = client.open_sftp()


        print('Processing:', file_name)
        file_path = remote_directory + '/' + file_name
        print(file_path)
        remote_file = sftp.file(file_path, 'rb')

        # Use PyArrow to read the dataset and filter it
        with remote_file as f:

            table = pq.read_table(f,columns=['geometry','subtype','road_surface','speed_limits','class'], filters=[[('class', 'in', list(Values.country_road_values.keys()))], [('subtype', 'in', ['rail','water'])]])
            table = table.to_pandas()
        client.close()

        mega_table = format_into_road_table(table)
        mega_table.to_parquet(f'higher_granularity_output/pixel_to_road_speed{n}.parquet', index=False)
        n = n+1




def format_into_road_table(table):
    table['speed_kph'] = table.apply(extract_speed, axis=1)#change this to a series of .map ?
    table['geometry'] = table['geometry'].map(wkb.loads)
    table['geometry'] = table['geometry'].map(grid_loc)


    #need to write geometry as seperate columns for max efficiency!!!!!!!!!!

    mega_table = table[['geometry','speed_kph']].explode('geometry')
    return(mega_table)



def turn_overture_into_road_table(f):
    table = pq.read_table(f,columns=['geometry','subtype','road_surface','speed_limits','class'], filters=[[('class', 'in', list(Values.country_road_values.keys()))], [('subtype', 'in', ['rail','water'])]])
    table = table.to_pandas()
    return format_into_road_table(table)




