import pandas as pd
from typing import List
from cleaner.config import DataLocale
class DateNormalizer:
    @staticmethod
    def to_iso(df: pd.DataFrame, columns: List[str], locale: DataLocale = DataLocale.BRAZIL) -> pd.DataFrame:
        df = df.copy()
        for c in columns:
            if c in df.columns:
                date = pd.to_datetime(df[c], format = "mixed", errors="coerce", dayfirst=locale.is_day_firts)
                df[c]= date.dt.strftime("%Y-%m-%d")
        return df
