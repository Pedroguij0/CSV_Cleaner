import pandas as pd
from typing import List

class StringCleaner:
    @staticmethod
    def format_title(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        df = df.copy()
        for c in columns:
            if c in df.columns:
                mask = df[c].notna()
                df.loc[mask,c] = (df.loc[mask,c].astype(str).str.strip().str.title())
        return df
    
    @staticmethod
    def format_email(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        df = df.copy()
        for c in columns:
            if c in df.columns:
                mask = df[c].notna()
                df.loc[mask,c] = (df.loc[mask, c].astype(str).str.strip().str.lower())
        return df