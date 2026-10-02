from pathlib import Path
import pandas as pd
from cleaner.core.exceptions import ReaderException

class DataLoader:
    @staticmethod
    def load(file_path: Path) -> pd.DataFrame:
        if not file_path or not file_path.is_file():
            raise ReaderException(f"Cannot read the file in: {file_path}")
        suffix = file_path.suffix.lower()
        try:
            if suffix == ".csv":
                return pd.read_csv(file_path, sep=None, engine="python", encoding="utf-8")
            elif suffix in[".xlsx", ".xls"]:
                return pd.read_excel(file_path)
            else:
                raise ReaderException(f"Archive Type [{suffix}] not supported")
        except Exception as e:
            raise ReaderException(f"Reading Error in {file_path}: {e}") from e
        