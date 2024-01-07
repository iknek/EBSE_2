from dotenv import load_dotenv
import os
import csv
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

# Load environment variable from .env file
load_dotenv()

# Access environment variable
absolute_path_to_folder = os.getenv('ABSOLUTE_PATH_TO_FOLDER')

# Ask user which data set to plot
data_set_choice = input("Which dataset would you like to plot - (1) 'Pull Requests', or (2) 'Issues': ")

if data_set_choice == '1':
    data_column = 'pull_number'
    input_csv_path = os.path.join(absolute_path_to_folder, 'sortedPullRequests.csv')
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
    print(f"Invalid input for the number of {choice} per group. Using default value of 100.")
    group_size = 100

def aggregate_data(csv_file_path, include_non_debt, group_size, data_column):
    satd_count = 0
    total_count = 0
    proportions = []
    time_groups = []

    with open(csv_file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            total_count += 1
            if row['classification'] != 'non_debt':
                satd_count += 1
            if total_count % group_size == 0:
                proportions.append((satd_count / total_count) * 100)
                time_groups.append(total_count // group_size)

    return time_groups, proportions

def plot_with_trend_line(csv_file_path, group_size, choice):
    time_groups, proportions = aggregate_data(csv_file_path, include_non_debt, group_size, data_column)

    # Convert to numpy arrays for numerical operations
    x = np.array(time_groups)
    y = np.array(proportions)

    # Plotting the points
    plt.scatter(x, y, color='blue', label='Data Points')

    # Calculating and plotting the trend line
    z = np.polyfit(x, y, 1)  # Linear fit
    p = np.poly1d(z)
    plt.plot(x, p(x), color='red', linestyle='-', linewidth=2, label='Trend Line')

    # Trend line equation y = mx + b
    slope, intercept = z
    trend_line_eq = f"y = {slope:.2f}x + {intercept:.2f}"

    # Adding labels, title, and trend line equation
    plt.xlabel(f'{choice} Groups (per {group_size})')
    plt.ylabel('Proportion of SATDs (%)')
    plt.title(f'Proportion of SATDs Over Time with Trend Line in {choice}')
    plt.legend()
    plt.text(min(x), max(y), trend_line_eq, fontsize=12, color='red')

    # Show plot
    plt.show()

plot_with_trend_line(input_csv_path, group_size, choice)
