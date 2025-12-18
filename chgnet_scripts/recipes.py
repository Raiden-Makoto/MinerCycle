from mp_api.client import MPRester
import numpy as np

import os
import re
from dotenv import load_dotenv

import warnings
warnings.filterwarnings('ignore')

load_dotenv()
api_key = os.getenv('MATERIALS_API_KEY')
targets = ["Ti2AlC", "Ti3SiC2", "Nb2AlC", "Nb4AlC3"]

literature_backup = {
    "Ti2AlC":  {"temp": 1400, "source": "Barsoum (1996)"},
    "Ti3SiC2": {"temp": 1450, "source": "El-Raghy (1999)"},
    "Nb2AlC":  {"temp": 1550, "source": "Salama (2002)"},
    "Nb4AlC3": {"temp": 1600, "source": "Hu (2007)"}
}

print(f"👨‍🍳 Extracting recipes for Nb2SiC family...")
print("-" * 50)

recipes = []

def extract_temp_from_text(text):
    # Regex to find patterns like "1400 C", "1400°C", "1400C"
    # We look for numbers between 800 and 2200 to avoid dates or other numbers
    matches = re.findall(r'(\d{3,4})\s?°?C', text)
    valid_temps = []
    for m in matches:
        t = float(m)
        if 800 < t < 2200:
            valid_temps.append(t)
    return valid_temps

# 2. THE SEARCH LOOP
with MPRester(api_key) as mpr:
    for formula in targets:
        found_via_api = False
        print(f"   🔎 Checking {formula}...", end="")
        
        try:
            # Get text data
            docs = mpr.synthesis.search(keywords=[formula])
            extracted_temps = []
            
            for doc in docs:
                # Look in the raw paragraph text if available
                text = getattr(doc, 'paragraph_string', "")
                if text:
                    extracted_temps.extend(extract_temp_from_text(text))
            
            if extracted_temps:
                avg_t = np.mean(extracted_temps)
                print(f" Found {len(extracted_temps)} temp mentions. Avg: {avg_t:.0f}°C")
                recipes.append({"cousin": formula, "temp": avg_t, "weight": 1.0})
                found_via_api = True
            else:
                print(" No temps in text.")
                
        except Exception as e:
            print(f" API Error ({str(e)})")

        # Fallback
        if not found_via_api:
            if formula in literature_backup:
                data = literature_backup[formula]
                print(f"      📚 Using Backup: {data['temp']}°C ({data['source']})")
                recipes.append({"cousin": formula, "temp": data['temp'], "weight": 2.0}) # Higher weight for verified manual data
            else:
                print("      ❌ No data.")

# 3. FINAL CALCULATION
if recipes:
    # Weighted Average
    total_weight = sum(r['weight'] for r in recipes)
    final_temp = sum(r['temp'] * r['weight'] for r in recipes) / total_weight
    
    # Niobium Bias (Ensure we respect the physics of Nb)
    if final_temp < 1500 and any("Nb" in r['cousin'] for r in recipes):
        print("\n   ⚠️ Adjustment: Detected Niobium content but low average temp.")
        print("   -> Bumping temp to match Nb2AlC baseline (1550°C).")
        final_temp = max(final_temp, 1550)

    print("\n" + "="*50)
    print("🧪 FINAL SYNTHESIS PROTOCOL: Nb2SiC")
    print("="*50)
    print(f"Predicted Temperature: {final_temp:.0f}°C")
    print("Method: Reactive Hot Pressing")
    print("Atmosphere: Inert (Argon)")
    print("-" * 50)
else:
    print("Failed to generate recipe.")