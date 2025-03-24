"""
why are there nones in the table?
df = pd.read_parquet("delete.parquet")
geometry_list = df["bbox"].tolist()
"""

from shapely import wkb
import duckdb
import pandas as pd
from shapely.ops import unary_union
from shapely.geometry.polygon import Polygon
from shapely.geometry import MultiPolygon, Polygon
import geopandas as gpd
import time
import csv


def hex_to_wkb(hex_string):
    binary_wkb = hex_string.hex()
    return wkb.loads(binary_wkb)




def read_and_format_numbers(filename="test_points_of_amazon_land.csv"):
    formatted_numbers = []
    unformatted_numbers = []
    with open(filename, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            unformatted_numbers.append(row)
            formatted_numbers.append(f"[{float(row[0])}, {float(row[1])}]")
    return formatted_numbers, unformatted_numbers



def best_land_algorithm(filtered_df, pixel):
    already_calculated = MultiPolygon([])
    total_speed = 0
    while not filtered_df.empty:
        # repeat until all of df is empty

        #seperate into dataframe of the slowest speed, and all others
        slowest_df = filtered_df[filtered_df["speed"] == filtered_df["speed"].min()]
        filtered_df = filtered_df[filtered_df["speed"] != filtered_df["speed"].min()]
        land = unary_union(slowest_df["geometry"].tolist())
        intersection = land.intersection(already_calculated)
        total_speed = total_speed + ((land.area - intersection.area) / angle**2) * slowest_df["speed"].iloc[0]
            
        already_calculated = unary_union([already_calculated,land])

    # if there is area with no data:
    total_speed = total_speed + (pixel.area - already_calculated.area) * no_land_data
    return total_speed




def worse_land_algorithm(filtered_df):
    total_speed = 0
    total = sum(filtered_df["geometry"])
    if total != 0:
        filtered_df["geometry"] = filtered_df["geometry"] / total
        return sum(filtered_df["geometry"] * filtered_df["speed"])
    return 1


def shit_land_algorithm(filtered_df):
    filtered_df = filtered_df[filtered_df["geometry"] != 0]
    if filtered_df.empty:
        print('!!!!')
        return 1
    return min(filtered_df["speed"] )



angle = 0.008333333333333333333
no_land_data = 1

pixels, p2 = read_and_format_numbers()
start_time = time.time()
speeds = []

with open('shit_land_algo_amazon3.csv', 'w') as f:
    for n in range (745,1000):

        query = f"""
        DROP TABLE IF EXISTS id_list;
        CREATE TEMP TABLE id_list AS
        SELECT id 
        FROM read_parquet('processed_land/pixel_to_id*.parquet') 
        WHERE bbox = '{pixels[n]}'
        """
        land_df = duckdb.query(query)

        query = f"""
        SELECT geometry, speed
        FROM id_list
        JOIN read_parquet('processed_land/id_to_info*.parquet') info
        ON id_list.id = info.id
        """
        land_df = duckdb.query(query).df()

        xangle = int(p2[n][0]) * angle
        print(xangle)
        yangle = int(p2[n][1]) * angle


        land_df['geometry'] = gpd.GeoDataFrame(land_df['geometry'].apply(hex_to_wkb), geometry='geometry', crs="EPSG:4326")
        pixel = Polygon([(xangle,yangle), (xangle, yangle + angle),  (xangle + angle, yangle + angle),  (xangle + angle, yangle)])
        land_df['geometry'] = land_df['geometry'].apply(lambda geom: pixel.intersection(geom).area)#get rid of .area for better version
        f.write(f"{pixels[n]},{shit_land_algorithm(land_df)}\n")






print(time.time() - start_time)