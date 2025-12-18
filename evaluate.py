import joblib
import traceback
import itertools
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from matminer.featurizers.conversions import StrToComposition #type: ignore
from matminer.featurizers.composition import ElementProperty #type: ignore

if __name__ == '__main__':
    filename = 'regressor.joblib'
    try: 
        model = joblib.load(filename)
        print("Model loaded successfully")
    except Exception as e:
        print("An exception occurred.")
        traceback.print_exc()
        model = None

    # MAX Candidates (M = Transition Metal, A = Group 13/14, X = Carbon/Nitrogen)
    M_list = ['Ti', 'V', 'Cr', 'Zr', 'Nb', 'Mo', 'Hf', 'Ta', 'W']
    A_list = ['Al', 'Si', 'P', 'S', 'Ga', 'Ge', 'In', 'Sn']
    X_list = ['C', 'N']

    print("Generating MAX Composites.")
    candidates = [f"{m}2{a}{x}" for m, a, x in itertools.product(M_list, A_list, X_list)]
    print(f"Generated {len(candidates)} candidates.")

    ep_feat = ElementProperty.from_preset(preset_name='magpie')

    df_candidates = pd.DataFrame({'formula': candidates})
    df_candidates = StrToComposition().featurize_dataframe(df_candidates, "formula")
    df_candidates = ep_feat.featurize_dataframe(df_candidates, col_id="composition")

    X_cand = df_candidates.drop(columns=['formula', 'composition'], errors='ignore')

    print("Predicting properties...")
    predictions = model.predict(X_cand)
    print("Predictions completed successfully.")

    df_candidates['pred_bulk_modulus'] = predictions[:, 0]
    df_candidates['pred_density'] = predictions[:, 1]

    # Calculate "Specific Stiffness" (Stiffness / Density)
    df_candidates['specific_stiffness'] = df_candidates['pred_bulk_modulus'] / df_candidates['pred_density']
    top_candidates = df_candidates.sort_values('specific_stiffness', ascending=False).head(10)

    print("----------------------------------------------------------")
    print("TOP 6 DISCOVERED MATERIALS (Ranked by Specific Stiffness)")
    print("----------------------------------------------------------")
    output_cols = ['formula', 'pred_bulk_modulus', 'pred_density', 'specific_stiffness']
    print(top_candidates[output_cols].to_string(index=False, float_format="%.2f"))

    df_candidates.to_csv(
        'candidates.csv',
        columns=['formula', 'pred_bulk_modulus', 'pred_density']
    )