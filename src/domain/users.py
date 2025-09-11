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