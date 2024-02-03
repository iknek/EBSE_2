import pandas as pd
import os
import numpy as np
from scipy import stats
from scikit_posthocs import posthoc_dunn
from dotenv import load_dotenv

class StatisticalAnalysis:
    def __init__(self):
        load_dotenv(os.path.join(os.path.dirname(__file__), '../..', '.env'))
        absolute_path_to_folder = os.getenv('ABSOLUTE_PATH_TO_FOLDER')
        self.csv_file_path = os.path.join(absolute_path_to_folder, '../../rq2/rq2.csv')

    def load_data(self):
        df = pd.read_csv(self.csv_file_path)
        df = df[df['classification'] != 'defect_debt']
        df = df.dropna(subset=['pr_duration_days'])
        return df

    def perform_kruskal_wallis_test(self, df, column='pr_duration_days', group_column='classification'):
        """
        Perform Kruskal-Wallis H test to determine if there are significant differences
        between two or more groups of an independent variable on a continuous or ordinal dependent variable.
        """
        unique_groups = df[group_column].unique()
        groups_data = [df[df[group_column] == group][column] for group in unique_groups if not df[df[group_column] == group][column].isnull().all()]

        kruskal_result = stats.kruskal(*groups_data)
    
        print(f'Kruskal-Wallis H Test Results: H={kruskal_result[0]}, p={kruskal_result[1]}')

        if kruskal_result.pvalue < 0.05:
            print("There are significant differences between the groups.")
        else:
            print("No significant differences were found between the groups.")

        return kruskal_result

    def perform_dunns_test(self, df, column='pr_duration_days', group_column='classification'):
        """
        Perform Dunn's test for multiple comparisons, to be used post Kruskal-Wallis if significant.
        """
        data = df[[group_column, column]].dropna()
        result = posthoc_dunn(data, val_col=column, group_col=group_column, p_adjust='bonferroni')
        
        print("Dunn's test result for multiple comparisons:")
        print(result)

        return result

if __name__ == "__main__":
    stat_analysis = StatisticalAnalysis()
    df = stat_analysis.load_data()

    print("\nPerforming Kruskal-Wallis H test...")
    stat_analysis.perform_kruskal_wallis_test(df)

    print("\nPerforming Dunn's test...")
    stat_analysis.perform_dunns_test(df)