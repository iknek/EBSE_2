from dotenv import load_dotenv
import os
import csv
import matplotlib.pyplot as plt
from collections import defaultdict

# Load environment variable from .env file
load_dotenv()

# Access environment variable
absolute_path_to_folder = os.getenv('ABSOLUTE_PATH_TO_FOLDER')

# Ask user which data set to plot
data_set_choice = input("Which dataset would you like to plot - (1) 'Pull Requests', or (2) 'Issues': ")

if data_set_choice == '1':
    data_column = 'pull_number'
    input_csv_path = os.path.join(absolute_path_to_folder,'sortedPullRequests.csv')
    choice = "Pull Requests"
elif data_set_choice == '2':
    data_column = 'issue_number'
    input_csv_path = os.path.join(absolute_path_to_folder, 'sortedDatasetIssues.csv')
    choice = "Dataset Issues"
else:
    print("Invalid dataset choice. Please enter '1' or '2'.")
    exit()

# Prompt user for settings
include_non_debt = input("Include 'non_debt' classification? (yes/no): ").lower().startswith('y')
group_size_input = input(f"Enter the number of {choice} per group: ")

try:
    group_size = int(group_size_input)
except ValueError:
    print(f"Invalid input for the number of {data_set_choice} per group. Using default value of 100.")
    group_size = 100

def aggregate_data(csv_file_path, include_non_debt, group_size, data_column):
    classification_counts = defaultdict(lambda: defaultdict(int))
    with open(csv_file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            item_group = int(row[data_column]) // group_size
            classification = row['classification']
            if include_non_debt or classification != 'non_debt':
                classification_counts[item_group][classification] += 1
    return classification_counts

def plot_stacked_bar_chart(classification_counts, group_size, choice):
    group_numbers = sorted(classification_counts.keys())
    bottom_values = defaultdict(int)
    total_counts = defaultdict(int)

    # Calculate total counts for each classification
    for group in classification_counts:
        for classification, count in classification_counts[group].items():
            total_counts[classification] += count

    # Sort classifications by total count (from most to least)
    sorted_classifications = sorted(total_counts, key=total_counts.get, reverse=True)

    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot bars in sorted order
    for classification in sorted_classifications:
        counts = [classification_counts[group][classification] for group in group_numbers]
        label = f"{classification} ({total_counts[classification]})"
        ax.bar(group_numbers, counts, bottom=[bottom_values[group] for group in group_numbers], label=label)
        for group in group_numbers:
            bottom_values[group] += classification_counts[group][classification]

    ax.set_xlabel(f'{choice} Groups (per {group_size})')
    ax.set_ylabel('Number of SATDs')
    ax.set_title(f'Number of SATDs per Classification Type per {group_size} {choice}')
    
    # Create a reversed legend (to match the stacked bar order)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], title='Classification Types (Total Count)')

    plt.show()


classification_counts = aggregate_data(input_csv_path, include_non_debt, group_size, data_column)
plot_stacked_bar_chart(classification_counts, group_size, choice)
