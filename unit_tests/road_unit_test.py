from shapely.geometry import LineString
#from values import ANGLE
ANGLE = 1
import pandas as pd
from shapely.wkb import dumps
import pyarrow.parquet as pq
import json


def polygon_to_hex(shape) -> bytes:
    return bytes.fromhex(dumps(LineString(shape), hex=True))

def scale_tuples(point_list):
    return [(p[0] * ANGLE, p[1] * ANGLE) for p in point_list]


def generate_unit_test_data(id, shapes, subtypes, road_surfaces,speed_limits,given_classes):
    table = pd.DataFrame({'geometry':[polygon_to_hex(shape) for shape in shapes], 'subtype':subtypes, 'road_surface':road_surfaces,'speed_limits':speed_limits,'class':given_classes})
    table.to_parquet(f'road_table_unit_test{id}.parquet', index=False)





shape = [(0.5, 0.5), (2.5, 0.5)]
generate_unit_test_data(1, [scale_tuples(shape)], ['road'], [None],[None],['primary'])


shape = [(1, 0.5), (2.5, 0.5)]
generate_unit_test_data(2, [scale_tuples(shape)], ['road'], [None],[None],['primary'])


shape = [(0.5, 0.5),(1.3, 0.5),(1.6, 0.5), (2.5, 0.5)]
generate_unit_test_data(3, [scale_tuples(shape)], ['road'], [None],[None],['primary'])

