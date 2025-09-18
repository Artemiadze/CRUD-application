from pydantic import BaseModel, ConfigDict, field_validator
from datetime import date
from typing import Optional
from uuid import UUID

from src.utils.validators import validate_birth_date, validate_receipt_date, validate_passport_series, validate_passport_number, validate_user_id
from src.domain.users import UserId

class PassportBase(BaseModel):
    model_config = ConfigDict(from_attributes=True) # to read data from ORM models

    birth_date: date
    passport_series: str
    passport_number: str 
    receipt_date: date
    user_id: UserId

    _validate_birth_date = field_validator("birth_date", mode="before")(validate_birth_date)
    _validate_receipt_date = field_validator("receipt_date", mode="before")(validate_receipt_date)
    _validate_passport_series = field_validator("passport_series", mode="before")(validate_passport_series)
    _validate_passport_number = field_validator("passport_number", mode="before")(validate_passport_number)
    _validate_user_id = field_validator("user_id", mode="before")(validate_user_id)
    
class PassportCreate(PassportBase):
    pass

class PassportUpdate(BaseModel):
    birth_date: Optional[date] = None
    passport_number: Optional[str] = None
    passport_series: Optional[str] = None
    receipt_date: Optional[date] = None
    user_id: Optional[UserId] = None

    _validate_birth_date = field_validator("birth_date", mode="before")(validate_birth_date)
    _validate_receipt_date = field_validator("receipt_date", mode="before")(validate_receipt_date)
    _validate_passport_series = field_validator("passport_series", mode="before")(validate_passport_series)
    _validate_passport_number = field_validator("passport_number", mode="before")(validate_passport_number)
    _validate_user_id = field_validator("user_id", mode="before")(validate_user_id)
    
class PassportOut(PassportBase):
    id: UUID