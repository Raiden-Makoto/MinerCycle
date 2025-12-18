import pandas as pd
import warnings

warnings.filterwarnings('ignore')

from matminer.featurizers.conversions import StrToComposition #type: ignore
from matminer.featurizers.composition import ElementProperty #type: ignore

from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor

import joblib

if __name__ == '__main__':
    data = pd.read_csv('materials_cleaned.csv')
    target_properties = ['bulk_modulus', 'density']

    y_data = data[target_properties]

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
    joblib.dump(model, 'regressor.joblib')
    print("Model saved to \"regressor.joblib\"")