from dataclasses import dataclass
from datetime import date

from src.domain.identifiers  import UserId, PassportId

@dataclass
class Passport:
    id: PassportId
    birth_date: date
    passport_series: str
    passport_number: str 
    receipt_date: date
    user_id: UserId