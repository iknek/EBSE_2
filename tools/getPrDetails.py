import requests
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

def get_pr_duration_and_status(owner, repo, pr_number, token):
    """
    Get the duration in days between the creation and merge or closure of a pull request,
    and also check if it was closed or neither.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    headers = {'Authorization': f'token {token}'}
    print(url)

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve PR data: {e}")
        time.sleep(20)  # Wait for 20 seconds
        return None

    pr_data = response.json()
    created_at = pr_data.get('created_at')
    merged_at = pr_data.get('merged_at')
    closed_at = pr_data.get('closed_at')

    if not created_at:
        print("PR is missing creation date.")
        return None

    created_at = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
    
    if merged_at:
        merged_at = datetime.strptime(merged_at, "%Y-%m-%dT%H:%M:%SZ")
        duration = (merged_at - created_at).days
        status = 'Merged'
    elif closed_at:
        closed_at = datetime.strptime(closed_at, "%Y-%m-%dT%H:%M:%SZ")
        duration = (closed_at - created_at).days
        status = 'Closed'
    else:
        duration = None
        status = 'Not Closed or Merged'
    
    return duration, status

# Create a temporary folder to store data and checkpoints
temp_folder = 'temp_data'
os.makedirs(temp_folder, exist_ok=True)
absolute_path_to_folder = os.getenv('ABSOLUTE_PATH_TO_FOLDER')
csv_file_path = os.path.join(absolute_path_to_folder, 'satd-dataset-pull_requests.csv')

# Load CSV file
data = pd.read_csv(csv_file_path)

# GitHub token
token = os.getenv('GH_TOEKN')

# Create an empty list to store updated rows
updated_rows = []

# Checkpoint counter and file name
checkpoint_counter = 0
checkpoint_file_number = 51

# Define the checkpoint interval
checkpoint_interval = 100

# Iterate through the data and update rows
for index, row in data.iterrows():
    owner = row['repo_owner']
    repo = row['project']
    pr_number = row['pull_number']
    
    duration, status = get_pr_duration_and_status(owner, repo, pr_number, token)

    # Update the 'pr_duration_days' and 'pr_status' columns
    row['pr_duration_days'] = duration
    row['pr_status'] = status

    # Remove the 'text' column from the row
    row = row.drop(['text'])

    # Append the updated row to the list
    updated_rows.append(row)

    checkpoint_counter += 1

    # Check if it's time to create a checkpoint
    if checkpoint_counter >= checkpoint_interval:
        # Convert the list of updated rows to a DataFrame
        updated_data = pd.DataFrame(updated_rows)

        # Save the updated data to a checkpoint CSV file
        checkpoint_file_path = os.path.join(temp_folder, f'checkpoint_{checkpoint_file_number}.csv')
        updated_data.to_csv(checkpoint_file_path, index=False)

        print(f"Checkpoint {checkpoint_file_number} saved.")
        
        # Reset the counter and clear the list for the next checkpoint
        checkpoint_counter = 0
        checkpoint_file_number += 1
        updated_rows = []

# Convert the remaining updated rows to a DataFrame
updated_data = pd.DataFrame(updated_rows)

# Save the final updated data to a single CSV file
updated_csv_file_path = os.path.join(temp_folder, 'updated_data.csv')
updated_data.to_csv(updated_csv_file_path, index=False)

print("Updated CSV file saved.")

# Save the final checkpoint count to the count file
with open(count_file_path, 'w') as count_file:
    count_file.write(str(checkpoint_counter))
