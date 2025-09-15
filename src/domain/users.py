from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class User:
    id: Optional[int]
    full_name: str
    phone_number: str
    birth_date: date
    passport: str