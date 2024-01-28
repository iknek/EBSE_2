import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
import os

# Setup for plotting
sns.set(style="whitegrid")

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '../..', '.env'))

# Get the absolute path to the folder where the CSV file is located
absolute_path_to_folder = os.getenv('ABSOLUTE_PATH_TO_FOLDER')
csv_file_path = os.path.join(absolute_path_to_folder, 'combined_checkpoints.csv')
print(csv_file_path)
# Load the dataset
data = pd.read_csv(csv_file_path)

# RQ1.1: Analyzing PR Acceptance Rates by SATD Type
grouped_data = data.groupby(['classification', 'pr_status']).size().unstack(fill_value=0)
grouped_data['acceptance_rate'] = grouped_data['Merged'] / (grouped_data['Merged'] + grouped_data['Closed']) * 100
grouped_data.reset_index(inplace=True)

# Plotting the acceptance rate by SATD type
plt.figure(figsize=(12, 8))  # Increased figure size
ax = sns.barplot(x='classification', y='acceptance_rate', data=grouped_data)
plt.title('Acceptance Rate by SATD Classification')
plt.ylabel('Acceptance Rate (%)')
plt.xlabel('SATD Classification')

# Rotate x-axis labels if there are many classifications, to avoid overlap
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

# Optionally, adjust the font size for better readability
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

plt.tight_layout()  # Adjust the layout
plt.savefig(os.path.join(absolute_path_to_folder, '../../rq1/rq1_1.png'))

print("Graph generation complete. PNG file saved.")


# Group by 'classification' and 'pr_status' and count occurrences
grouped_data2 = data.groupby(['classification', 'pr_status']).size().unstack(fill_value=0)

# Calculate acceptance rate (merged) for each classification
grouped_data2['acceptance_rate'] = grouped_data['Merged'] / (grouped_data2['Merged'] + grouped_data2['Closed']) * 100

# Reset the index to make 'classification' a column
grouped_data2.reset_index(inplace=True)

# Exporting to a new CSV
grouped_data2.to_csv(os.path.join(absolute_path_to_folder, '../../rq1/rq1_1.csv'), index=False)
print("CSV Saved")
