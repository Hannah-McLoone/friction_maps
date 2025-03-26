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
from creating_road_speed_table import format_into_table




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



shape = [(0.5, 0.5), (2.5, 0.5)]
unit_test_data = generate_unit_test_data([scale_tuples(shape)], ['road'], [None],[None],['primary'])
df1 = format_into_table(unit_test_data)
df2 = pd.DataFrame({'geometry':[(0,0),(2,0)], 'speed_kph':[97,97]})
print(compare_dataframes_ignore_order(df1, df2))


shape = [(1, 0.5), (2.5, 0.5)]
unit_test_data = generate_unit_test_data([scale_tuples(shape)], ['road'], [None],[None],['primary'])
df1 = format_into_table(unit_test_data)
df2 = pd.DataFrame({'geometry':[(1,0),(2,0)], 'speed_kph':[97,97]})
print(compare_dataframes_ignore_order(df1, df2))

shape = [(0.5, 0.5),(1.3, 0.5),(1.6, 0.5), (2.5, 0.5)]
unit_test_data = generate_unit_test_data([scale_tuples(shape)], ['road'], [None],[None],['primary'])
df1 = format_into_table(unit_test_data)
df2 = pd.DataFrame({'geometry':[(0,0),(1,0),(2,0)], 'speed_kph':[97,97,97]})
print(compare_dataframes_ignore_order(df1, df2))
