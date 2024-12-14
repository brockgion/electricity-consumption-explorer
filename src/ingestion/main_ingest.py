# main_ingest.py
"""
Main script for ingesting files to Azure Data Lake Storage.
The filename is passed as an argument and then uploads it to the specified container in Azure
"""

import sys
import os
from data_lake_utils import upload_file_to_data_lake

def main(file_name):

    file_path = os.path.join(file_name)

    if os.path.exists(file_path):
        upload_file_to_data_lake(file_path)
    else:
        print(f"Error: File '{file_path}' not found. Please check the file path and try again.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        main(file_name)
    else:
        print("Error: Please provide the file name as an argument.")
        print("Usage: python main_ingest.py <filename>")