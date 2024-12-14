# data_lake_utils.py
"""
Module contains function for uploading files to Azure Data Lake Storage.
"""
import os
from azure.storage.filedatalake import DataLakeServiceClient

storage_account_name = "azdbrickstorage" 
with open("AccountKey.config") as f:
    storage_account_key=f.readline()
file_system_name = "electric-meter-data"
# directory_name = "raw/emporiacircuits" 
directory_name = "raw/itronmeter"              

def upload_file_to_data_lake(file_path):
    try:
        service_client = DataLakeServiceClient(account_url=f"https://{storage_account_name}.dfs.core.windows.net",
                                               credential=storage_account_key)
        file_system_client = service_client.get_file_system_client(file_system=file_system_name)
        directory_client = file_system_client.get_directory_client(directory_name)
        file_name = os.path.basename(file_path)
        file_client = directory_client.create_file(file_name)
        with open(file_path, 'rb') as file:
            file_contents = file.read()
            file_client.upload_data(file_contents, overwrite=True)
        print(f"File '{file_name}' uploaded successfully to '{directory_name}' in container '{file_system_name}'.")
    except Exception as e:
        print(e)