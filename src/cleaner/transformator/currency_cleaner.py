import pandas as pd
from typing import List
from cleaner.config import CurrencyLocale

class CurrencyCleaner:
    @staticmethod
    def to_float(df: pd.DataFrame,
    columns: List[str],
    locale: CurrencyLocale = CurrencyLocale.BRAZIL) -> pd.DataFrame:
        df = df.copy()
        for c in columns:
            if c in df.columns:
                mask = df[c].notna()
                cleaned_str = (df.loc[mask,c].astype(str).str.replace(r"[R\$€\s]", "", regex=True))
                if locale in (CurrencyLocale.BRAZIL, CurrencyLocale.EUROPE):
                    has_comma = cleaned_str.str.contains(",")
                    cleaned_str = cleaned_str.where(~has_comma, cleaned_str.str.replace(".", "",regex=False)
                    .str.replace(",", ".", regex=False))
                elif locale in (CurrencyLocale.US):
                    cleaned_str = cleaned_str.str.replace(",","",regex=False)
                df.loc[mask,c] = pd.to_numeric(cleaned_str, errors="coerce")
                df[c] = df[c].astype(float)
        return df
