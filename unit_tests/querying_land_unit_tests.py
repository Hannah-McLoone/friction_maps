# Write to Parquet
import pandas as pd
import numpy as np
import sys
import os
import math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))# fix this
from main_pipeline.querying_algorithm import create_friction_map_for_section


def test_query(input, expected, rounding = -1):
    selection = "SELECT input_pixels.pixel, COALESCE(SUM(read_parquet.speed * read_parquet.coverage) / NULLIF(SUM(read_parquet.coverage), 0), 0) AS speed"
    input.to_parquet('unit_test_data_for_querying.parquet', index=False)
    calculated = (create_friction_map_for_section(len(expected[0]),len(expected),0,0,'unit_test_data_for_querying',selection))
    os.remove('unit_test_data_for_querying.parquet')


    if rounding != -1:
        expected = np.round(expected, rounding)
        calculated = np.round(calculated, rounding)

    return(np.array_equal(expected,calculated))


# TEST 1
pixels = [[0,0],[1,0],[2,0],[0,1],[1,1],[2,1],[0,2],[1,2],[2,2]]
speeds = [12,12,12,12,12,12,12,12,12]
coverage = [1/8,6/8,1/8,6/8,1,6/8,1/8,6/8,1/8]
df = pd.DataFrame({'pixel':pixels, 'coverage':coverage,'speed':speeds})
print("TEST 1: ",test_query(df, [[12,12,12.],[12,12,12.],[12,12,12.]], 4))


# TEST 2
pixels = [[0,0],[1,0],[0,1],[1,1],[1,1],[2,1],[1,2],[2,2]]
speeds = [12,12,12,12,5,5,5,5]
coverage = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
df = pd.DataFrame({'pixel':pixels, 'coverage':coverage,'speed':speeds})
expected = np.array([[0,5,5],[12,8.5,5],[12,12,0]])
print("TEST 2: ",test_query(df,expected))



# TEST 3
pixels = [[0,0],[1,0],[2,0],[0,1],[1,1],[2,1],[0,1],[1,1],[2,1],[0,2],[1,2],[2,2]]
speeds = [12,12,12,12,12,12,5,5,5,5,5,5]
coverage = [1,1,1,0.5,0.5,0.5,0.5,0.5,0.5,1,1,1]
df = pd.DataFrame({'pixel':pixels, 'coverage':coverage,'speed':speeds})
expected = np.array([[5,5,5],[8.5,8.5,8.5],[12,12,12]])
print("TEST 3: ",test_query(df,expected))



# TEST 4
pixels = [[0,0],[1,0],[0,1],[1,1],[0,1],[1,1],[0,2],[1,2],[1,1],[2,1],[1,2],[2,2]]
speeds = [4,4,4,4,12,12,12,12,5,5,5,5]
coverage = [math.pi/16,math.pi/16,math.pi/16,math.pi/16,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
df = pd.DataFrame({'pixel':pixels, 'coverage':coverage,'speed':speeds})
expected = np.array([[12,8.5,5],[9.74,7.76,5],[4,4,0]])
print("TEST 4: ",test_query(df,expected,2))