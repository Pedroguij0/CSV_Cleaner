import pandas as pd

class Deduplicator:
    @staticmethod
    def deduplicate(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
        initial_count = len(df)
        df_cleaned = df.drop_duplicates(keep="first").copy()
        removed = initial_count - len(df_cleaned)
        return df_cleaned, removed