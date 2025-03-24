from shapely.geometry import Polygon
from values import ANGLE
import pandas as pd
from shapely.wkb import dumps
import pyarrow.parquet as pq
import json
#questions from this:
#how i want to index pixels
#underflow? printing off small values rounds inccorecclty, is it being stored correctly?

"""
i believe that soe arent passing because iterates through boxes using bbox min to max, if these are floats?
problem with generating grid for each one

"""

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
    return bytes.fromhex(dumps(Polygon(shape), hex=True))

def generate_unit_test_data(id, shapes, subtypes):
    table = pd.DataFrame({'geometry':[polygon_to_hex(shape) for shape in shapes], 'bbox':[create_bounding_box(shape) for shape in shapes], 'subtype':subtypes})
    table.to_parquet(f'unit_test{id}.parquet', index=False)




#shape = [(1.5, 3), (3, 1.5), (1.5, 0), (0, 1.5)]
#generate_unit_test_data(1, [scale_tuples(shape)], subtypes = ['grass'])



shape1 = [(1, 3), (3, 3), (3,1), (1,1)]
shape2 = [(0,0), (0,2), (2,2), (2,0)]
generate_unit_test_data(2, [scale_tuples(shape1), scale_tuples(shape2)], subtypes = ['grass', 'forest'])


shape1 = [(0, 3), (3, 3), (3, 1.5), (0, 1.5)]
shape2 = [(0, 1.5), (3, 1.5), (3, 0), (0, 0)]
generate_unit_test_data(3, [scale_tuples(shape1), scale_tuples(shape2)], subtypes = ['grass', 'forest'])



import math
shape1 = [(0,2), (1,3), (2,2), (1,1)]
shape2 = [(1,2), (2,3), (3,2), (2,1)]

# Generate points on the circle
radius = 0.5
num_points = 100
shape3 = [(1 + radius * math.cos(2 * math.pi * i / num_points), 
           1 + radius * math.sin(2 * math.pi * i / num_points)) 
          for i in range(num_points)]


generate_unit_test_data(4, [scale_tuples(shape1), scale_tuples(shape2), scale_tuples(shape3)], subtypes = ['grass', 'forest', 'wetland'])