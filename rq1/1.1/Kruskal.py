import pandas as pd
import numpy as np
from scipy import stats
import scikit_posthocs as sp
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '../..', '.env'))

# Get the absolute path to the folder where the CSV file is located
absolute_path_to_folder = os.getenv('ABSOLUTE_PATH_TO_FOLDER')
csv_file_path = os.path.join(absolute_path_to_folder, 'combined_checkpoints.csv')

# Load the data from the CSV file
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

class KruskalWallisHTest:
    """
    A class to perform the Kruskal-Wallis H test on a dataset.
    """
    
    @staticmethod
    def test(data, groups, values):
        """
        Performs the Kruskal-Wallis H test on the given data.
        
        Parameters:
        - data: pd.DataFrame, the dataset containing the groups and values.
        - groups: str, the column name in the dataset representing the groups.
        - values: str, the column name in the dataset representing the values to test.
        
        Returns:
        - H statistic and p-value from the test.
        """
        data_groups = data.groupby(groups)[values].apply(list).to_dict()
        samples = list(data_groups.values())
        H, p_value = stats.kruskal(*samples)
        return H, p_value

class DunnsTest:
    """
    A class to perform Dunn's post-hoc test following a Kruskal-Wallis H test.
    """
    
    @staticmethod
    def test(data, groups, values):
        """
        Performs Dunn's post-hoc test to identify differences between groups.
        
        Parameters:
        - data: pd.DataFrame, the dataset containing the groups and values.
        - groups: str, the column name representing the groups.
        - values: str, the column name representing the values to test.
        
        Returns:
        - A DataFrame containing the p-values of the test between each pair of groups.
        """
        posthoc_results = sp.posthoc_dunn(data, val_col=values, group_col=groups, p_adjust='bonferroni')
        return posthoc_results

# Example usage:
# Assuming df is your DataFrame and 'classification' is the group column and 'Acceptance_Rate' is the value column.
# You might need to adjust the 'Acceptance_Rate' to numerical values before applying these tests.

# Kruskal-Wallis H Test
kruskal_results = KruskalWallisHTest.test(grouped, 'classification', 'Acceptance_Rate')
print(f'Kruskal-Wallis H Test Results: H={kruskal_results[0]}, p={kruskal_results[1]}')

# If Kruskal-Wallis test indicates significant differences, proceed with Dunn's Test
if kruskal_results[1] < 0.05:
    dunns_results = DunnsTest.test(grouped, 'classification', 'Acceptance_Rate')
    print('Dunn\'s Post-Hoc Test Results:')
    print(dunns_results)
