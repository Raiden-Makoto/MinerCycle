import os
from dotenv import load_dotenv
from mp_api.client import MPRester #type: ignore

import pandas as pd

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
df.dropna()
df.to_csv('materials.csv', index=False)