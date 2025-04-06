#uses land_cover. do i want land cover or land???

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
import sys


def load_geometry_from_wkb_bytes(wkb_bytes):
    binary_wkb = wkb_bytes.hex()
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


def format_into_land_table(table):
    table['subtype'] = table['subtype'].map(land_speed)
    table.rename(columns={'subtype': 'speed'}, inplace=True)

    #this line is about 5 percent of time
    table['geometry'] = gpd.GeoDataFrame(table['geometry'].apply(load_geometry_from_wkb_bytes), geometry='geometry', crs="EPSG:4326")

    #roughly the other 95 percent
    table[['pixel', 'coverage']] = table.apply(lambda row: pd.Series(generate_coord_overlap(row['bbox'], row['geometry'])), axis=1)

    table = table.drop(['bbox','geometry'], axis = 1)
    table = table.explode(['pixel', 'coverage'])
    table = table[table['coverage'] != 0]

    return table


def parquet_file_to_database(input_file, output_file, chunk_size=100): # more ram efficient to be readig and processing in chunks
    reader = pq.ParquetFile(input_file)
    
    first_chunk = True
    writer = None
    
    for batch in reader.iter_batches(batch_size=chunk_size):
        table = batch.to_pandas()
        
        if {'subtype', 'geometry', 'bbox'}.issubset(table.columns):
            table = table[['subtype', 'geometry', 'bbox']]
        else:
            raise ValueError("Missing required columns in the input file")
        
        table = format_into_land_table(table)
        
        table_arrow = pa.Table.from_pandas(table)
        
        if first_chunk:
            writer = pq.ParquetWriter(output_file, table_arrow.schema)
            first_chunk = False
        
        writer.write_table(table_arrow)
    
    if writer:
        writer.close()



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script <arg1> <arg2>")
    else:
        arg1, arg2 = sys.argv[1], sys.argv[2]
        parquet_file_to_database(arg1, arg2)
