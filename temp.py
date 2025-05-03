import pandas as pd
import sqlite3

# Create a simple DataFrame
df = pd.DataFrame({
    'pixel': [1, 1, 1, 1, 2, 2, 2, 3],
    'subtype': ['a', 'a', 'b', 'c', 'b', 'b', 'c', 'a'], 
    'coverage': [1, 2, 3, 5, 2, 6, 1, 3]
})

# Create in-memory SQLite DB and write DataFrame to it
conn = sqlite3.connect(':memory:')
df.to_sql('my_table', conn, index=False, if_exists='replace')

# SQL query to get total coverage per pixel-subtype combination
query = """
SELECT pixel, subtype, SUM(coverage) as total_coverage
FROM my_table
GROUP BY pixel, subtype
"""
result_df = pd.read_sql_query(query, conn)

# Pivot the result
pivot_df = result_df.pivot(index='pixel', columns='subtype', values='total_coverage').fillna(0)

print(pivot_df)

conn.close()
