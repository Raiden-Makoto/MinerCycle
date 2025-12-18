# this code visualizes the pareto front of the data
# the pareto front is the set of points a set of the best possible
# trade-off solutions when we have multiple, conflicting goals
# i.e both lighter AND stiffer

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns #type: ignore

df = pd.read_csv('materials.csv')

# remove diamond because it is an extreme outlier
df = df[(df["bulk_modulus"] < 600) & (df["density"] < 15)]
print(f"Plotting {len(df)} materials...")

df_sorted = df.sort_values("density")
pareto_boundary = []
max_stiffness = -1.0 

for _, row in df_sorted.iterrows():
    if row["bulk_modulus"] > max_stiffness:
        max_stiffness = row["bulk_modulus"]
        pareto_boundary.append(row)

pareto_values = pd.DataFrame(pareto_boundary)
print(f"Calculuated {len(pareto_boundary)} materials on the Pareto Front.")

plt.figure(figsize=(12,8))
sns.set_style('whitegrid')

# Plots all materials
plt.scatter(
    df['density'], 
    df['bulk_modulus'], 
    alpha = 0.3, 
    c = 'slategrey', 
    s = 15, 
    label = 'Existing Materials'
)

# Plot the Pareto Front
plt.plot(
    pareto_values['density'], 
    pareto_values['bulk_modulus'], 
    color='red', 
    linewidth=2, 
    marker='o', 
    markersize=5, 
    label='Pareto Front'
)

# Label Pareto Materials
for i, row in pareto_values.iterrows():
    if row["bulk_modulus"] >= 41:
        plt.text(
            row['density'] + 0.1, 
            row['bulk_modulus'], 
            row['formula'], 
            fontsize = 9, 
            color = 'darkred',
            fontweight = 'bold'
        )

plt.xlabel('Density (g/cm³)', fontsize=14)
plt.ylabel('Bulk Modulus (GPa)', fontsize=14)
plt.title('Material Discovery: Stiffness vs. Density Trade-off', fontsize=16)
plt.legend(fontsize=12)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

plt.savefig('pareto.png')
plt.close()
print("Saved image to \"figures/pareto.png\"")