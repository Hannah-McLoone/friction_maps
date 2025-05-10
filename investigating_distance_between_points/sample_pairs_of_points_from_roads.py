import pandas as pd

from shapely import wkb
import paramiko
import pyarrow.parquet as pq
import pyarrow.dataset as ds
import time
from main_pipeline.values import Values, water_values
import random

# --select 1000 roads from each file
# get set of interpoint distances - in angles and km
#       record whether road, rail or water


#part 9 - i=10

def select_points_from_single_road(entry):
    point_set = list(entry.coords)
    #return [(point_set[i], point_set[i+1]) for i in range(0, min(5,len(point_set) - 1))]
    i = random.randint(0, len(point_set) - 2)
    return (point_set[i], point_set[i + 1])



def test(remote_directory,coord_file):
    start_time = time.time()

    df = pd.read_csv(coord_file)
    names_list = df['file_name'].tolist()



    i = 0
    names_list = [names_list[0],names_list[1],names_list[2],names_list[3],names_list[9]]

    for file_name in names_list:
        i = i + 1
        print(i)
        client = create_connection()
        sftp = client.open_sftp()
        #print('Processing:', file_name)
        file_path = remote_directory + '/' + file_name
        remote_file = sftp.file(file_path, 'rb')

        # Use PyArrow to read the dataset and filter it
        with remote_file as f:
            table = pq.read_table(f,columns=['geometry','class', 'subtype'], filters=[[('class', 'in', list(Values.country_road_values.keys()))]   ])#, [('subtype', 'in', ['rail','water'])]])

        table = table.to_pandas()
        client.close()

        sampled_df = table.sample(n=int(len(table) / 100), random_state=42)
        sampled_df['geometry'] = sampled_df['geometry'].map(wkb.loads)
        sampled_df['geometry'] = sampled_df['geometry'].map(select_points_from_single_road)
        #mega_table = sampled_df.explode('geometry')

        sampled_df.to_csv('amazon_sample.csv', mode='a', index=False, header=not pd.io.common.file_exists(file_path))


# theres 2243540 in file 1
#2243540 / 10000 =~= 200


#empty_df = pd.DataFrame()
#empty_df.to_csv('amazon_sample.csv', index=False)#no!!!!!!!!!!!!!!!!!!!!!!!!!!!!


#go from 4





# Configuration
hostname = 'sherwood.cl.cam.ac.uk'  # or 'kinabalu.cl.cam.ac.uk'
port = 22  # Default SSH port
username = 'hm708'  # Replace with your actual CSRid
private_key_path = '/Users/hanna/.ssh/id_rsa'  # Path to your private key file

def create_connection():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
        client.connect(hostname, port=port, username=username, pkey=private_key)
        return client
    except Exception as e:
        print(f'An error occurred: {e}')




start_time = time.time()


test('/maps/sj514/overture/theme=transportation/type=segment', "file_cords_of_transport.csv")

end_time = time.time()

print(end_time - start_time)


#start from n = 40