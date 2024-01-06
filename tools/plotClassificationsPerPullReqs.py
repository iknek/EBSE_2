from dotenv import load_dotenv
import os
import csv
import matplotlib.pyplot as plt
from collections import defaultdict

# Load environment variable from .env file
load_dotenv()

# Access environment variable
absolute_path_to_folder = os.getenv('ABSOLUTE_PATH_TO_FOLDER')
input_csv_path = os.path.join(absolute_path_to_folder, 'satd-dataset-pull_requests.csv')

# Prompt user for settings
include_non_debt = input("Include 'non_debt' classification? (yes/no): ").lower().startswith('y')
group_size_input = input("Enter the number of pull requests per group (The Z value in the README): ")

try:
    group_size = int(group_size_input)
except ValueError:
    print("Invalid input for the number of pull requests per group. Using default value of 100.")
    group_size = 100

def aggregate_data(csv_file_path, include_non_debt, group_size):
    classification_counts = defaultdict(lambda: defaultdict(int))
    with open(csv_file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            pull_number_group = int(row['pull_number']) // group_size
            classification = row['classification']
            if include_non_debt or classification != 'non_debt':
                classification_counts[pull_number_group][classification] += 1
    return classification_counts

def plot_stacked_bar_chart(classification_counts, group_size):
    group_numbers = sorted(classification_counts.keys())
    classifications = set(clas for counts in classification_counts.values() for clas in counts)
    bottom_values = defaultdict(int)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for classification in classifications:
        counts = [classification_counts[group][classification] for group in group_numbers]
        ax.bar(group_numbers, counts, bottom=[bottom_values[group] for group in group_numbers], label=classification)
        for group in group_numbers:
            bottom_values[group] += classification_counts[group][classification]

    ax.set_xlabel(f'Pull Request Groups (per {group_size})')
    ax.set_ylabel('Number of SATDs')
    ax.set_title(f'Number of SATDs per Classification Type per {group_size} Pull Requests')
    ax.legend(title='Classification Types')

    plt.show()

classification_counts = aggregate_data(input_csv_path, include_non_debt, group_size)
plot_stacked_bar_chart(classification_counts, group_size)
