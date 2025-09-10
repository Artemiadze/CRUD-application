from pydantic import BaseModel, ConfigDict, field_validator
from datetime import date, datetime
from typing import Optional
import re

class UsersBase(BaseModel):
    model_config = ConfigDict(from_attributes=True) # to read data from ORM models
    full_name: str
    phone_number: str
    birth_date: date
    passport: str

    @field_validator('full_name', mode='before')
    def validate_full_name(cls, value):
        if value is None or not value.strip():
            raise ValueError('Name cannot be empty or None')
        
        if not isinstance(value, str):
            raise ValueError('Name must be a string')
        
        if not re.match(r'^[a-zA-Zа-яА-Я\s]*$', value):
            raise ValueError('Name must contain only alphabetic characters and spaces')
        
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

    @field_validator('birth_date', mode='before')
    def validate_birth_date(cls, value):
        if value is None:
            raise ValueError('Birth date cannot be None')
        
        # Converting a string or other type to a date
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Birth date must be in YYYY-MM-DD format')
        elif not isinstance(value, date):
            raise ValueError('Birth date must be a valid date')
        
        # Is date in the future?
        if value > date.today():
            raise ValueError('Birth date cannot be in the future')
        
        return value

    @field_validator('passport', mode='before')
    def validate_passport(cls, value):
        if value is None or not value.strip():
            raise ValueError('Passport cannot be empty or None')
        
        if not isinstance(value, str):
            raise ValueError('Passport must be a string')
        
        if len(value) != 11:
            raise ValueError('Passport must be exactly 11 characters long with whitespace')
        
        alphanumeric = re.sub(r'[^0-9]', '', value)
        if len(alphanumeric) != 10:
            raise ValueError('Passport must contain exactly 10 integer number')
        if not re.match(r'^[0-9\s]+$', value):
            raise ValueError('Passport must contain only alphanumeric characters and spaces')
        
        return value.upper()

class UsersCreate(UsersBase):
    # ToDO
    pass

class UsersUpdate(UsersBase):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    birth_date: Optional[date] = None
    passport: Optional[str] = None

    @field_validator('full_name', mode='before')
    def validate_full_name(cls, value):
        if value is None:
            return value  # Skip it if the field is not provided.
        
        if not value.strip():
            raise ValueError('Name cannot be empty or None')
        
        if not isinstance(value, str):
            raise ValueError('Name must be a string')
        
        if not re.match(r'^[a-zA-Zа-яА-Я\s]*$', value):
            raise ValueError('Name must contain only alphabetic characters and spaces')
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

    @field_validator('birth_date', mode='before')
    def validate_birth_date(cls, value):
        if value is None:
            return value  # Skip it if the field is not provided.
        
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Birth date must be in YYYY-MM-DD format')
        elif not isinstance(value, date):
            raise ValueError('Birth date must be a valid date')
        
        if value > date.today():
            raise ValueError('Birth date cannot be in the future')
        return value

    @field_validator('passport', mode='before')
    def validate_passport(cls, value):
        if value is None:
            return value  # Skip it if the field is not provided.
        
        if not value.strip():
            raise ValueError('Passport cannot be empty or None')
        
        if not isinstance(value, str):
            raise ValueError('Passport must be a string')
        
        if len(value) != 11:
            raise ValueError('Passport must be exactly 11 characters long with whitespace')
        
        alphanumeric = re.sub(r'[^0-9]', '', value)
        if len(alphanumeric) != 10:
            raise ValueError('Passport must contain exactly 10 integer number')
        
        if not re.match(r'^[0-9\s]+$', value):
            raise ValueError('Passport must contain only alphanumeric characters and spaces')
        return value.upper()

class UsersOut(UsersBase):
    id: int