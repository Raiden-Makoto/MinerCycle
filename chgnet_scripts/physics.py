import os

from ase.optimize import BFGS
from chgnet.model.dynamics import MolecularDynamics
from chgnet.model.dynamics import StructOptimizer
from chgnet.model.model import CHGNet
from dotenv import load_dotenv
from mp_api.client import MPRester
from pymatgen.core import Structure
from pymatgen.io.ase import AseAtomsAdaptor

import warnings
warnings.filterwarnings('ignore')

load_dotenv()
api_key = os.getenv('MATERIALS_API_KEY')

print("Initializaing CHGNet...")
chgnet = CHGNet.load()

print("Performing Alchemy...")
with MPRester(api_key) as mpr:
    print("\tSearching for stable Ti2AlC template...")
    docs = mpr.materials.summary.search(
        formula="Ti2AlC", 
        is_stable=True, 
        fields=["structure", "material_id"]
    )
    if not docs:
        raise ValueError("Could not find Ti2AlC in database!")
        
    structure = docs[0].structure
    print(f"\tFound template: {docs[0].material_id}")

print(f"Original Structure: {structure.formula}")
structure.replace_species({"Ti": "Nb", "Al": "Si"})
print(f"Transmuted Structure: {structure.formula}")

print("\nStarting Geometric Relaxation...")
prediction_pre = chgnet.predict_structure(structure)
e_pre = prediction_pre['e']
print(f"\tEnergy before relaxation: {e_pre:.3f} eV/atom")

relaxer = StructOptimizer(model=chgnet, optimizer_class=BFGS)
result = relaxer.relax(structure, verbose=True)
final_structure = result['final_structure']
e_post = result['trajectory'].energies[-1] / len(structure)

print(f"DONE! Final Energy: {e_post:.3f} eV/atom")
print(f"Energy Drop: {e_pre - e_post:.3f} eV (This represents stabilization)")

vol_start = structure.volume
vol_end = final_structure.volume
vol_change = ((vol_end - vol_start) / vol_start) * 100

print(f"Volume Change: {vol_change:.2f}%")

if abs(vol_change) < 10:
    print("✅ RESULT: Structure is STABLE! (It held its shape)")
    final_structure.to(filename="../figures/Nb2SiC_relaxed.cif")
    print("\tSaved structure to 'Nb2SiC_relaxed.cif'. You can view this in VESTA.")
else:
    print("❌ RESULT: Structure collapsed or expanded too much. Likely unstable.")
