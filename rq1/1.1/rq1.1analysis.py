import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '../..', '.env'))

# Get the absolute path to the folder where the CSV file is located
absolute_path_to_folder = os.getenv('ABSOLUTE_PATH_TO_FOLDER')
csv_file_path = os.path.join(absolute_path_to_folder, 'combined_checkpoints.csv')

# Load the data from the CSV file
df = pd.read_csv(csv_file_path)

# Filter out rows where classification is 'defect_debt'
df_filtered = df[df['classification'] != 'defect_debt']

# Group by classification and pr_status, then count occurrences
grouped = df_filtered.groupby(['classification', 'pr_status']).size().unstack(fill_value=0)

# Add a Total column for merged and closed PRs
grouped['Total'] = grouped['Merged'] + grouped['Closed']

# Calculate the acceptance rate for each classification
grouped['Acceptance_Rate'] = grouped['Merged'] / grouped['Total'] * 100  # Convert to percentage

# Calculate baseline acceptance rate for 'non_debt'
non_debt_acceptance_rate = grouped.loc['non_debt', 'Acceptance_Rate'] if 'non_debt' in grouped.index else 0

# Calculate acceptance rates relative to 'non_debt' classification
grouped['Relative_to_NonDebt'] = grouped['Acceptance_Rate'] - non_debt_acceptance_rate

# Prepare the final DataFrame for display
grouped_final = grouped.copy()
grouped_final['Acceptance_Rate'] = grouped_final['Acceptance_Rate'].round(2).astype(str) + '%'
grouped_final['Relative_to_NonDebt'] = grouped_final['Relative_to_NonDebt'].round(2).astype(str) + '%'

# Calculate mean and standard deviation of acceptance rates relative to 'non_debt'
relative_stats = {
    'Mean Relative Acceptance Rate': grouped['Relative_to_NonDebt'].mean(),
    'Standard Deviation of Relative Rates': grouped['Relative_to_NonDebt'].std(),
}

# Print results
print(grouped_final)
print({k: f'{v:.2f}%' for k, v in relative_stats.items()})


# Plotting
plt.figure(figsize=(14, 8))

# Acceptance Rate Plot
plt.subplot(1, 2, 1)  # 1 row, 2 columns, 1st subplot
ax1 = sns.barplot(x='Acceptance_Rate', y=grouped.index, data=grouped, palette="coolwarm")
plt.title('Acceptance Rate by Classification')
plt.xlabel('Acceptance Rate (%)')
plt.ylabel('Classification')

# Capitalize and format the y-axis labels for ax1
ax1.set_yticklabels([label.get_text().replace('_', ' ').capitalize() for label in ax1.get_yticklabels()])

# Relative to NonDebt Plot
plt.subplot(1, 2, 2)  # 1 row, 2 columns, 2nd subplot
ax2 = sns.barplot(x='Relative_to_NonDebt', y=grouped.index, data=grouped, palette="coolwarm")

plt.title('Relative Acceptance Rate to NonDebt by Classification')
plt.xlabel('Relative Acceptance Rate to NonDebt (%)')
plt.ylabel('')

# Extract text from Text objects and format the y-axis labels for ax2
ytick_labels = [label.get_text() for label in ax2.get_yticklabels()]
ytick_labels = [label.replace('_', ' ').capitalize() for label in ytick_labels]
ax2.set_yticklabels(ytick_labels)

plt.tight_layout()
plt.show()
