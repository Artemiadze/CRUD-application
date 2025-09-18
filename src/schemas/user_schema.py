from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from uuid import UUID
import re

class UsersBase(BaseModel):
    model_config = ConfigDict(from_attributes=True) # to read data from ORM models

    first_name: str
    last_name: str
    patronymic: str | None
    phone_number: str

    @field_validator('first_name', mode='before')
    def validate_first_name(cls, value):
        if value is None or not value.strip():
            raise ValueError('first_name cannot be empty or None')
        
        if not isinstance(value, str):
            raise ValueError('first_name must be a string')
        
        if not re.match(r'^[a-zA-Zа-яА-Я]*$', value):
            raise ValueError('first_name must contain only alphabetic characters')
        
        return value.title()
    
    @field_validator('last_name', mode='before')
    def validate_last_name(cls, value):
        if value is None or not value.strip():
            raise ValueError('last_name cannot be empty or None')
        
        if not isinstance(value, str):
            raise ValueError('last_name must be a string')
        
        if not re.match(r'^[a-zA-Zа-яА-Я]*$', value):
            raise ValueError('last_name must contain only alphabetic characters')
        
        return value.title()
    
    @field_validator('patronymic', mode='before')
    def validate_patronymic(cls, value):      
        if not isinstance(value, str):
            raise ValueError('patronymic must be a string')
        
        if not re.match(r'^[a-zA-Zа-яА-Я]*$', value):
            raise ValueError('patronymic must contain only alphabetic characters')
        
        return value.title()
    
    @field_validator('phone_number', mode='before')
    def validate_phone_number(cls, value):
        if value is None or not value.strip():
            raise ValueError('Phone number cannot be empty or None')
        
        if not isinstance(value, str):
            raise ValueError('Phone number must be a string')
        
        # Remove all non-digit characters
        digits = re.sub(r'[^0-9]', '', value)
        if len(digits) != 11:
            raise ValueError('Phone number must contain exactly 11 digits')
        
        if not re.match(r'^[0-9\+\-]*$', value):
            raise ValueError('Phone number can only contain digits, "+", and "-"')
        
        return value

class UsersCreate(UsersBase):
    pass

class UsersUpdate(UsersBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    phone_number: Optional[str] = None

    
    @field_validator('first_name', mode='before')
    def validate_first_name(cls, value):
        if value is None or not value.strip():
            return value  # Skip it if the field is not provided.
        
        if not isinstance(value, str):
            raise ValueError('first_name must be a string')
        
        if not re.match(r'^[a-zA-Zа-яА-Я]*$', value):
            raise ValueError('first_name must contain only alphabetic characters')
        
        return value.title()
    
    @field_validator('last_name', mode='before')
    def validate_last_name(cls, value):
        if value is None or not value.strip():
            return value  # Skip it if the field is not provided.
        
        if not isinstance(value, str):
            raise ValueError('last_name must be a string')
        
        if not re.match(r'^[a-zA-Zа-яА-Я]*$', value):
            raise ValueError('last_name must contain only alphabetic characters')
        
        return value.title()
    
    @field_validator('patronymic', mode='before')
    def validate_patronymic(cls, value):
        if value is None or not value.strip():
            return value  # Skip it if the field is not provided.
          
        if not isinstance(value, str):
            raise ValueError('patronymic must be a string')
        
        if not re.match(r'^[a-zA-Zа-яА-Я]*$', value):
            raise ValueError('patronymic must contain only alphabetic characters')
        
        return value.title()

    @field_validator('phone_number', mode='before')
    def validate_phone_number(cls, value):
        if value is None:
            return value  # Skip it if the field is not provided.
        
        if not value.strip():
            raise ValueError('Phone number cannot be empty or None')
        
        if not isinstance(value, str):
            raise ValueError('Phone number must be a string')
        
        digits = re.sub(r'[^0-9]', '', value)
        if len(digits) != 11:
            raise ValueError('Phone number must contain exactly 11 digits')
        
        if not re.match(r'^[0-9\+\-]*$', value):
            raise ValueError('Phone number can only contain digits, "+", and "-"')
        return value

class UsersOut(UsersBase):
    id: UUID