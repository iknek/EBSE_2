import csv
from collections import defaultdict
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def count_classifications(csv_file):
    classification_count = defaultdict(int)

    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            classification = row['classification']
            classification_count[classification] += 1

    return classification_count

# Replace 'path/to/your/csvfile.csv' with the path to your CSV file
absolute_path_to_folder = os.getenv('ABSOLUTE_PATH_TO_FOLDER')
csv_file_path = absolute_path_to_folder+'satd-dataset-commit_messages.csv'
counts = count_classifications(csv_file_path)

for classification, count in counts.items():
    print(f'{classification}: {count}')
