import pandas as pd
import itertools

from matminer.featurizers.conversions import StrToComposition #type: ignore
from matminer.featurizers.composition import ElementProperty #type: ignore

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor

data = pd.read_csv('materials_cleaned.csv')
target_properties = ['bulk_modulus', 'density']

y_data = data[target_properties]

# calculate X data via featurizers