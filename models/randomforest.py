import os
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

from matminer.featurizers.conversions import StrToComposition #type: ignore
from matminer.featurizers.composition import ElementProperty #type: ignore

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor

import joblib

if __name__ == '__main__':
    # Get paths relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_path = os.path.join(project_root, 'data', 'materials_cleaned.csv')
    
    data = pd.read_csv(data_path)
    target_properties = ['bulk_modulus', 'density']

    y_data = data[target_properties]
    y_stability = data['is_stable'].astype(int)

    # calculate X data via featurizers
    print("Featurizing Dataset (this may take several minutes)...")
    df = StrToComposition().featurize_dataframe(data, 'formula')
    ep_feat = ElementProperty.from_preset(preset_name='magpie')
    df_featurized = ep_feat.featurize_dataframe(df, col_id='composition')

    cols_to_drop = target_properties + ['material_id', 'formula', 'shear_modulus', 'is_stable', 'composition']
    X_features = df_featurized.drop(columns=cols_to_drop, errors='ignore')

    print(f"Training on {X_features.shape[0]} materials with {X_features.shape[1]} features each.")

    model = MultiOutputRegressor(
        RandomForestRegressor(
            n_estimators=100,
            random_state=67
        )
    )
    model.fit(X_features, y_data)
    print("Model trained successfully!")
    regressor_path = os.path.join(script_dir, 'regressor.joblib')
    joblib.dump(model, regressor_path)
    print(f"Model saved to \"{regressor_path}\"")
    print()
    
    print("Training Stability Predictor.")
    clf = RandomForestClassifier(n_estimators=100, random_state=67)
    clf.fit(X_features, y_stability)
    print("Trained Stability Predictor.")
    stability_path = os.path.join(script_dir, 'stability.joblib')
    joblib.dump(clf, stability_path)
    print(f"Model saved to \"{stability_path}\"")
