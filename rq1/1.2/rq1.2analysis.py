import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats
from dotenv import load_dotenv

class PRResolutionTimeAnalysis:
    def __init__(self):
        load_dotenv(os.path.join(os.path.dirname(__file__), '../..', '.env'))
        absolute_path_to_folder = os.getenv('ABSOLUTE_PATH_TO_FOLDER')
        self.csv_file_path = os.path.join(absolute_path_to_folder, '../../rq2/rq2.csv')

    def load_data(self):
        df = pd.read_csv(self.csv_file_path)
        return df

    def filter_outliers(self, df, z_score_threshold=2):
        outliers_indices = pd.Series([], dtype=bool)
        
        for classification, group in df.groupby('classification'):
            pr_duration = group['pr_duration_days']
            valid_indices = ~pr_duration.isna()  # Filter out rows with missing values
            pr_duration_valid = pr_duration[valid_indices]
            
            if len(pr_duration_valid) > 1:  # Check if there are enough data points for z-score calculation
                z_scores = stats.zscore(pr_duration_valid, nan_policy='omit')
                is_outlier = abs(z_scores) > z_score_threshold
                outliers_indices = outliers_indices | (valid_indices & is_outlier)

        df_filtered = df[~outliers_indices]
        removed_counts = df.shape[0] - df_filtered.shape[0]
        return df_filtered, removed_counts

    def analyze_resolution_time(self, df, exclude_outliers=False):
        if exclude_outliers:
            df, removed_counts = self.filter_outliers(df)
        else:
            removed_counts = 0

        grouped = df.groupby('classification')['pr_duration_days'].agg(['mean', 'std'])
        non_debt_mean = grouped.loc['non_debt', 'mean']
        non_debt_std = grouped.loc['non_debt', 'std']

        grouped['Relative Mean Duration (days)'] = grouped['mean'] - non_debt_mean
        grouped['Relative Standard Deviation for Mean (days)'] = grouped['std'] - non_debt_std
        grouped['Data Points Removed'] = removed_counts

        return grouped

    def perform_analysis(self, exclude_outliers=False):
        df = self.load_data()
        df = df[df['classification'] != 'defect_debt']  # Exclude defect_debt

        grouped = self.analyze_resolution_time(df, exclude_outliers)

        print("Resolution Time Analysis Table:")
        print(grouped)

        if exclude_outliers:
            print("Total Outliers Removed:", grouped['Data Points Removed'].sum())

        # Plot the results
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        sns.barplot(x='mean', y='classification', data=grouped.reset_index(), palette="coolwarm")
        plt.title('Mean PR Resolution Time by Classification')
        plt.xlabel('Mean PR Resolution Time (days)')
        plt.ylabel('Classification')

        plt.subplot(1, 2, 2)
        sns.barplot(x='Relative Mean Duration (days)', y='classification', data=grouped.reset_index(), palette="coolwarm")
        plt.title('Relative Mean PR Resolution Time by Classification')
        plt.xlabel('Relative Mean PR Resolution Time (days)')
        plt.ylabel('')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    analyzer = PRResolutionTimeAnalysis()
    exclude_outliers_input = input("Do you want to exclude outliers? (yes/no): ").lower()
    exclude_outliers = exclude_outliers_input == 'yes'
    analyzer.perform_analysis(exclude_outliers)
