import csv
from collections import defaultdict
from dotenv import load_dotenv
import os

# Load environment variable for PATH from .env file
load_dotenv()

def count_classifications(csv_file):
    classification_count = defaultdict(int)

    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            classification = row['classification']
            classification_count[classification] += 1

    return classification_count

absolute_path_to_folder = os.getenv('ABSOLUTE_PATH_TO_FOLDER')

# Ask the user to choose the dataset
data_choice = input("Count classifications for (1) Pull Requests, (2) Code Comments, (3) Commit Messages, (4) Dataset Issues? Enter 1, 2, 3, or 4: ")

if data_choice == '1':
    csv_file_name = 'combined_checkpoints.csv' # Uses updated combined checkpoints
elif data_choice == '2':
    csv_file_name = 'satd-dataset-code_comments.csv'
elif data_choice == '3':
    csv_file_name = 'satd-dataset-commit_messages.csv'
elif data_choice == '4':
    csv_file_name = 'satd-dataset-issues.csv'
else:
    print("Invalid choice. Please run the script again and select a valid option.")
    exit()

csv_file_path = os.path.join(absolute_path_to_folder, csv_file_name)
counts = count_classifications(csv_file_path)

for classification, count in counts.items():
    print(f'{classification}: {count}')