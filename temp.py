


import pandas as pd

# Sample DataFrame (each row is a country, each column is a land type)
df = pd.DataFrame({
    'forest': [30, 20, 50],
    'desert': [10, 30, 5],
    'grassland': [60, 50, 45],
    'country': ['CountryA', 'CountryB', 'CountryC']
})

# Land type to speed mapping (you can change these values)
landtype_to_speed = {
    'forest': 2,
    'desert': 1,
    'grassland': 3
}

print(df)
speed_series = pd.Series(landtype_to_speed)

# Select only land type columns
land_columns = list(landtype_to_speed.keys())

# Calculate weighted sum and total coverage
weighted_sum = df[land_columns].mul(speed_series)
coverage_sum = df[land_columns].sum(axis=1)
weighted_avg_speed = weighted_sum.sum(axis=1) / coverage_sum

print(weighted_avg_speed)

print(df)


def calculate_speed(coords, params):
    filename = '/maps/hm708/processed_land_without_speed'

    df = pd.DataFrame({"pixel": [f"[{x}, {y}]" for (x, y) in coords]})
    df['original_index'] = df.index

    duckdb.query("DROP TABLE IF EXISTS input_pixels; CREATE TEMP TABLE input_pixels (pixel TEXT, original_index INTEGER)")
    duckdb.query("INSERT INTO input_pixels SELECT pixel, original_index FROM df")

    #edit this to be the actual parameter types used!!!
    land_type_to_speed = {
        "barren": params[0],          
        "crop": params[1],        
        "forest": params[2],            
        "grass": params[3],          
        "mangrove": params[4],         
        "moss": params[5],              
        "shrub": params[6],            
        "snow": params[7],     
        "urban": params[8],  
        "wetland": params[9]   
    }

    # Convert the dictionary to a DataFrame
    mapping_df = pd.DataFrame(list(land_type_to_speed.items()), columns=['land_type', 'speed'])

    # Register it as a DuckDB table
    duckdb.register('land_speed_mapping', mapping_df)

    query = f"""
    SELECT 
        input_pixels.pixel, 
        COALESCE(SUM(mapping.speed * read_parquet.coverage) / NULLIF(SUM(read_parquet.coverage), 0), 0) AS weighted_avg_speed
    FROM input_pixels
    LEFT JOIN read_parquet('{filename}*.parquet') AS read_parquet
        ON input_pixels.pixel = read_parquet.pixel
    LEFT JOIN land_speed_mapping AS mapping
        ON read_parquet.subtype = mapping.land_type
    GROUP BY input_pixels.pixel, input_pixels.original_index
    ORDER BY input_pixels.original_index
    """

    result = duckdb.query(query).df()
    return result['weighted_avg_speed']