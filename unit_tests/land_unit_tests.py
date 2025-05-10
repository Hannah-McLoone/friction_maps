from shapely.geometry import Polygon, MultiPolygon
#from values import ANGLE
ANGLE = 1
import pandas as pd
from shapely.wkb import dumps
import pyarrow.parquet as pq
import json
import numpy as np
#questions from this:
#how i want to index pixels
#underflow? printing off small values rounds inccorecclty, is it being stored correctly?


"""
need to change speeds so they match current values


"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))# fix this
from creating_land_coverage_table import format_into_land_table





s = ANGLE # do i want to do something about this?
def scale_tuples(point_list):
    return [(p[0] * ANGLE, p[1] * ANGLE) for p in point_list]



def create_bounding_box(shape):
    xmin = min([p[0] for p in shape])
    xmax = max([p[0] for p in shape])
    ymin = min([p[1] for p in shape])
    ymax = max([p[1] for p in shape])
    return({'xmin': xmin, 'xmax':xmax, 'ymin':ymin, 'ymax':ymax })


#def polygon_to_hex(shape) -> str:
#    return dumps(Polygon(shape), hex=True)

def polygon_to_hex(shape) -> bytes:
    #return bytes.fromhex(dumps(Polygon(shape), hex=True))
    shape2 = [(5, 6), (6.5, 5), (5, 4), (3.5, 5)]
    shape1 = [(1.5, 3), (3, 1.5), (1.5, 0), (0, 1.5)]

    # Create a MultiPolygon
    multi = MultiPolygon([Polygon(shape1), Polygon(shape2)])

    # Get the WKB hex representation and convert to bytes
    return bytes.fromhex(dumps(multi, hex=True))

def generate_unit_test_data(shapes, subtypes):
    table = pd.DataFrame({'geometry':[polygon_to_hex(shape) for shape in shapes], 'bbox':[create_bounding_box(shape) for shape in shapes], 'subtype':subtypes})
    #table.to_parquet(f'unit_test{id}.parquet', index=False)
    return table






import numpy as np

def convert_unhashables_to_tuples(df):
    df_converted = df.copy()
    for col in df_converted.columns:
        if df_converted[col].dtype == 'object':
            df_converted[col] = df_converted[col].apply(
                lambda x: tuple(x) if isinstance(x, (np.ndarray, list)) else x
            )
    return df_converted




def compare_dataframes_ignore_order(df1, df2):
    df1_clean = convert_unhashables_to_tuples(df1)
    df2_clean = convert_unhashables_to_tuples(df2)

    # Ensure columns are in the same order
    if set(df1_clean.columns) != set(df2_clean.columns):
        return False

    common_columns = sorted(df1_clean.columns)
    df1_clean = df1_clean[common_columns].round(3)
    df2_clean = df2_clean[common_columns].round(3)


    # Sort rows and compare
    df1_sorted = df1_clean.sort_values(by=common_columns).reset_index(drop=True)
    df2_sorted = df2_clean.sort_values(by=common_columns).reset_index(drop=True)

    return df1_sorted.equals(df2_sorted)




#_________________________________________________________________
#grass = 12
#forest = 5

shape = [(1.5, 3), (3, 1.5), (1.5, 0), (0, 1.5)]
unit_test_data = generate_unit_test_data([scale_tuples(shape)], subtypes = ['grass'])
df1 = format_into_land_table(unit_test_data)
pixels = [[0,0],[1,0],[2,0],[0,1],[1,1],[2,1],[0,2],[1,2],[2,2]]
speeds = [12,12,12,12,12,12,12,12,12]
coverage = [1/8,6/8,1/8,6/8,1,6/8,1/8,6/8,1/8]
df2 = pd.DataFrame({'pixel':pixels, 'coverage':coverage,'speed':speeds})
print(compare_dataframes_ignore_order(df1, df2))
print(df1)

print(df2)


"""
shape = [(1.5, 3), (3, 1.5), (1.5, 0), (0, 1.5)]
unit_test_data = generate_unit_test_data([scale_tuples(shape)], subtypes = ['grass'])
df1 = format_into_land_table(unit_test_data)
pixels = [[0,0],[1,0],[2,0],[0,1],[1,1],[2,1],[0,2],[1,2],[2,2]]
speeds = [12,12,12,12,12,12,12,12,12]
coverage = [1/8,6/8,1/8,6/8,1,6/8,1/8,6/8,1/8]
df2 = pd.DataFrame({'pixel':pixels, 'coverage':coverage,'speed':speeds})
print(compare_dataframes_ignore_order(df1, df2))



shape1 = [(1, 3), (3, 3), (3,1), (1,1)]
shape2 = [(0,0), (0,2), (2,2), (2,0)]
unit_test_data = generate_unit_test_data([scale_tuples(shape1), scale_tuples(shape2)], subtypes = ['forest', 'grass'])
df1 = format_into_land_table(unit_test_data)
pixels = [[0,0],[1,0],[0,1],[1,1],[1,1],[2,1],[1,2],[2,2]]
speeds = [12,12,12,12,5,5,5,5]
coverage = [1,1,1,1,1,1,1,1.0]#need a float to make it a float column not an int column
df2 = pd.DataFrame({'pixel':pixels, 'coverage':coverage,'speed':speeds})
print(compare_dataframes_ignore_order(df1, df2))




shape1 = [(0, 3), (3, 3), (3, 1.5), (0, 1.5)]
shape2 = [(0, 1.5), (3, 1.5), (3, 0), (0, 0)]
unit_test_data = generate_unit_test_data([scale_tuples(shape1), scale_tuples(shape2)], subtypes = ['forest','grass'])
df1 = format_into_land_table(unit_test_data)
pixels = [[0,0],[1,0],[2,0],[0,1],[1,1],[2,1],[0,1],[1,1],[2,1],[0,2],[1,2],[2,2]]
speeds = [12,12,12,12,12,12,5,5,5,5,5,5]
coverage = [1,1,1,0.5,0.5,0.5,0.5,0.5,0.5,1,1,1]
df2 = pd.DataFrame({'pixel':pixels, 'coverage':coverage,'speed':speeds})
print(compare_dataframes_ignore_order(df1, df2))



import math
shape1 = [(0,2), (1,3), (2,2), (1,1)]
shape2 = [(1,2), (2,3), (3,2), (2,1)]

# Generate points on the circle
radius = 0.5
num_points = 10000
shape3 = [(1 + radius * math.cos(2 * math.pi * i / num_points), 
           1 + radius * math.sin(2 * math.pi * i / num_points)) 
          for i in range(num_points)]




unit_test_data = generate_unit_test_data([scale_tuples(shape1), scale_tuples(shape2), scale_tuples(shape3)], subtypes = ['grass', 'forest', 'wetland'])
df1 = format_into_land_table(unit_test_data)
pixels = [[0,0],[1,0],[0,1],[1,1],[0,1],[1,1],[0,2],[1,2],[1,1],[2,1],[1,2],[2,2]]
speeds = [4,4,4,4,12,12,12,12,5,5,5,5]
coverage = [math.pi/16,math.pi/16,math.pi/16,math.pi/16,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
df2 = pd.DataFrame({'pixel':pixels, 'coverage':coverage,'speed':speeds})
print(compare_dataframes_ignore_order(df1, df2))
"""