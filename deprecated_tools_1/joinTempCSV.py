import os
import requests
import pandas as pd
from dotenv import load_dotenv
import time
import glob

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Get the absolute path to the folder where the CSV file is located
csv_directory = os.path.join(os.getenv('ABSOLUTE_PATH_TO_FOLDER'),'../../rq1/temp2')
output_file = os.path.join(os.getenv('ABSOLUTE_PATH_TO_FOLDER'), '../../rq1/rq1_22.csv')

# Use glob to get a list of all CSV files in the directory
csv_files = glob.glob(os.path.join(csv_directory, '*.csv'))

# List to hold data from each CSV
all_data = []

# Iterate over the list of CSV files
for file in csv_files:
    # Read each CSV file and append it to the list
    df = pd.read_csv(file)
    all_data.append(df)

# Concatenate all data into one DataFrame
combined_df = pd.concat(all_data, ignore_index=True)

# Save the combined data to a single CSV file
combined_df.to_csv(output_file, index=False)

print("All CSV files have been combined into one.")