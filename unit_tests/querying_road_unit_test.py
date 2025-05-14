import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))# fix this
from main_pipeline.querying_algorithm import create_friction_map_for_section


# Write to Parquet
def test_query(input, expected, rounding = -1):
    selection = "SELECT input_pixels.pixel, COALESCE(MAX(read_parquet.speed_kph), 0) AS speed"
    input.to_parquet('unit_test_data_for_querying.parquet', index=False)
    calculated = (create_friction_map_for_section(len(expected[0]),len(expected),0,0,'unit_test_data_for_querying',selection))
    os.remove('unit_test_data_for_querying.parquet')


    if rounding != -1:
        expected = np.round(expected, rounding)
        calculated = np.round(calculated, rounding)

    return(np.array_equal(expected,calculated))


#______________________________________________________________________________

#simple examples from single road unit tests, includes testing squares with no roads
#TEST 1
df = pd.DataFrame({'pixel':[(0,0),(2,0)], 'speed_kph':[97,97]})
expected = np.array([[0,0,0],[0,0,0],[97,0,97]])
print("TEST 1: ",test_query(df,expected))

#TEST 2
df = pd.DataFrame({'pixel':[(1,0),(2,0)], 'speed_kph':[97,97]})
expected = np.array([[0,0,0],[0,0,0],[0,97,97]])
print("TEST 2: ",test_query(df,expected))

#TEST 3
df = pd.DataFrame({'pixel':[(0,0),(1,0),(2,0)], 'speed_kph':[97,97,97]})
expected = np.array([[0,0,0],[0,0,0],[97,97,97]])
print("TEST 3: ",test_query(df,expected))


#__________________________________________________________________________________
#some other tests not mentioned in write up
#testing multiple roads of same speed in square
df = pd.DataFrame({'pixel':[(0,0),(0,0)], 'speed_kph':[10,10]})
expected = np.array([[0,0,0],[0,0,0],[10,0,0]])
print(test_query(df,expected))

df = pd.DataFrame({'pixel':[(0,0),(0,0),(0,0)], 'speed_kph':[10,10,10]})
expected = np.array([[0,0,0],[0,0,0],[10,0,0]])
print(test_query(df,expected))



#testing multiple roda of different speeds in square
df = pd.DataFrame({'pixel':[(0,0),(0,0)], 'speed_kph':[10,15]})
expected = np.array([[0,0,0],[0,0,0],[15,0,0]])
print(test_query(df,expected))


df = pd.DataFrame({'pixel':[(0,0),(0,0),(0,0)], 'speed_kph':[10,15,20]})
expected = np.array([[0,0,0],[0,0,0],[20,0,0]])
print(test_query(df,expected))

df = pd.DataFrame({'pixel':[(0,0),(0,0),(0,0)], 'speed_kph':[10,10,20]})
expected = np.array([[0,0,0],[0,0,0],[20,0,0]])
print(test_query(df,expected))

df = pd.DataFrame({'pixel':[(0,0),(0,0),(0,0)], 'speed_kph':[10,20,20]})
expected = np.array([[0,0,0],[0,0,0],[20,0,0]])
print(test_query(df,expected))


#__________________________________________________________________________________
#example from multi-road unit tests

#TEST 4
df = pd.DataFrame({'pixel':[(0,0),(1,0),(0,1),(0,1),(1,1),(1,1),(2,1),(2,1),(2,1),(1,2)], 'speed_kph':[50,50,50,100,50,50,50,50,100,100]})
expected = np.array([[0,100,0],[100,50,100],[50,50,0]])
print("TEST 4: ",test_query(df,expected))


df = pd.DataFrame({'pixel':[(0,0),(1,0),(0,1),(0,1),(1,1),(1,1),(2,1),(2,1),(2,1),(1,2)], 'speed_kph':[50,50,50,100,50,50,50,50,100,100]})
expected = np.array([[0,100,0],[100,50,100],[50,50,0]])
print("TEST 4: ",test_query(df,expected))