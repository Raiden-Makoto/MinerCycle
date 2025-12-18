from mp_api.client import MPRester
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("MATERIALS_API_KEY")
target_formula = "Hf2GaN"

print(f"🕵️‍♂️ Investigating {target_formula}...")

with MPRester(api_key) as mpr:
    # 1. Search for the material
    docs = mpr.materials.summary.search(
        formula=target_formula, 
        fields=["material_id", "formula_pretty", "is_stable", "energy_above_hull", "formation_energy_per_atom"]
    )

print("\n--- INVESTIGATION REPORT ---")
if len(docs) == 0:
    print(f"🎉 RESULT: {target_formula} is NOT in the database!")
    print("This is a POTENTIAL NOVEL DISCOVERY.")
    print("Your ML model has proposed a material that (likely) hasn't been characterized yet.")
else:
    print(f"RESULT: {target_formula} ALREADY EXISTS ({len(docs)} entries found).")
    best_doc = docs[0] # Usually the most stable one is first
    print(f"Is it Stable? {best_doc.is_stable}")
    print(f"Energy Above Hull: {best_doc.energy_above_hull:.3f} eV/atom")
    
    if best_doc.is_stable:
        print("Verdict: You REDISCOVERED a known stable material. (Still a win for model accuracy!)")
    else:
        print("Verdict: It exists but is UNSTABLE. Your model was optimistic (77%), but nature says 'No'.")
