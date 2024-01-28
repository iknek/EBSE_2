import os
import requests
import pandas as pd
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '../..', '.env'))

# Get the absolute path to the folder where the CSV file is located
absolute_path_to_folder = os.getenv('ABSOLUTE_PATH_TO_FOLDER')
csv_file_path = os.path.join(absolute_path_to_folder, 'combined_checkpoints.csv')

# GitHub token and setup
token = os.getenv('GH_TOKEN')
headers = {'Authorization': f'token {token}'}

def get_pr_additional_info(owner, repo, pr_number, headers):
    """
    Fetch additional information for a PR: number of commits, number of comments, and labels.
    """
    commits_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/commits"
    comments_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/comments"
    labels_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/labels"
    try:
        # Get the number of commits
        commits_response = requests.get(commits_url, headers=headers)
        commits_response.raise_for_status()
        commits_count = len(commits_response.json())

        # Get the number of comments
        comments_response = requests.get(comments_url, headers=headers)
        comments_response.raise_for_status()
        comments_count = len(comments_response.json())

        # Get the labels
        labels_response = requests.get(labels_url, headers=headers)
        labels_response.raise_for_status()
        labels = [label['name'] for label in labels_response.json()]
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        time.sleep(20)  # Wait for 20 seconds before trying again
        return None

    return commits_count, comments_count, labels

# Load existing data
data = pd.read_csv(csv_file_path)

# Add columns for additional information
data['commits_count'] = 0
data['comments_count'] = 0
data['labels'] = ''

# Directory for temporary storage
temp_dir = os.path.join(os.path.dirname(__file__), 'temp2')
os.makedirs(temp_dir, exist_ok=True)

# Initialize variables for checkpointing
processed_data = []
checkpoint_counter = 0
checkpoint_file_number = 1

# Fetch and add additional data
for index, row in data.iterrows():
    info = get_pr_additional_info(row['repo_owner'], row['project'], row['pull_number'], headers)
    if info is not None:
        commits_count, comments_count, labels = info
        row['commits_count'] = commits_count
        row['comments_count'] = comments_count
        row['labels'] = ', '.join(labels)
    
    processed_data.append(row)
    checkpoint_counter += 1
    print(checkpoint_counter)
    # Checkpoint every 50 entries
    if checkpoint_counter >= 50:
        checkpoint_df = pd.DataFrame(processed_data)
        checkpoint_file = os.path.join(temp_dir, f'checkpoint_{checkpoint_file_number}.csv')
        checkpoint_df.to_csv(checkpoint_file, index=False)
        processed_data = []
        checkpoint_counter = 0
        checkpoint_file_number += 1

    # To avoid hitting the API rate limit, consider adding a delay here
    time.sleep(0.1)

# Save any remaining data after the loop
if processed_data:
    checkpoint_df = pd.DataFrame(processed_data)
    checkpoint_file = os.path.join(temp_dir, f'checkpoint_{checkpoint_file_number}.csv')
    checkpoint_df.to_csv(checkpoint_file, index=False)

# Save the final augmented dataset
augmented_csv_file_path = os.path.join(absolute_path_to_folder, '../../rq2/rq2.csv')
data.to_csv(augmented_csv_file_path, index=False)

print("Data collection complete. Augmented dataset and checkpoints saved.")
