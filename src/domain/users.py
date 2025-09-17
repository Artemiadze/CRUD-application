from dataclasses import dataclass
from datetime import date
from typing import NewType
from uuid import UUID

UserId = NewType("UserId", UUID)

@dataclass
class User:
    id: UserId
    first_name: str
    last_name: str
    patronymic: str | None
    phone_number: str