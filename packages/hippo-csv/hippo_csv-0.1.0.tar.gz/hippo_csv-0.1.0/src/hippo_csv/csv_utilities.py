import pandas as pd
import os

def read_csv(filepath: str, encoding: str = "utf-8", errors: str = "replace") -> pd.DataFrame:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found {filepath}")
    
    try:
        df = pd.read_csv(filepath, encoding=encoding, on_bad_lines='skip', engine='python')
    except Exception as e:
        raise ValueError(f"Failed to read CSV: {e}")
    
    if df.empty:
        raise ValueError("CSV file is empty or unreadable.")
    
    return df
