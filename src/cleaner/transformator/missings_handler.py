import pandas as pd
from typing import Dict, Any

class MissingValuesHandler:
    @staticmethod
    def apply_logical_defaults(df:pd.DataFrame, rules: Dict[str,Any]) -> pd.DataFrame:
        df=df.copy()
        for c, default_val in rules.items():
            if c in df.columns:
                df[c] = df[c].fillna(default_val)
                if isinstance(default_val, bool):
                    df[c] = df[c].astype(bool)
        return df
    
    @staticmethod
    def apply_placeholder(df:pd.DataFrame, placeholders: Dict[str,str]) -> pd.DataFrame:
        df=df.copy()
        for c, placeholder in placeholders.items():
            if c in df.columns:
                df[c] = df[c].fillna(placeholder)
        return df