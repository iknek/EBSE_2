import csv
from dotenv import load_dotenv
import os

# Load environment variable for PATH from .env file
load_dotenv()

def sort_csv_by_key(input_csv_path, output_csv_path, sort_key):
    with open(input_csv_path, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        sorted_list = sorted(reader, key=lambda row: int(row[sort_key]))

    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in sorted_list:
            writer.writerow(row)

# Prompt user for dataset choice
dataset_choice = input("Sort dataset (1) 'Pull Requests', or (2) 'Dataset Issues': ")

# Set file paths and sort key based on choice
absolute_path_to_folder = os.getenv('ABSOLUTE_PATH_TO_FOLDER')
if dataset_choice == '1':
    input_csv_path = os.path.join(absolute_path_to_folder, 'satd-dataset-pull_requests.csv')
    output_csv_path = os.path.join(absolute_path_to_folder, 'sortedPullRequests.csv')
    sort_key = 'pull_number'
elif dataset_choice == '2':
    input_csv_path = os.path.join(absolute_path_to_folder, 'satd-dataset-issues.csv')
    output_csv_path = os.path.join(absolute_path_to_folder, 'sortedIssues.csv')
    sort_key = 'issue_number'
else:
    print("Invalid choice. Please enter '1' for 'Pull Requests' or '2' for 'Dataset Issues'.")
    exit()

sort_csv_by_key(input_csv_path, output_csv_path, sort_key)
