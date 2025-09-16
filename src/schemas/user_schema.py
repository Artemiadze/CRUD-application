from pydantic import BaseModel, ConfigDict, field_validator
from datetime import date, datetime
from typing import Optional
import re

class UsersBase(BaseModel):
    model_config = ConfigDict(from_attributes=True) # to read data from ORM models

    first_name: str
    last_name: str
    patronymic: str | None
    phone_number: str
    birth_date: date
    passport_series: int
    passport_number: int

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
    
    @field_validator('birth_date', mode='before')
    def validate_birth_date(cls, value):
        if value is None or not value.strip():
            raise ValueError('Birth date cannot be None')
        
        # List of acceptable date formats
        date_formats = [
            '%Y-%m-%d',  # 2000-01-01
            '%d.%m.%Y',  # 01.01.2000
            '%d/%m/%Y',  # 01/01/2000
            '%d-%m-%Y',  # 01-01-2000
            '%Y.%m.%d',  # 2000.01.01
            '%Y/%m/%d',  # 2000/01/01
        ]
        
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError('Birth date cannot be empty')
            
            # Check for invalid characters
            if not re.match(r'^[\d\s.-/]+$', value):
                raise ValueError('Birth date contains invalid characters')
            
            # Try to parse the date using the acceptable formats
            parsed_date = None
            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(value, fmt).date()
                    break
                except ValueError:
                    # continue trying other formats
                    continue
            
            if parsed_date is None:
                raise ValueError('Birth date must be in one of the formats: YYYY-MM-DD, DD.MM.YYYY, DD/MM/YYYY, DD-MM-YYYY, YYYY.MM.DD, YYYY/MM/DD')
            
            value = parsed_date
        
        elif not isinstance(value, date):
            raise ValueError('Birth date must be a valid date object')
        
        # Is date in the future?
        if value > date.today():
            raise ValueError('Birth date cannot be in the future')
        
        return value
    
    @field_validator('passport_series', mode='before')
    def validate_passport_series(cls, value):
        if value is None or not value.strip():
            raise ValueError('passport_series cannot be empty or None')
        
        # Removing leading and trailing whitespace
        value = value.strip()

        if not isinstance(value, str):
            raise ValueError('passport_series must be a string')
        
        if len(value) != 4:
            raise ValueError('passport_series must be exactly 4 characters long with whitespace')
        
        if not re.match(r'^[1-9][0-9]{3}$', value):
            raise ValueError('passport_series must contain only digits and cannot start with zero')

        if not re.match(r'^[0-9]+$', value):
            raise ValueError('passport_series must contain only alphanumeric characters and spaces')
        
        return value.upper()
    
    @field_validator('passport_number', mode='before')
    def validate_passport_number(cls, value):
        if value is None or not value.strip():
            raise ValueError('passport_number cannot be empty or None')
        
        # Removing leading and trailing whitespace
        value = value.strip()
        
        if not isinstance(value, str):
            raise ValueError('passport_number must be a string')
        
        if len(value) != 6:
            raise ValueError('passport_number must be exactly 6 characters long')
        
        if not re.match(r'^[0-9]{6}$', value):
            raise ValueError('passport_number must contain only digits')
        
        return value

class UsersCreate(UsersBase):
    @field_validator("birth_date")
    def check_age(cls, v: date):
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 14:
            raise ValueError("User must be at least 14 years old")
        return v

class UsersUpdate(UsersBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    phone_number: Optional[str] = None
    birth_date: Optional[date] = None
    passport_number: Optional[str] = None
    passport_series: Optional[str] = None

    
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

    @field_validator('birth_date', mode='before')
    def validate_birth_date(cls, value):
        if value is None or value.strip():
            return value  # Skip it if the field is not provided.
        
        # List of acceptable date formats
        date_formats = [
            '%Y-%m-%d',  # 2000-01-01
            '%d.%m.%Y',  # 01.01.2000
            '%d/%m/%Y',  # 01/01/2000
            '%d-%m-%Y',  # 01-01-2000
            '%Y.%m.%d',  # 2000.01.01
            '%Y/%m/%d',  # 2000/01/01
        ]
        
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError('Birth date cannot be empty')
            
            # Check for invalid characters
            if not re.match(r'^[\d\s.-/]+$', value):
                raise ValueError('Birth date contains invalid characters')
            
            # Try to parse the date using the acceptable formats
            parsed_date = None
            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(value, fmt).date()
                    break
                except ValueError:
                    # continue trying other formats
                    continue
            
            if parsed_date is None:
                raise ValueError('Birth date must be in one of the formats: YYYY-MM-DD, DD.MM.YYYY, DD/MM/YYYY, DD-MM-YYYY, YYYY.MM.DD, YYYY/MM/DD')
            
            value = parsed_date
        
        elif not isinstance(value, date):
            raise ValueError('Birth date must be a valid date object')
        
        # Is date in the future?
        if value > date.today():
            raise ValueError('Birth date cannot be in the future')
        
        return value
    
    @field_validator('passport_series', mode='before')
    def validate_passport_series(cls, value):
        if value is None or value.strip():
            return value
        
        # Removing leading and trailing whitespace
        value = value.strip()

        if not isinstance(value, str):
            raise ValueError('passport_series must be a string')
        
        if len(value) != 4:
            raise ValueError('passport_series must be exactly 4 characters long with whitespace')
        
        if not re.match(r'^[1-9][0-9]{3}$', value):
            raise ValueError('passport_series must contain only digits and cannot start with zero')

        if not re.match(r'^[0-9]+$', value):
            raise ValueError('passport_series must contain only alphanumeric characters and spaces')
        
        return value.upper()
    
    @field_validator('passport_number', mode='before')
    def validate_passport_number(cls, value):
        if value is None or value.strip():
            return value  # Skip it if the field is not provided.
        
        # Removing leading and trailing whitespace
        value = value.strip()
        
        if not isinstance(value, str):
            raise ValueError('passport_number must be a string')
        
        if len(value) != 6:
            raise ValueError('passport_number must be exactly 6 characters long')
        
        if not re.match(r'^[0-9]{6}$', value):
            raise ValueError('passport_number must contain only digits')
        
        return value

class UsersOut(UsersBase):
    id: int