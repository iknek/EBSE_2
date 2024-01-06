# Repo for our Course Project

## Tools Available
1. **CountClassifications.py** - Counts the number of each classification (code_debt, architecture_debt, non_debt, etc). Running it will prompt for you to choose from either (1) Pull Requests, (2) Code Comments, (3) Commit Messages, or (4) Dataset Issues.
2. **plotClassifications.py** - Plots a bar graph where the Y-axis is the number of total SATDs, and the X-axis is *either* the number of Dataset Issues or Pull Requests /Z (where Z is the number of either metric aggregated per one bar). Each bar is divided horizaontally (i.e. along the corresponding y height), to indicate the proportion of each classification. Running it will prompt for you to choose the metric, if non-debt should be included, and the Z value.
3. **sortPRsOrIssues.py** - Simply sorts their the original pull request CSV, or the dataset issues CSV into a new CSV ordered by PR/Issue number.

## To run the files
1. Install python
2. Run the following in your console:
- "pip install python-dotenv"
3. Make a .env in the tools directory, and set the absolut path to the csv folder
- For example: 
`
ABSOLUTE_PATH_TO_FOLDER='C:/Users/Data/Desktop/satd-different-sources-data-main/tools/csv/'
`
4. Simply run a tool/class using:
` 
python 
`