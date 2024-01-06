import csv
from dotenv import load_dotenv
import os

# Load environment variable for PATH from .env file
load_dotenv()

def sort_csv_by_pull_number(input_csv_path, output_csv_path):
    with open(input_csv_path, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        sorted_list = sorted(reader, key=lambda row: int(row['pull_number']))

    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in sorted_list:
            writer.writerow(row)

# REPLACE with your ACTUAL file absolute path!!!
absolute_path_to_folder = os.getenv('ABSOLUTE_PATH_TO_FOLDER')
input_csv_path = absolute_path_to_folder+'satd-dataset-pull_requests.csv'
output_csv_path = absolute_path_to_folder+'orderSortedPullRequests.csv'
sort_csv_by_pull_number(input_csv_path, output_csv_path)
