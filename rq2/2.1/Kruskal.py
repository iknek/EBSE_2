import pandas as pd
import os
import numpy as np
from scipy.stats import kruskal
import scikit_posthocs as sp
from dotenv import load_dotenv

class StatisticalAnalysis:
    def __init__(self):
        load_dotenv(os.path.join(os.path.dirname(__file__), '../..', '.env'))
        absolute_path_to_folder = os.getenv('ABSOLUTE_PATH_TO_FOLDER')
        self.csv_file_path = os.path.join(absolute_path_to_folder, '../../rq2/rq2.csv')
        self.df = None

    def load_data(self):
        self.df = pd.read_csv(self.csv_file_path)
        self.df = self.df[self.df['classification'] != 'defect_debt']

    def kruskal_wallis_test(self, group_column, value_column):
        """
        Perform Kruskal-Wallis H test on the provided dataframe.

        :param group_column: Column name for group classification
        :param value_column: Column name for values to be tested
        :return: Kruskal-Wallis H test result
        """
        self.load_data()  # Ensure data is loaded
        groups = self.df[group_column].unique()
        data = [self.df[self.df[group_column] == group][value_column] for group in groups]
        kruskal_result = kruskal(*data)
        print(f'Kruskal-Wallis H Test Results: H={kruskal_result[0]}, p={kruskal_result[1]}')
        return kruskal_result

    def dunn_test(self, group_column, value_column):
        """
        Perform Dunn's test for multiple comparisons following Kruskal-Wallis H test.

        :param group_column: Column name for group classification
        :param value_column: Column name for values to be tested
        :return: Dunn's test result as a DataFrame
        """
        if self.df is None:
            self.load_data()  # Ensure data is loaded
        data_groups = self.df[[group_column, value_column]]
        dunn_result = sp.posthoc_dunn(data_groups, val_col=value_column, group_col=group_column, p_adjust='bonferroni')
        print("Dunn's test result (with Bonferroni correction):")
        print(dunn_result)
        return dunn_result

if __name__ == "__main__":
    stat_analysis = StatisticalAnalysis()
    # Example usage:
    # Perform Kruskal-Wallis H test
    kruskal_result = stat_analysis.kruskal_wallis_test('classification', 'comments_count')
    # Perform Dunn's test if Kruskal-Wallis test is significant
    if kruskal_result.pvalue < 0.05:
        dunn_result = stat_analysis.dunn_test('classification', 'comments_count')
