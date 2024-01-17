import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from dotenv import load_dotenv

# Load the dataset
# Load environment variable from .env file
load_dotenv()

# Access environment variable
absolute_path_to_folder = os.getenv('ABSOLUTE_PATH_TO_FOLDER')

input_csv_path = os.path.join(absolute_path_to_folder, 'combined_checkpoints.csv')

data = pd.read_csv(input_csv_path)

# Ask the user if they want to include only merged PRs
include_only_merged = input("Include only merged PRs? (yes/no): ").strip().lower() == 'yes'

if include_only_merged:
    data = data[data['pr_status'] == 'Merged']

# Set the aesthetic style of the plots
sns.set(style="whitegrid")

# Calculate mean and median PR durations for each classification
mean_duration_by_classification = data.groupby('classification')['pr_duration_days'].mean()
median_duration_by_classification = data.groupby('classification')['pr_duration_days'].median()

# Visualization: Bar chart of mean and median PR duration for each classification
plt.figure(figsize=(12, 6))

# Plotting mean durations
mean_duration_by_classification.plot(kind='bar', position=0, color='lightblue', width=0.4, label='Mean Duration')

# Plotting median durations
median_duration_by_classification.plot(kind='bar', position=1, color='salmon', width=0.4, label='Median Duration')

plt.title('Mean and Median Time Before PR Merge by Classification')
plt.xlabel('Classification')
plt.ylabel('PR Duration (days)')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()