from pydantic import BaseModel, ConfigDict, field_validator
from src.utils.validators import validate_first_name, validate_last_name, validate_patronymic, validate_phone_number
from typing import Optional
from datetime import date
from typing import Optional
from uuid import UUID

from src.schemas.passport_schema import PassportOut

class UsersBase(BaseModel):
    model_config = ConfigDict(from_attributes=True) # to read data from ORM models

    first_name: str
    last_name: str
    patronymic: str | None
    phone_number: str

    _validate_first_name = field_validator('first_name', mode='before')(validate_first_name)
    _validate_last_name = field_validator('last_name', mode='before')(validate_last_name)
    _validate_patronymic = field_validator('patronymic', mode='before')(validate_patronymic)
    _validate_phone_number = field_validator('phone_number', mode='before')(validate_phone_number)

class UsersCreate(UsersBase):
    pass

class UsersUpdate(UsersBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    phone_number: Optional[str] = None

    
    _validate_first_name = field_validator('first_name', mode='before')(validate_first_name)
    _validate_last_name = field_validator('last_name', mode='before')(validate_last_name)
    _validate_patronymic = field_validator('patronymic', mode='before')(validate_patronymic)
    _validate_phone_number = field_validator('phone_number', mode='before')(validate_phone_number)

class UsersOut(UsersBase):
    id: UUID
    first_name: str
    last_name: str
    patronymic: str | None
    phone_number: str
    passports: list[PassportOut] = []