import pandas as pd
import os
from dotenv import load_dotenv

# Load the dataset
# Load environment variable from .env file
load_dotenv()

def read_csv_file(file_path, headers, skip_first_row):
    try:
        if skip_first_row:
            df = pd.read_csv(file_path, skiprows=1, header=None)
        else:
            df = pd.read_csv(file_path)

        df.columns = headers[:len(df.columns)]  # Align columns to headers

        # Add any missing columns
        for header in headers[len(df.columns):]:
            df[header] = None

        return df
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return pd.DataFrame()

def read_and_combine_csv_files(directory_path, output_file):
    first_file_path = os.path.join(directory_path, 'checkpoint_1.csv')
    first_file_df = pd.read_csv(first_file_path)
    headers = first_file_df.columns.tolist()

    combined_dataframe = first_file_df

    for i in range(2, 51):
        file_path = os.path.join(directory_path, f'checkpoint_{i}.csv')
        df = read_csv_file(file_path, headers, skip_first_row=True)
        combined_dataframe = pd.concat([combined_dataframe, df], ignore_index=True)

    combined_dataframe.to_csv(output_file, index=False)

# Example usage
    



# Access environment variable
absolute_path_to_folder = os.getenv('ABSOLUTE_PATH_TO_PROJ')

directory_path = os.path.join(absolute_path_to_folder, 'tools/csv/temp_data/')

output_file = 'combined_checkpoints.csv'  # Name of the output file
read_and_combine_csv_files(directory_path, output_file)
