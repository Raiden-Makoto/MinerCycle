# this script visualizes our novel discovered materials on the pareto plot
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

try:
    materials = 'data/materials_cleaned.csv'
    df = pd.read_csv(materials)
    df = df[(df['bulk_modulus'] < 450) & (df['density'] < 12)]
except FileNotFoundError:
    print(f"File Not Found: {materials}")
    raise SystemExit(1)

try:
    candidates = 'data/candidates.csv'
    cand = pd.read_csv(candidates)
    top10 = cand.sort_values('specific_stiffness', ascending=False)
except FileNotFoundError:
    print(f"File Not Found: {candidates}")
    raise SystemExit(1)

# Calculate the Pareto Front
densities = df.sort_values('density')
pareto_boundary = []
max_stiffness = -1.0

for _, row in densities.iterrows():
    if row['bulk_modulus'] > max_stiffness:
        pareto_boundary.append(row)
        max_stiffness = row['bulk_modulus']

pareto_df = pd.DataFrame(pareto_boundary)

# Plot the Data
plt.figure(figsize=(12, 8))
sns.set_style("whitegrid")

# Existing Data
plt.scatter(
    df['density'],
    df['bulk_modulus'], 
    alpha=0.15,
    color='slategrey',
    s=15,
    label='Existing Database'
)

# Pareto Front
plt.plot(
    pareto_df['density'],
    pareto_df['bulk_modulus'], 
    color='firebrick',
    linewidth=2,
    alpha=0.6,
    linestyle='--',
    label='Pareto Front (Curr. Eff. Limit)'
)

# Novel Candidates
plt.scatter(
    top10['pred_density'],
    top10['pred_bulk_modulus'], 
    color='gold',
    marker='*',
    s=300,
    edgecolors='black',
    linewidth=1.0, 
    label='Top Candidates',
    zorder=10
)

for _, row in top10.sort_values('pred_density').iterrows():
    label = f"{row['formula']}"
    plt.text(
        row['pred_density'] + 0.1,
        row['pred_bulk_modulus'], 
        label,
        fontsize=10,
        fontweight='bold',
        color='darkgoldenrod'
    )

plt.title("Material Discovery: Novel Candidates vs. Known Materials", fontsize=16, fontweight='bold')
plt.xlabel('Density (g/cm³)', fontsize=12)
plt.ylabel('Stiffness (Bulk Modulus GPa)', fontsize=12)
plt.legend(loc='upper left', frameon=True, framealpha=0.9)
plt.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.savefig("portfolio_plot.png")
print("Plot saved to \"portfolio_plot.png\"")