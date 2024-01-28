import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from dotenv import load_dotenv

class PRResolutionTimeAnalysis:
    def __init__(self):
        load_dotenv(os.path.join(os.path.dirname(__file__), '../..', '.env'))
        # Get the absolute path to the folder where the CSV file is located
        absolute_path_to_folder = os.getenv('ABSOLUTE_PATH_TO_FOLDER')
        self.csv_file_path = os.path.join(absolute_path_to_folder, 'combined_checkpoints.csv')

    def load_data(self):
        # Load the data from the CSV file
        df = pd.read_csv(self.csv_file_path)

        # Filter out rows where classification is 'defect_debt' since we only have 1 of those
        df_filtered = df[df['classification'] != 'defect_debt']

        return df_filtered

    def analyze_resolution_time(self, df, exclude_outliers=False):
        # Group by classification and calculate mean and standard deviation of PR duration
        if exclude_outliers:
            # Exclude outliers based on z-score for each classification
            df_filtered = self.calculate_z_scores(df)
            df = df_filtered[(df_filtered['z_score'] >= -2) & (df_filtered['z_score'] <= 2)]
            count_removed = df_filtered.shape[0] - df.shape[0]  # Count removed when excluding outliers
        else:
            count_removed = 0  # No data points removed when not excluding outliers

        grouped = df.groupby('classification')['pr_duration_days'].agg(['mean', 'std', 'count'])

        # Calculate the mean and standard deviation of PR duration for all classifications
        overall_mean = df['pr_duration_days'].mean()
        overall_std = df['pr_duration_days'].std()

        # Calculate the mean and standard deviation relative to the 'non_debt' classification
        non_debt_mean = grouped.loc['non_debt', 'mean']
        non_debt_std = grouped.loc['non_debt', 'std']

        grouped['Relative_Mean_Duration'] = grouped['mean'] - non_debt_mean
        grouped['Relative_Std_Duration'] = grouped['std'] - non_debt_std
        grouped['Data Points Removed'] = count_removed
        print(count_removed)
        return grouped

    def calculate_z_scores(self, df):
        df['z_score'] = (df['pr_duration_days'] - df.groupby('classification')['pr_duration_days'].transform('mean')) / df.groupby('classification')['pr_duration_days'].transform('std')
        return df

    def generate_table(self, grouped, df_filtered, exclude_outliers):
        # Create a table
        table = grouped[['mean', 'std', 'Relative_Mean_Duration', 'Relative_Std_Duration']]

        # Rename existing columns
        table.rename(columns={'mean': 'Mean Duration (days)', 'std': 'Standard Deviation for Mean (days)',
                            'Relative_Mean_Duration': 'Relative Mean Duration (days)',
                            'Relative_Std_Duration': 'Relative Standard Deviation for Mean (days)'}, inplace=True)

        return table


    def plot_resolution_time(self, grouped):
        # Calculate Relative Mean Duration (days) for each classification
        grouped['Relative Mean Duration (days)'] = grouped['mean'] - grouped.loc['non_debt', 'mean']

        # Plotting
        plt.figure(figsize=(12, 6))

        # Mean PR Duration Plot
        plt.subplot(1, 2, 1)  # 1 row, 2 columns, 1st subplot
        ax1 = sns.barplot(x='mean', y='classification', data=grouped, palette="coolwarm")
        plt.title('Mean PR Duration by Classification')
        plt.xlabel('Mean PR Duration (days)')
        plt.ylabel('Classification')

        # Relative Mean Duration Plot
        plt.subplot(1, 2, 2)  # 1 row, 2 columns, 2nd subplot
        ax2 = sns.barplot(x='Relative Mean Duration (days)', y='classification', data=grouped, palette="coolwarm")
        plt.title('Relative Mean Duration by Classification')
        plt.xlabel('Relative Mean Duration (days)')
        plt.ylabel('Classification')

        plt.tight_layout()
        plt.show()



    def perform_analysis(self, exclude_outliers=False):
        df = self.load_data()
        grouped = self.analyze_resolution_time(df, exclude_outliers)
        self.plot_resolution_time(grouped)

        # Generate and print the table
        table = self.generate_table(grouped, df, exclude_outliers)
        print(table)

if __name__ == "__main__":
    analyzer = PRResolutionTimeAnalysis()

    # Ask the user if they want to exclude outliers
    exclude_outliers = input("Do you want to exclude outliers? (yes/no): ").lower()
    if exclude_outliers == "yes":
        exclude_outliers = True
    else:
        exclude_outliers = False

    analyzer.perform_analysis(exclude_outliers)
