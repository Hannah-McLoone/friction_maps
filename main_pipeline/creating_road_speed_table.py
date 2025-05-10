from shapely import wkb

import pandas as pd
import pyarrow.parquet as pq
import pyarrow.dataset as ds
import io
import time
from values import Transport_values
import sys
from values import ANGLE # again, need to override this with 1

def grid_loc(entry):#how many pixels it is from 0,0
    point_set = list(entry.coords)
    return set([(p[0] // ANGLE ,p[1]// ANGLE) for p in point_set])


def extract_speed(row):
    if row['subtype'] == 'rail':
        return Transport_values.railspeed
    
    speed_lim = -1
    if row['speed_limits'] is not None:  # Check if there is a speed limit
        max_speed = row['speed_limits'][0].get('max_speed', {})  # Safely get 'max_speed' dictionary

        if max_speed is not None and max_speed != {}:
            value = max_speed.get('value')
            unit = max_speed.get('unit')

            if unit == 'kph':
                speed_lim = value
            else:
                speed_lim = value * 1.60934

    #limit by speed limit

    # implicit speed - on types of road
    if row['class'] is not None:
        if speed_lim != -1:
            return min(speed_lim, Transport_values.country_road_values_glob_avg[row['class']])
        return Transport_values.country_road_values_glob_avg[row['class']]
    
    #anything else is extension from weisse. as stated earlier i am trying to mimic his results
    #but if one wanted to use other information, it is here
    #example of implicit speed on road surface, would need to have a mapping in the balues program
    """
    if row['road_surface'] is not None:
        surface = row['road_surface'][0].get('value', {})

        if speed_lim != -1:
            return min(speed_lim, Transportation_values.speeds_of_features[surface])
        return Transportation_values.speeds_of_features[surface]
    """
    
    #in case a row lacks class data - not observed, just a failsafe
    return 0


def format_into_road_table(table):
    table['speed_kph'] = table.apply(extract_speed, axis=1)
    table['geometry'] = table['geometry'].map(wkb.loads)
    table['pixel'] = table['geometry'].map(grid_loc)
    table = table.drop(['geometry'], axis = 1)


    mega_table = table[['pixel','speed_kph']].explode('pixel')
    return(mega_table)



def turn_overture_into_road_table(f):
    table = pq.read_table(f,columns=['geometry','subtype','road_surface','speed_limits','class'], filters=[[('class', 'in', list(Transport_values.country_road_values_glob_avg.keys()))], [('subtype', 'in', ['rail'])]])
    table = table.to_pandas()
    return format_into_road_table(table)




if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script <arg1> <arg2>")
    else:
        arg1, arg2 = sys.argv[1], sys.argv[2]
        table = turn_overture_into_road_table(arg1)
        table.to_parquet(arg2, index=False)
