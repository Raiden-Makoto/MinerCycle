# Some coompounds in our downloaded dataset are theoretical
# they may contain radioactive elements (e.g Plutonium)
# and/or noble gases

from pymatgen.core import Element, Composition
import pandas as pd

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

df = pd.read_csv('materials.csv')
print(f"Loaded {len(df)} materials from original dataset.")
df['invalid_elements'] = df['formula'].apply(is_invalid)
df_clean = df[df['invalid_elements'] == False].drop(columns=['invalid_elements'])
df_clean.to_csv('materials_cleaned.csv', index=False)
print(f"Saved {len(df_clean)} cleaned materials.")