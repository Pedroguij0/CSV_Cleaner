from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Any


class CurrencyLocale(str, Enum):
    BRAZIL = "BRL"
    US = "USD"
    EUROPE = "EUR"

class DataLocale(str,Enum):
    BRAZIL = "DD/MM/YYYY"
    EUROPE = "DD/MM/YYYY"
    US = "MM/DD/YYYY"

    @property
    def is_day_firts(self) -> bool:
        return self in(DataLocale.BRAZIL, DataLocale.EUROPE)

@dataclass(frozen=True)
class PipelineConfig:
    text_columns: List[str] = field(default_factory=lambda: ["client_name", "city", "category"])
    email_columns: List[str] = field(default_factory= lambda: ["client_email"])
    currency_columns: List[str] = field(default_factory=lambda: ["unity_price"])
    date_columns: List[str] = field(default_factory=lambda: ["bought_date"])
    logical_defaults: Dict[str, Any] = field(default_factory= lambda: {"discount":0.0, "receive_newsletter":False})
    placeholder: Dict[str,Any] = field(default_factory=lambda: {"category":"NOT INFORMED", "city":"NOT INFORMED", "client_email":"NOT INFORMED"})
    currency_locale: CurrencyLocale = CurrencyLocale.BRAZIL
    date_locale: DataLocale=DataLocale.BRAZIL