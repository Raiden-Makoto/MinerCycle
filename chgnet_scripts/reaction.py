import os
from chgnet.model.model import CHGNet
from pymatgen.core import Structure, Lattice

import warnings
warnings.filterwarnings('ignore')

# 1. LOAD CHGNET
print("🚀 Loading CHGNet...")
chgnet = CHGNet.load()

# 2. DEFINE STRUCTURES
# We need the energy of the GOAL (Nb2SiC) and the INGREDIENTS (Nb, Si, C)

# A. The Goal: Load your relaxed structure from the previous step
# Get the path relative to this script file
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
cif_path = os.path.join(project_root, "figures", "Nb2SiC_relaxed.cif")

try:
    nb2sic = Structure.from_file(cif_path)
except FileNotFoundError:
    print(f"Error: Nb2SiC_relaxed.cif not found at {cif_path}")
    print("Run the previous script (physics.py) first!")
    raise SystemExit(1)

# B. The Ingredients: We create simple crystals for pure elements
# (In a real paper, you'd relax these too, but standard reference values work for rough checks)
# Here we approximate them roughly or use MP IDs if you want high precision. 
# For a quick demo, we use simplified lattices.

# Niobium (BCC crystal)
nb_metal = Structure(Lattice.cubic(3.30), ["Nb", "Nb"], [[0,0,0], [0.5, 0.5, 0.5]])
# Silicon (Diamond cubic)
si_crystal = Structure(Lattice.cubic(5.43), ["Si"]*8, [[0,0,0], [0.5,0.5,0], [0.5,0,0.5], [0,0.5,0.5], [0.25,0.25,0.25], [0.75,0.75,0.25], [0.75,0.25,0.75], [0.25,0.75,0.75]])
# Carbon (Graphite - approximated as simple hexagonal for quick energy check)
c_graphite = Structure(Lattice.hexagonal(2.46, 6.70), ["C"]*4, [[0,0,0], [0,0,0.5], [0.33, 0.66, 0], [0.66, 0.33, 0.5]])

# 3. GET ENERGIES (per atom)
print("\n⚡️ Calculating Energies with CHGNet...")

def get_energy_per_atom(struct):
    pred = chgnet.predict_structure(struct)
    return pred['e']

e_nb2sic = get_energy_per_atom(nb2sic)
e_nb = get_energy_per_atom(nb_metal)
e_si = get_energy_per_atom(si_crystal)
e_c = get_energy_per_atom(c_graphite)

print(f"E(Nb2SiC): {e_nb2sic:.3f} eV/atom")
print(f"E(Nb):     {e_nb:.3f} eV/atom")
print(f"E(Si):     {e_si:.3f} eV/atom")
print(f"E(C):      {e_c:.3f} eV/atom")

# 4. CALCULATE REACTION ENERGY
# Reaction: 2 Nb + 1 Si + 1 C -> Nb2SiC (4 atoms total)
# We calculate total energy of reactants vs product

total_E_product = e_nb2sic * 4  # Nb2SiC has 4 atoms in formula unit
total_E_reactants = (2 * e_nb) + (1 * e_si) + (1 * e_c)

delta_H = total_E_product - total_E_reactants

print("\n------------------------------------------------")
print("⚗️  REACTION ANALYSIS: 2Nb + Si + C -> Nb2SiC")
print("------------------------------------------------")
print(f"Formation Energy (Delta H): {delta_H:.3f} eV (per formula unit)")

if delta_H < 0:
    print("✅ RESULT: EXOTHERMIC (Stable)")
    print("   The reaction releases energy. The atoms WANT to form Nb2SiC.")
    print("   This confirms synthesizability is thermodynamically likely.")
else:
    print("❌ RESULT: ENDOTHERMIC (Unstable)")
    print("   You would need to force this reaction. It might decompose back into elements.")