
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

class MissingValuePredictor:
    def __init__(self, df):
        self.df = df
        self.models = {}
        self.train_models()

    def train_models(self):
        ignore = ['Product', 'Market_ID']
        features = [col for col in self.df.columns if col not in ignore]

        for target in features:
            temp_df = self.df.dropna(subset=[target])  # Ensure target is not NaN
            X = temp_df.drop(columns=[target] + ignore)
            y = temp_df[target]

        # Keep only numeric features
            X = X.select_dtypes(include=['int64', 'float64'])

            if not X.empty and y.dtype in ['int64', 'float64']:
                try:
                    model = RandomForestRegressor(n_estimators=100)
                    model.fit(X, y)
                    self.models[target] = model
                except Exception as e:
                    print(f"⚠️ Skipping model for {target}: {e}")

    def fill_missing(self, row):
        filled = row.copy()
        base_features = {k: v for k, v in row.items() if isinstance(v, (int, float))}

        for param, model in self.models.items():
            if param not in filled or pd.isna(filled[param]):
                try:
                    df_input = pd.DataFrame([base_features]).select_dtypes(include=['int64', 'float64'])

                    filled[param] = model.predict(df_input)[0]
                except Exception as e:
                    print(f"⚠️ Could not predict {param}: {e}")
        return filled
