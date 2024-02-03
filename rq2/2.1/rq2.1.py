import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats
from dotenv import load_dotenv

class PRCommentCountAnalysis:
    def __init__(self):
        load_dotenv(os.path.join(os.path.dirname(__file__), '../..', '.env'))
        absolute_path_to_folder = os.getenv('ABSOLUTE_PATH_TO_FOLDER')
        self.csv_file_path = os.path.join(absolute_path_to_folder, '../../rq2/rq2.csv')

    def load_data(self):
        df = pd.read_csv(self.csv_file_path)
        return df

    def filter_outliers(self, df):
        original_counts = df.groupby('classification')['comments_count'].count()
        df['z_score'] = df.groupby('classification')['comments_count'].transform(lambda x: stats.zscore(x, nan_policy='omit'))
        df_filtered = df[(df['z_score'] > -2) & (df['z_score'] < 2)]
        filtered_counts = df_filtered.groupby('classification')['comments_count'].count()
        removed_counts = original_counts - filtered_counts
        return df_filtered, removed_counts

    def analyze_comment_counts(self, exclude_outliers=False):
        df = self.load_data()
        df_filtered = df[df['classification'] != 'defect_debt']
        removed_counts = None

        if exclude_outliers:
            df_filtered, removed_counts = self.filter_outliers(df_filtered)

        grouped = df_filtered.groupby('classification')['comments_count'].agg(['mean', 'std'])
        non_debt_mean = grouped.loc['non_debt', 'mean']
        non_debt_std = grouped.loc['non_debt', 'std']
        grouped['Relative_Mean_Comments'] = grouped['mean'] - non_debt_mean
        grouped['Relative_Std_Comments'] = grouped['std'] - non_debt_std

        if exclude_outliers:
            grouped['Removed_Counts'] = removed_counts

        return grouped

    def generate_comment_count_table(self, grouped):
        columns = ['mean', 'std', 'Relative_Mean_Comments', 'Relative_Std_Comments']
        if 'Removed_Counts' in grouped.columns:
            columns.append('Removed_Counts')
        table = grouped[columns]
        table.rename(columns={
            'mean': 'Comment_Count_Mean', 
            'std': 'Comment_Count_Std',
            'Relative_Mean_Comments': 'Relative Comment_Count_Mean',
            'Relative_Std_Comments': 'Relative Comment_Count_Std',
            'Removed_Counts': 'Removed Data Points'}, inplace=True)
        return table

    def plot_comment_counts(self, grouped):
        grouped_df = grouped.reset_index()

        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)  # Mean PR Comment Counts Plot
        sns.barplot(x='mean', y='classification', data=grouped_df, palette="coolwarm")
        plt.title('Mean PR Comment Counts by Classification')
        plt.xlabel('Mean PR Comment Counts')
        plt.ylabel('Classification')

        plt.subplot(1, 2, 2)  # Relative Mean PR Comment Counts Plot
        sns.barplot(x='Relative_Mean_Comments', y='classification', data=grouped_df, palette="coolwarm")
        plt.title('Relative Mean PR Comment Counts by Classification')
        plt.xlabel('Relative Mean PR Comment Counts')
        plt.ylabel('')

        plt.tight_layout()
        plt.show()

    def perform_analysis(self):
        exclude_outliers_input = input("Would you like to exclude outliers based on z-score? (yes/no): ").lower()
        exclude_outliers = exclude_outliers_input == 'yes'

        grouped = self.analyze_comment_counts(exclude_outliers)
        self.plot_comment_counts(grouped)

        table = self.generate_comment_count_table(grouped)
        print("Comment Counts Table:")
        print(table)

if __name__ == "__main__":
    analyzer = PRCommentCountAnalysis() 
    analyzer.perform_analysis()