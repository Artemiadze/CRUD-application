from dataclasses import dataclass
from datetime import date
from typing import Optional

class DomainValidationError(Exception):
    """Custom exception for domain validation errors."""
    pass

@dataclass
class User:
    id: Optional[int]
    full_name: str
    phone_number: str
    birth_date: date
    passport: str

    def validate_age(self):
        today = date.today()
        age = today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
        if age < 14:
            raise DomainValidationError("User must be at least 14 years old.")