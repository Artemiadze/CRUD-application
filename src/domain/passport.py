from dataclasses import dataclass
from datetime import date
from typing import NewType
from uuid import UUID

from src.domain.users import UserId

PassportID = NewType("PassportID", UUID)

@dataclass
class Passport:
    id: PassportID
    birth_date: date
    passport_series: str
    passport_number: str 
    receipt_date: date
    user_id: UserId