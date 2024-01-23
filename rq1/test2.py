import matplotlib.pyplot as plt
import seaborn as sns

# Set the aesthetic style of the plots
sns.set(style="whitegrid")

# Create a bar plot
plt.figure(figsize=(10, 6))
rejection_revision_rate.plot(kind='bar')
plt.title('Rejection/Revision Rate by SATD Classification')
plt.xlabel('SATD Classification')
plt.ylabel('Rejection/Revision Rate')
plt.xticks(rotation=45)  # Rotate labels for better readability
plt.tight_layout()
plt.show()
