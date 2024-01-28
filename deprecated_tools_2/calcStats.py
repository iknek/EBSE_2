import pandas as pd
import os
from dotenv import load_dotenv

# Load the dataset
# Load environment variable from .env file
load_dotenv()

# Re-loading the dataset
# Access environment variable
absolute_path_to_folder = os.getenv('ABSOLUTE_PATH_TO_FOLDER')

path = os.path.join(absolute_path_to_folder, 'combined_checkpoints.csv')

data = pd.read_csv(path)

# Grouping the data by classification and calculating the mean PR duration
mean_durations = data.groupby('classification')['pr_duration_days'].mean()

# Extracting the mean duration for 'non_debt'
non_debt_mean_duration = mean_durations['non_debt']

# Calculating the difference in mean duration for each classification type compared to 'non_debt'
duration_differences = mean_durations - non_debt_mean_duration

# Calculating the percentage difference
percentage_differences = (duration_differences / non_debt_mean_duration) * 100

percentage_differences_rounded = percentage_differences.round(2)

print(percentage_differences_rounded, "%")

