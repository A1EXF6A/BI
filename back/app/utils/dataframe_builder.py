import pandas as pd

def build_dataframe(data):
    return pd.json_normalize(data)