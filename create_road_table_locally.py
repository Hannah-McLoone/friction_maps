import pandas as pd
import pyarrow.parquet as pq
from values import Values
from creating_road_speed_table import format_into_road_table
from create_connection import create_connection

def create_tables_for_all_files_using_connection(remote_directory,coord_file): #coord file contains list of names
    df = pd.read_csv(coord_file)
    names_list = df['file_name'].tolist()


    n = 0
    # Loop through each file in the names_list
    for file_name in names_list:
        client = create_connection()
        sftp = client.open_sftp()


        print('Processing:', file_name)
        file_path = remote_directory + '/' + file_name
        print(file_path)
        remote_file = sftp.file(file_path, 'rb')

        # Use PyArrow to read the dataset and filter it
        with remote_file as f:
            table = pq.read_table(f,columns=['geometry','subtype','road_surface','speed_limits','class'], filters=[[('class', 'in', list(Values.country_road_values.keys()))], [('subtype', 'in', ['rail','water'])]])
            table = table.to_pandas()
        client.close()

        mega_table = format_into_road_table(table)
        mega_table.to_parquet(f'higher_granularity_output/pixel_to_road_speed{n}.parquet', index=False)
        n = n+1





#___________________________________________________________
#for investigation purposes



client = create_connection()
sftp = client.open_sftp()
remote_directory = '/maps/sj514/overture/theme=transportation/type=segment'
file_name='part-00000-d84517a6-f7b3-48eb-8ec2-e27684978d01-c000.zstd.parquet' #35 for uk or 01
file_path = remote_directory + '/' + file_name
remote_file = sftp.file(file_path, 'rb')

with remote_file as f:
    batch = next(pq.ParquetFile(f).iter_batches(
        batch_size=1000,
        columns=['geometry','class']
    ))
    df = batch.to_pandas()
    df = df[
        df['class'].isin(['unclassified'])
    ]

def get_coord(entry):
    return list(entry.coords)[0]

from shapely import wkb

client.close()
df['geometry'] = df['geometry'].map(wkb.loads)
df['geometry'] = df['geometry'].apply(get_coord)
print(df)