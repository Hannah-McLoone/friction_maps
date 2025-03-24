print(1)
import pandas as pd
import paramiko
import os
import re
import pyarrow.parquet as pq
import pyarrow.dataset as ds
import io
import time
from values import Values, water_values
import numpy as np


hostname = 'sherwood.cl.cam.ac.uk'  # or 'kinabalu.cl.cam.ac.uk'
port = 22  # Default SSH port
username = 'hm708' 
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



client = create_connection()


sftp = client.open_sftp()
file_path = '/home/hm708' + '/' + 'output_file.parquet'

remote_file = sftp.file(file_path, 'rb')

# Use PyArrow to read the dataset and filter it
with remote_file as f:
    table = pq.read_table(f)#geometry, subtype

print(table.to_pandas())
client.close()