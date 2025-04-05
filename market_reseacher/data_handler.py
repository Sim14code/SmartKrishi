import pandas as pd

class DataHandler:
    def __init__(self, path):
        self.df = pd.read_csv(path)

    def get_product_data(self, product_name):
        row = self.df[self.df['Product'].str.lower() == product_name.lower()]
        return row.iloc[0].to_dict() if not row.empty else {}
    
    def get_training_data(self):
        return self.df.dropna()
