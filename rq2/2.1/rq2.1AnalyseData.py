import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv

class SATDAnalysis:
    def __init__(self):
        # Load environment variables
        load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

        # Get the absolute path to the folder where the CSV file is located
        absolute_path_to_folder = os.getenv('ABSOLUTE_PATH_TO_FOLDER')
        csv_file_path = os.path.join(absolute_path_to_folder, '../../rq2/rq2_1.csv')

        # Load the data
        self.data = pd.read_csv(csv_file_path)

    def correlation_analysis(self):
        # Add a binary 'rejected' column for correlation analysis
        self.data['rejected'] = self.data['pr_status'] == 'Closed'  # Assuming 'Closed' means rejected
        return self.data[['comments_count', 'commits_count', 'rejected']].corr()

    def calculate_averages(self):
        # Group by classification and calculate mean
        return self.data.groupby(['classification', 'pr_status']).agg({'comments_count': 'mean', 'commits_count': 'mean'}).reset_index()

    def visualize_averages(self, avg_data, metric):
        # Visualization of average comments/commits
        plt.figure(figsize=(10, 6))
        sns.barplot(x='classification', y=metric, hue='pr_status', data=avg_data)
        plt.xticks(rotation=45)
        plt.title(f'Average {metric} per SATD Classification')
        plt.show()

# Usage
analysis = SATDAnalysis()
correlation_matrix = analysis.correlation_analysis()
average_data = analysis.calculate_averages()

print("Correlation Matrix:")
print(correlation_matrix)

print("\nAverage Comments and Commits:")
print(average_data)

# Visualize average comments count
analysis.visualize_averages(average_data, 'comments_count')

# Visualize average commits count
analysis.visualize_averages(average_data, 'commits_count')