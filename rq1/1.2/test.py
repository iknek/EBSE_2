import pandas as pd
from scipy import stats
import os
from dotenv import load_dotenv

# Read the CSV file into a DataFrame
load_dotenv(os.path.join(os.path.dirname(__file__), '../..', '.env'))
absolute_path_to_folder = os.getenv('ABSOLUTE_PATH_TO_FOLDER')
csv_file_path = os.path.join(absolute_path_to_folder, 'combined_checkpoints2.csv')

df = pd.read_csv(csv_file_path)

# Step 1: Calculate the mean pr_duration_days for each classification
mean_duration_by_classification = df.groupby('classification')['pr_duration_days'].mean()

# Step 2: Define a function to filter outliers based on z-score
def filter_outliers(group):
    # Calculate z-scores for each PR within its classification
    group['z_score'] = stats.zscore(group['pr_duration_days'])
    # Filter based on z-scores
    return group[(group['z_score'] >= -2) & (group['z_score'] <= 2)]

# Step 3: Apply the filtering function and calculate the mean after removing outliers
filtered_data = df.groupby('classification').apply(filter_outliers).reset_index(drop=True)
mean_duration_after_filter = filtered_data.groupby('classification')['pr_duration_days'].mean().reset_index()

# Display the results
print("Mean PR Duration Days for Each Classification:")
print(mean_duration_by_classification)

print("\nMean PR Duration Days for Each Classification After Removing Outliers:")
print(mean_duration_after_filter)