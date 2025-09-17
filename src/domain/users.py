from dataclasses import dataclass
from datetime import date
from typing import NewType
from uuid import UUID

from src.domain.passport import Passport


UserId = NewType("UserId", UUID)

@dataclass
class User:
    id: UserId
    first_name: str
    last_name: str
    patronymic: str | None
    phone_number: str
    passports: list[Passport] | None = None