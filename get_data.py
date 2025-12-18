import os
from dotenv import load_dotenv
from mp_api.client import MPRester #type: ignore
from pymatgen.core import Composition
import pandas as pd

# Some compounds in our downloaded dataset are theoretical
# they may contain radioactive elements (e.g Plutonium)
# and/or noble gases
invalid_elements = ["Tc", "Pm", "Po", "At", "Rn", "Fr", "Ra", "Ac", "He", "Ne", "Ar", "Kr", "Xe"]

def is_invalid(formula_str):
    try:
        # Create a Pymatgen Composition object from the string
        comp = Composition(formula_str)
        # Check every element in the formula
        for element in comp.elements:
            if element.symbol in invalid_elements:
                return True
        return False
    except:
        # If the formula is garbage/unparseable, mark it as "bad"
        return True

load_dotenv()
api_key = os.getenv("MATERIALS_API_KEY")

with MPRester(api_key) as mpr:
    print("Querying for materials with calculated elastic properties...")
    docs = mpr.materials.summary.search(
        has_props=['elasticity'],
        fields=["material_id", "formula_pretty", "density", "bulk_modulus", "shear_modulus", "is_stable"]
    )
    print(f"Found {len(docs)} materials.")

data = {
    'material_id' : [],
    'formula' : [],
    'density' : [],
    'bulk_modulus' : [],
    'shear_modulus' : [],
    'is_stable' : []
}

for mat in docs:
    data["bulk_modulus"].append(mat.bulk_modulus['vrh'] if mat.bulk_modulus else None)
    data["density"].append(mat.density)
    data["formula"].append(mat.formula_pretty)
    data["is_stable"].append(mat.is_stable)
    data["shear_modulus"].append(mat.shear_modulus['vrh'] if mat.shear_modulus else None)
    data["material_id"].append(mat.material_id)

df = pd.DataFrame(data)
df = df.dropna()
print(f"Loaded {len(df)} materials from original dataset.")

# Clean invalid elements
df['invalid_elements'] = df['formula'].apply(is_invalid)
df_clean = df[df['invalid_elements'] == False].drop(columns=['invalid_elements'])
df_clean.to_csv('materials_cleaned.csv', index=False)
print(f"Saved {len(df_clean)} cleaned materials.")