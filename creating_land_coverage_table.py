#uses land_cover. do i want land cover or land???

"""
the code i am working on in the newer version
"""


import pandas as pd
import paramiko
import pyarrow.parquet as pq
import pyarrow as pa 
import pyarrow.dataset as ds
import time
import numpy as np
from values import Land_values
from values import ANGLE
import geopandas as gpd
from shapely import wkb
from shapely.geometry import Polygon


#change this from hex string!!!!!!
def hex_to_wkb(hex_string):
    binary_wkb = hex_string.hex()
    return wkb.loads(binary_wkb)




def generate_coord_overlap(bbox, geometry):
    # Define the range of x and y values based on bbox and ANGLE
    x_values = np.arange(bbox['xmin']//ANGLE, bbox['xmax']//ANGLE + 1)
    y_values = np.arange(bbox['ymin']//ANGLE, bbox['ymax']//ANGLE + 1)

    # Create mesh grid and flatten it into coordinate pairs
    x_grid, y_grid = np.meshgrid(x_values, y_values, indexing="ij")
    flat_geometries = np.column_stack([x_grid.ravel(), y_grid.ravel()])

    # Create the corner coordinates for the polygons
    x_vals, y_vals = flat_geometries[:, 0] * ANGLE, flat_geometries[:, 1] * ANGLE
    x0, y0 = x_vals, y_vals
    x1, y1 = x_vals, y_vals + ANGLE
    x2, y2 = x_vals + ANGLE, y_vals + ANGLE
    x3, y3 = x_vals + ANGLE, y_vals

    # Stack coordinates into polygons
    polygons_array = np.stack([np.column_stack((x0, y0)),
                               np.column_stack((x1, y1)),
                               np.column_stack((x2, y2)),
                               np.column_stack((x3, y3))], axis=1)

    # Create a GeoSeries of Shapely Polygons
    polygons = [Polygon(coords) for coords in polygons_array]
    geo_series = gpd.GeoSeries(polygons)

    # Convert the geometry into a Shapely Polygon
    geometry_polygon = Polygon(geometry)


    #----------------------------------------------------------------------------------
    #95 percent of the time is spent on this section few lines

    #method 1: 
    intersection_areas = geo_series.intersection(geometry_polygon).area

    #method 2??:
    #intersection_areas = geo_series.apply(lambda x: compute_area(x, geometry_polygon))

    #----------------------------------------------------------------------------------

    # Extract pixel coordinates and areas
    #takes the bottom left corner of the pixel as the identifier. is this the same as roads? Yes, yes it is
    pixels = np.array([coords[0] for coords in polygons_array])
    
    return pixels, intersection_areas.values  # Convert the result to a numpy array




def land_speed(subtype):#,given_class):
    return Land_values.land_type_speeds.get(subtype, 1)



def parquet_file_to_database(input_file, output_file):##kept around as backup
    table = pq.read_table(input_file).to_pandas()

    table['subtype'] = table['subtype'].map(land_speed)
    table.rename(columns={'subtype': 'speed'}, inplace=True)

    #this line is about 5 percent of time
    table['geometry'] = gpd.GeoDataFrame(table['geometry'].apply(hex_to_wkb), geometry='geometry', crs="EPSG:4326")

    table[['pixel', 'coverage']] = table.apply(lambda row: pd.Series(generate_coord_overlap(row['bbox'], row['geometry'])), axis=1)
    #drop geometry column

    table = table.drop(['bbox','geometry'], axis = 1)

    table = table.explode(['pixel', 'coverage'])

    #if i wanted to drop the pixels with 0 coverage it would be at this point.
    #im not sure whether this is worth it though because i would only look at each 0 pixel once anyway. saves space, not sure about time
    table = table[table['coverage'] != 0]# mostly for ease of testing. will prob get rid of in final version

    table.to_parquet(output_file, index=False)



def format_into_land_table(table):
    table['subtype'] = table['subtype'].map(land_speed)
    table.rename(columns={'subtype': 'speed'}, inplace=True)

    #this line is about 5 percent of time
    table['geometry'] = gpd.GeoDataFrame(table['geometry'].apply(hex_to_wkb), geometry='geometry', crs="EPSG:4326")

    table[['pixel', 'coverage']] = table.apply(lambda row: pd.Series(generate_coord_overlap(row['bbox'], row['geometry'])), axis=1)
    #drop geometry column

    table = table.drop(['bbox','geometry'], axis = 1)

    table = table.explode(['pixel', 'coverage'])

    #if i wanted to drop the pixels with 0 coverage it would be at this point.
    #im not sure whether this is worth it though because i would only look at each 0 pixel once anyway. saves space, not sure about time
    table = table[table['coverage'] != 0]# mostly for ease of testing. will prob get rid of in final version


    return table

def turn_overture_into_land_table(input_file, output_file):
    table = pq.read_table(input_file).to_pandas()
    format_into_land_table(table).to_parquet(output_file, index=False)

