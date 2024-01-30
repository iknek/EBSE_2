import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
from dotenv import load_dotenv
from scipy.stats import kruskal

class SATDCommentAnalysis:
    def __init__(self):
        load_dotenv(os.path.join(os.path.dirname(__file__), '../..', '.env'))
        absolute_path_to_folder = os.getenv('ABSOLUTE_PATH_TO_FOLDER')
        self.csv_file_path = os.path.join(absolute_path_to_folder, '../../rq2/rq2.csv')
        self.data = self.load_data()

    def load_data(self):
        df = pd.read_csv(self.csv_file_path)
        return df[df['classification'] != 'defect_debt']  # Assuming you want to exclude 'defect_debt' as before

    def encode_classifications(self):
        # Example encoding, adjust according to your SATD classifications
        encoding = {'architecture_debt' : 1, 'build_debt' : 2, 'code_debt': 3, 'design_debt': 4, 'documentation_debt': 5, 'non_debt': 6, 'requirement_debt' : 7 , 'test_debt' : 8}
        self.data['classification_encoded'] = self.data['classification'].map(encoding)

    def perform_kruskal_test(self):
        # Group data by classification and extract comment counts
        groups = [group["comments_count"].values for name, group in self.data.groupby("classification")]
        kruskal_test_result = kruskal(*groups)
        return kruskal_test_result

    def plot_comment_counts(self):
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='classification', y='comments_count', data=self.data, palette="coolwarm")
        plt.title('PR Comment Counts by SATD Classification')
        plt.xlabel('SATD Classification')
        plt.ylabel('PR Comment Counts')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def analyze(self):
        self.encode_classifications()  # Optional, comment out if not needed
        test_result = self.perform_kruskal_test()
        print(f"Kruskal-Wallis H-test result: {test_result}")
        self.plot_comment_counts()

if __name__ == "__main__":
    analysis = SATDCommentAnalysis()
    analysis.analyze()
