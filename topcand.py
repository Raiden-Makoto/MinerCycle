# Top Candidate: Nb2SiC
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Data: Your Top Candidate vs. Common Industry Materials
data = {
    'Material': ['Standard Steel', 'Titanium Alloy', 'Aluminum Alloy', 'Your Discovery (Nb2SiC)', 'Diamond (Theoretical Limit)'],
    'Specific_Stiffness': [25, 26, 26, 43, 126], # Approx values for Steel/Ti/Al/Diamond
    'Type': ['Industry Standard', 'Industry Standard', 'Industry Standard', 'AI Discovery', 'Limit']
}

df_compare = pd.DataFrame(data)

# Plot
plt.figure(figsize=(10, 6))
sns.set_style("whitegrid")

# Create colors: Grey for old stuff, Gold for yours, Red for the limit
colors = ['slategrey', 'slategrey', 'slategrey', 'gold', 'firebrick']

ax = sns.barplot(x='Material', y='Specific_Stiffness', data=df_compare, palette=colors)

# Add numbers on top of bars
for i, v in enumerate(df_compare['Specific_Stiffness']):
    ax.text(i, v + 2, str(v), color='black', ha='center', fontweight='bold')

plt.title("Performance Comparison: AI Candidate vs. Industry Standards", fontsize=14, fontweight='bold')
plt.ylabel("Specific Stiffness (GPa / g/cm³)", fontsize=12)
plt.xlabel("")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('figures/topcand.png')