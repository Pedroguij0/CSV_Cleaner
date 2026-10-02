from dataclasses import dataclass
import pandas as pd
from typing import Dict,Any, List

@dataclass
class Anomaly:
    record_id: str
    anomaly_type: str
    details: str
    raw_value: Any
    message: str
    column: str

class DataAuditor:
    @staticmethod
    def run_audit(df:pd.DataFrame) -> List[Anomaly]:
        anomalies: List[Anomaly] = []
        if "unity_price" in df.columns:
            invalid_price = df[df["unity_price"]<0]
            for i, row in invalid_price.iterrows():
                record_id = str(row["transaction_id"]) if "transaction_id" in df.columns else f"Row {i}"
                anomalies.append(Anomaly(
                    record_id=str(record_id),
                    anomaly_type="Negative Price",
                    details=f"Price:{row['unity_price']}",
                    raw_value=row["unity_price"],
                    message="Price bellow zero. Please, enter a valid value.",
                    column="unity_price",
                    ))

        if "quantity" in df.columns:
            invalid_qty = df[df["quantity"]<=0]
            for i, row in invalid_qty.iterrows():
                record_id = str(row["transaction_id"]) if "transaction_id" in df.columns else f"Row {i}"
                anomalies.append(Anomaly(
                    record_id=str(record_id),
                    anomaly_type="Invalid Quantity",
                    details=f"Quantity: {row['quantity']}",
                    raw_value=row["quantity"],
                    message="Invalid Quantity. Please, enter a valid quantity.",
                    column="quantity"
                ))

        if "client_email" in df.columns:
            missing_email = df[(df["client_email"].isna()) | (df["client_email"] == "") | (df["client_email"]=="NOT INFORMED")]
            for i, row in missing_email.iterrows():
                record_id = str(row["transaction_id"]) if "transaction_id" in df.columns else f"Row {i}"
                anomalies.append(Anomaly(
                    record_id=str(record_id),
                    anomaly_type="Missing Email",
                    details=f"Missing Email of: {row.get("client_name", "NOT INFORMED")}",
                    raw_value=row["client_email"],
                    message="Missing or corrupted email. Please, enter a valid Email.",
                    column="client_email"
                ))

        if "bought_date" in df.columns:
            invalid_dates= df[df["bought_date"].isna()]
            for i, row in invalid_dates.iterrows():
                record_id = str(row["transaction_id"]) if "transaction_id" in df.columns else f"Row {i}"
                anomalies.append(Anomaly(
                    record_id=str(record_id),
                    anomaly_type="Invalid Date",
                    details=f"Cannot Parse the date: {row["bought_date"]}",
                    raw_value=row["bought_date"],
                    message="Missing or Invalid date. Please, enter a valid date",
                    column="bought_date"
                ))
            parsed_date = pd.to_datetime(df["bought_date"], errors="coerce") 
            today = pd.Timestamp.now().normalize()
            past_limit = pd.Timestamp("2007-01-01")
            future_dates = df[parsed_date>today]
            for i, row in future_dates.iterrows():
                record_id = str(row["transaction_id"]) if "transaction_id" in df.columns else f"Row {i}"
                anomalies.append(Anomaly(
                    record_id=str(record_id),
                    anomaly_type="Future Date",
                    details=f"Transacion date {row["bought_date"]} is in the future",
                    raw_value= row["bought_date"],
                    message= "The transacion date cannot be greater than today",
                    column="bought_date"
                ))
            outdated_date = df[parsed_date<past_limit]
            for i, row in outdated_date.iterrows():
                record_id = str(row["transaction_id"]) if "transaction_id" in df.columns else f"Row {i}"
                anomalies.append(Anomaly(
                    record_id=str(record_id),
                    anomaly_type="Outdated Date",
                    details=f"Transacion date '{row["bought_date"]}' is older than the setted limit '{past_limit.strftime('%Y-%m-%d')}'.",
                    raw_value=row["bought_date"],
                    message="The transacion date is older than system operational threshold.",
                    column="bought_date"
                ))
        return anomalies