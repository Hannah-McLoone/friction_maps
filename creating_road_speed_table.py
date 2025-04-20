#this code takes 10 min for 1 file!!!!!!!!

from shapely import wkb

import pandas as pd
import pyarrow.parquet as pq
import pyarrow.dataset as ds
import io
import time
from values import Values#, water_values#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import sys
ANGLE = 0.008333333333333333333 / 5 # 30/3600

def grid_loc(entry):#how many pixels it is from 0,0
    point_set = list(entry.coords)
    return set([(p[0] // ANGLE ,p[1]// ANGLE) for p in point_set])


def extract_speed(row):
    if row['subtype'] == 'rail':
        return Values.railspeed
    return Values.country_road_values[row['class']] # delete!!!!!!!!!!
    speed_lim = -1

    if row['speed_limits'] is not None:  # Check if there is a speed limit
        max_speed = row['speed_limits'][0].get('max_speed', {})  # Safely get 'max_speed' dictionary

        if max_speed != None and max_speed != {}:
            value = max_speed.get('value')
            unit = max_speed.get('unit')

            if unit == 'kph':
                speed_lim = value
            else:
                speed_lim = value * 1.60934




    #limit by speed limit

    # implicit speed - on types of road
    if row['class'] is not None and row['class'] != 'unknown' and row['class'] != 'track':

        if speed_lim != -1:
            return min(speed_lim, Values.country_road_values[row['class']])
        return Values.country_road_values[row['class']]
    
    #anything else is extension from weisse
    #implicit speed on road surface
    if row['road_surface'] is not None:
        surface = row['road_surface'][0].get('value', {})

        if speed_lim != -1:
            return min(speed_lim, Values.speeds_of_features[surface])
        return Values.speeds_of_features[surface]
    
    
    return 0


def format_into_road_table(table):
    table['speed_kph'] = table.apply(extract_speed, axis=1)#change this to a series of .map ?
    table['geometry'] = table['geometry'].map(wkb.loads)
    table['pixel'] = table['geometry'].map(grid_loc)
    table = table.drop(['geometry'], axis = 1)


    #need to write pixel as seperate columns for max efficiency!!!!!!!!!!

    mega_table = table[['pixel','speed_kph']].explode('pixel')
    return(mega_table)



def turn_overture_into_road_table(f):
    table = pq.read_table(f,columns=['geometry','subtype','road_surface','speed_limits','class'], filters=[[('class', 'in', list(Values.country_road_values.keys()))], [('subtype', 'in', ['rail','water'])]])
    table = table.to_pandas()
    return format_into_road_table(table)




if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script <arg1> <arg2>")
    else:
        arg1, arg2 = sys.argv[1], sys.argv[2]
        table = turn_overture_into_road_table(arg1)
        table.to_parquet(arg2, index=False)
