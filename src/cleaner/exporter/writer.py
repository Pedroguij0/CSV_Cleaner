from pathlib import Path
import pandas as pd

class DataExporter:
    @staticmethod
    def export(df:pd.DataFrame, output_path:Path, base_name:str = "cleaned_data") -> tuple[Path, Path]:
        output_path.mkdir(parents=True, exist_ok=True)
        csv_path = output_path/f"{base_name}.csv"
        xlsx_path = output_path/f"{base_name}.xlsx"

        df.to_csv(csv_path, index=False, encoding="utf-8")
        df.to_excel(xlsx_path, index=False, engine="openpyxl")
        return csv_path, xlsx_path