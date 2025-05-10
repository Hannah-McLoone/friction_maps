from shapely.geometry import LineString
#from values import ANGLE
ANGLE = 1
import pandas as pd
from shapely.wkb import dumps
import pyarrow.parquet as pq
import json


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))# fix this
from main_pipeline.creating_road_speed_table import format_into_road_table




def polygon_to_hex(shape) -> bytes:
    return bytes.fromhex(dumps(LineString(shape), hex=True))

def scale_tuples(point_list):
    return [(p[0] * ANGLE, p[1] * ANGLE) for p in point_list]


def generate_unit_test_data(shapes, subtypes, road_surfaces,speed_limits,given_classes):
    table = pd.DataFrame({'geometry':[polygon_to_hex(shape) for shape in shapes], 'subtype':subtypes, 'road_surface':road_surfaces,'speed_limits':speed_limits,'class':given_classes})
    return table


def compare_dataframes_ignore_order(df1, df2):
    # Sort both by all columns (as tuple), reset index, and compare
    df1_sorted = df1.sort_values(by=list(df1.columns)).reset_index(drop=True)
    df2_sorted = df2.sort_values(by=list(df2.columns)).reset_index(drop=True)
    
    return df1_sorted.equals(df2_sorted)


#--------------------------------------------------------------------------------------------------
#testing that a correct speed is assigned to each road point

#priority is speed limit - overrides other things
shape = [(0.5, 0.5),(0.1,0.1)]
unit_test_data = generate_unit_test_data([scale_tuples(shape)], ['road'], [None],[[{'max_speed':{'value':1,'unit':'kph'}}]],['primary'])
df1 = format_into_road_table(unit_test_data)
df2 = pd.DataFrame({'geometry':[(0,0)], 'speed_kph':[1]})
print(compare_dataframes_ignore_order(df1, df2))

#speed limit in mph
shape = [(0.5, 0.5),(0.1,0.1)]
unit_test_data = generate_unit_test_data([scale_tuples(shape)], ['road'], [None],[[{'max_speed':{'value':1,'unit':'mph'}}]],['primary'])
df1 = format_into_road_table(unit_test_data)
df2 = pd.DataFrame({'geometry':[(0,0)], 'speed_kph':[1.60934]})
print(compare_dataframes_ignore_order(df1, df2))


#subtype
shape = [(0.5, 0.5),(0.1,0.1)]
unit_test_data = generate_unit_test_data([scale_tuples(shape)], ['road'], [None],[None],['motorway'])
df1 = format_into_road_table(unit_test_data)
df2 = pd.DataFrame({'geometry':[(0,0)], 'speed_kph':[113]})
print(compare_dataframes_ignore_order(df1, df2))


#then class
shape = [(0.5, 0.5),(0.1,0.1)]
unit_test_data = generate_unit_test_data([scale_tuples(shape)], ['water'],[[{'value':'paving_stones'}]],[None],[None])
df1 = format_into_road_table(unit_test_data)
df2 = pd.DataFrame({'geometry':[(0,0)], 'speed_kph':[20]})
print(compare_dataframes_ignore_order(df1, df2))


#if class is road or none it looks at road coverage
shape = [(0.5, 0.5),(0.1,0.1)]
unit_test_data = generate_unit_test_data([scale_tuples(shape)], ['road'], [[{'value':'paving_stones'}]],[None],[None])
df1 = format_into_road_table(unit_test_data)
df2 = pd.DataFrame({'geometry':[(0,0)], 'speed_kph':[32]})
print(compare_dataframes_ignore_order(df1, df2))


shape = [(0.5, 0.5),(0.1,0.1)]
unit_test_data = generate_unit_test_data([scale_tuples(shape)], [None], [[{'value':'paving_stones'}]],[None],[None])
df1 = format_into_road_table(unit_test_data)
df2 = pd.DataFrame({'geometry':[(0,0)], 'speed_kph':[32]})
print(compare_dataframes_ignore_order(df1, df2))



#what about speed limit that is None???????????????????????? does this happen


#------------------------------------------------------------------------------------------------

#testing that a single road is assigned to the correct squares

shape = [(0.5, 0.5), (2.5, 0.5)]
unit_test_data = generate_unit_test_data([scale_tuples(shape)], ['road'], [None],[None],['primary'])
df1 = format_into_road_table(unit_test_data)
df2 = pd.DataFrame({'geometry':[(0,0),(2,0)], 'speed_kph':[97,97]})
print(compare_dataframes_ignore_order(df1, df2))


shape = [(1, 0.5), (2.5, 0.5)]
unit_test_data = generate_unit_test_data([scale_tuples(shape)], ['road'], [None],[None],['primary'])
df1 = format_into_road_table(unit_test_data)
df2 = pd.DataFrame({'geometry':[(1,0),(2,0)], 'speed_kph':[97,97]})
print(compare_dataframes_ignore_order(df1, df2))

shape = [(0.5, 0.5),(1.3, 0.5),(1.6, 0.5), (2.5, 0.5)]
unit_test_data = generate_unit_test_data([scale_tuples(shape)], ['road'], [None],[None],['primary'])
df1 = format_into_road_table(unit_test_data)
df2 = pd.DataFrame({'geometry':[(0,0),(1,0),(2,0)], 'speed_kph':[97,97,97]})
print(compare_dataframes_ignore_order(df1, df2))


#------------------------------------------------------------------------------------------------
#motorway is 113
#testing world with multiple roads and speeds
shape1 = [(0.8, 1.8),(1.7, 2.2),(2.2, 1.8)]
shape2 = [(0.5, 1.5),(1.3, 1.5),(1.6, 1.5), (2.5, 1.5)]
shape3 = [(0.5, 0.5),(1.3, 0.5),(1.6, 0.8), (1.6, 1.2),(2.5, 1.2)]
unit_test_data = generate_unit_test_data([scale_tuples(shape1),scale_tuples(shape2),scale_tuples(shape3)], ['road','road','road'], [None,None,None],[None,None,None],['motorway','primary','primary'])
df1 = format_into_road_table(unit_test_data)
df2 = pd.DataFrame({'geometry':[(0,0),(1,0),(0,1),(0,1),(1,1),(1,1),(2,1),(2,1),(2,1),(1,2)], 'speed_kph':[97,97,97,113,97,97,97,97,113,113]})
print(compare_dataframes_ignore_order(df1, df2))