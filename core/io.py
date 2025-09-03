# core/io.py
import yaml, pandas as pd

def load_catalog(path): return yaml.safe_load(open(path))
def load_metrics(path): 
    df = pd.read_csv(path)
    df['ts'] = pd.to_datetime(df['ts'])
    return df.sort_values('ts')

def save_csv(df, path): df.to_csv(path, index=False)
