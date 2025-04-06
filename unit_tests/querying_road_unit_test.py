#angle?

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))# fix this
from querying_road_pixel import create_friction_map_for_section


# Write to Parquet
def test_query(input, expected, rounding = -1):
    input.to_parquet('unit_test_data_for_querying.parquet', index=False)
    calculated = (create_friction_map_for_section(len(expected[0]),len(expected),0,0,'unit_test_data_for_querying'))
    os.remove('unit_test_data_for_querying.parquet')


    if rounding != -1:
        expected = np.round(expected, rounding)
        calculated = np.round(calculated, rounding)

    return(np.array_equal(expected,calculated))



#______________________________________________________________________________

#simple examples from single road unit tests, includes testing squares with no roads
df = pd.DataFrame({'geometry':[(0,0),(2,0)], 'speed_kph':[97,97]})
expected = np.array([[0,0,0],[0,0,0],[97,0,97]])
print(test_query(df,expected))


df = pd.DataFrame({'geometry':[(1,0),(2,0)], 'speed_kph':[97,97]})
expected = np.array([[0,0,0],[0,0,0],[0,97,97]])
print(test_query(df,expected))


df = pd.DataFrame({'geometry':[(0,0),(1,0),(2,0)], 'speed_kph':[97,97,97]})
expected = np.array([[0,0,0],[0,0,0],[97,97,97]])
print(test_query(df,expected))


#__________________________________________________________________________________
#testing multiple roads of same speed in square
df = pd.DataFrame({'geometry':[(0,0),(0,0)], 'speed_kph':[10,10]})
expected = np.array([[0,0,0],[0,0,0],[10,0,0]])
print(test_query(df,expected))

df = pd.DataFrame({'geometry':[(0,0),(0,0),(0,0)], 'speed_kph':[10,10,10]})
expected = np.array([[0,0,0],[0,0,0],[10,0,0]])
print(test_query(df,expected))



#testing multiple roda of different speeds in square
df = pd.DataFrame({'geometry':[(0,0),(0,0)], 'speed_kph':[10,15]})
expected = np.array([[0,0,0],[0,0,0],[15,0,0]])
print(test_query(df,expected))


df = pd.DataFrame({'geometry':[(0,0),(0,0),(0,0)], 'speed_kph':[10,15,20]})
expected = np.array([[0,0,0],[0,0,0],[20,0,0]])
print(test_query(df,expected))

df = pd.DataFrame({'geometry':[(0,0),(0,0),(0,0)], 'speed_kph':[10,10,20]})
expected = np.array([[0,0,0],[0,0,0],[20,0,0]])
print(test_query(df,expected))

df = pd.DataFrame({'geometry':[(0,0),(0,0),(0,0)], 'speed_kph':[10,20,20]})
expected = np.array([[0,0,0],[0,0,0],[20,0,0]])
print(test_query(df,expected))


#__________________________________________________________________________________
#example from multi-road unit tests

df2 = pd.DataFrame({'geometry':[(0,0),(1,0),(0,1),(0,1),(1,1),(1,1),(2,1),(2,1),(2,1),(1,2)], 'speed_kph':[97,97,97,113,97,97,97,97,113,113]})


