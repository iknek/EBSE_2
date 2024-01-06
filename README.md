# Repo for our Course Project

## Tools Available
1. **CountNumbOfClassifications.py** - Counts the number of each classification (code_debt, architecture_debt, non_debt, etc). Running it will prompt for you to choose from either (1) Pull Requests, (2) Code Comments, or (3) Commit Messages.
2. **plotClassificationsPerPullReqs.py** - Plots a bar graph where the Y-axis is the number of total SATDs, and the X-axis is the number of Pull Requests/Z (where Z is the number of pull requests aggregated into one bar). Each bar is divided horizaontally (i.e.along the corresponding y height), to indicate the proportion of each classification. Running it will prompt for you to choose if non-debt should be included, and the Z value.
3. **sortPullReqCSV.py** - Simply sorts the original pull request CSV into one ordered by PR number.

## To run the files
1. Install python
2. Run the following in your console:
- "pip install python-dotenv"
3. Make a .env in the tools directory, and set the absolut path to the csv folder
- For example: 
```
"ABSOLUTE_PATH_TO_FOLDER='C:/Users/Data/Desktop/satd-different-sources-data-main/tools/csv/'" 
```
