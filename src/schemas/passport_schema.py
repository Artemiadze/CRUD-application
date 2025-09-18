from pydantic import BaseModel, ConfigDict, field_validator
from datetime import date, datetime
from typing import Optional
from uuid import UUID

from src.domain.users import UserId
import re

class PassportBase(BaseModel):
    model_config = ConfigDict(from_attributes=True) # to read data from ORM models

    birth_date: date
    passport_series: str
    passport_number: str 
    receipt_date: date
    user_id: UserId

    @field_validator('birth_date', mode='before')
    def validate_birth_date(cls, value):
        if value is None:
            raise ValueError('Birth date cannot be None')

        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError('Birth date cannot be empty')

            # Check for invalid characters
            if not re.fullmatch(r'[\d.\-\/ ]+', value):
                raise ValueError('Birth date contains invalid characters')

            # Formats to try parsing the date
            date_formats = [
                '%Y-%m-%d',  # 2000-01-01
                '%d.%m.%Y',  # 01.01.2000
                '%d/%m/%Y',  # 01/01/2000
                '%d-%m-%Y',  # 01-01-2000
                '%Y.%m.%d',  # 2000.01.01
                '%Y/%m/%d',  # 2000/01/01
            ]

            for fmt in date_formats:
                try:
                    parsed = datetime.strptime(value, fmt).date()
                    if parsed > date.today():
                        raise ValueError('Birth date cannot be in the future')
                    return parsed
                except ValueError:
                    continue

            raise ValueError(
                'Birth date must be in one of the formats: '
                'YYYY-MM-DD, DD.MM.YYYY, DD/MM/YYYY, DD-MM-YYYY, YYYY.MM.DD, YYYY/MM/DD'
            )

        raise ValueError('Birth date must be a valid date or string')
    
    @field_validator('passport_series', mode='before')
    def validate_passport_series(cls, value):
        if value is None:
            raise ValueError('passport_series cannot be empty or None')
        
        # Removing leading and trailing whitespace
        value = str(value).strip()

        if not isinstance(value, str):
            raise ValueError('passport_series must be a string')
        
        if len(value) != 4:
            raise ValueError('passport_series must be exactly 4 characters long with whitespace')
        
        if not re.match(r'^[1-9][0-9]{3}$', value):
            raise ValueError('passport_series must contain only digits and cannot start with zero')
        
        return value.upper()
    
    @field_validator('passport_number', mode='before')
    def validate_passport_number(cls, value):
        if value is None:
            raise ValueError('passport_number cannot be empty or None')
        
        # Removing leading and trailing whitespace
        value = str(value).strip()
        
        if not isinstance(value, str):
            raise ValueError('passport_number must be a string')
        
        if len(value) != 6:
            raise ValueError('passport_number must be exactly 6 characters long')
        
        if not re.match(r'^[0-9]{6}$', value):
            raise ValueError('passport_number must contain only digits')
        
        return value
    
    @field_validator('receipt_date', mode='before')
    def validate_receipt_date(cls, value):
        if value is None:
            raise ValueError('Date receipt cannot be None')

        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError('Date receipt cannot be empty')

            # Check for invalid characters
            if not re.fullmatch(r'[\d.\-\/ ]+', value):
                raise ValueError('Date receipt contains invalid characters')

            # Formats to try parsing the date
            date_formats = [
                '%Y-%m-%d',  # 2000-01-01
                '%d.%m.%Y',  # 01.01.2000
                '%d/%m/%Y',  # 01/01/2000
                '%d-%m-%Y',  # 01-01-2000
                '%Y.%m.%d',  # 2000.01.01
                '%Y/%m/%d',  # 2000/01/01
            ]

            for fmt in date_formats:
                try:
                    parsed = datetime.strptime(value, fmt).date()
                    return parsed
                except ValueError:
                    continue

            raise ValueError(
                'Date receipt must be in one of the formats: '
                'YYYY-MM-DD, DD.MM.YYYY, DD/MM/YYYY, DD-MM-YYYY, YYYY.MM.DD, YYYY/MM/DD'
            )

        raise ValueError('Date receipt must be a valid date or string')
    
    @field_validator('user_id', mode='before')
    def validate_user_id(cls, value):
        if value is None:
            raise ValueError('user_id cannot be None')
        
        if isinstance(value, UUID):
            return value
        
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError('user_id cannot be empty')
            
            try:
                return UUID(value)
            except ValueError:
                raise ValueError('user_id must be a valid UUID string')
        
        raise ValueError('user_id must be a UUID or a valid UUID string')
    
class PassportCreate(PassportBase):
    pass

class PassportUpdate(BaseModel):
    birth_date: Optional[date] = None
    passport_number: Optional[str] = None
    passport_series: Optional[str] = None
    receipt_date: Optional[date] = None
    user_id: Optional[UserId] = None

    @field_validator('birth_date', mode='before')
    def validate_birth_date(cls, value):
        if value is None:
            raise ValueError('Birth date cannot be None')

        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError('Birth date cannot be empty')

            # Check for invalid characters
            if not re.fullmatch(r'[\d.\-\/ ]+', value):
                raise ValueError('Birth date contains invalid characters')

            # Formats to try parsing the date
            date_formats = [
                '%Y-%m-%d',  # 2000-01-01
                '%d.%m.%Y',  # 01.01.2000
                '%d/%m/%Y',  # 01/01/2000
                '%d-%m-%Y',  # 01-01-2000
                '%Y.%m.%d',  # 2000.01.01
                '%Y/%m/%d',  # 2000/01/01
            ]

            for fmt in date_formats:
                try:
                    parsed = datetime.strptime(value, fmt).date()
                    if parsed > date.today():
                        raise ValueError('Birth date cannot be in the future')
                    return parsed
                except ValueError:
                    continue

            raise ValueError(
                'Birth date must be in one of the formats: '
                'YYYY-MM-DD, DD.MM.YYYY, DD/MM/YYYY, DD-MM-YYYY, YYYY.MM.DD, YYYY/MM/DD'
            )

        raise ValueError('Birth date must be a valid date or string')
    
    @field_validator('passport_series', mode='before')
    def validate_passport_series(cls, value):
        if value is None:
            raise ValueError('passport_series cannot be empty or None')
        
        # Removing leading and trailing whitespace
        value = str(value).strip()

        if not isinstance(value, str):
            raise ValueError('passport_series must be a string')
        
        if len(value) != 4:
            raise ValueError('passport_series must be exactly 4 characters long with whitespace')
        
        if not re.match(r'^[1-9][0-9]{3}$', value):
            raise ValueError('passport_series must contain only digits and cannot start with zero')
        
        return value.upper()
    
    @field_validator('passport_number', mode='before')
    def validate_passport_number(cls, value):
        if value is None:
            raise ValueError('passport_number cannot be empty or None')
        
        # Removing leading and trailing whitespace
        value = str(value).strip()
        
        if not isinstance(value, str):
            raise ValueError('passport_number must be a string')
        
        if len(value) != 6:
            raise ValueError('passport_number must be exactly 6 characters long')
        
        if not re.match(r'^[0-9]{6}$', value):
            raise ValueError('passport_number must contain only digits')
        
        return value
    
    @field_validator('receipt_date', mode='before')
    def validate_receipt_date(cls, value):
        if value is None:
            raise ValueError('Date receipt cannot be None')

        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError('Date receipt cannot be empty')

            # Check for invalid characters
            if not re.fullmatch(r'[\d.\-\/ ]+', value):
                raise ValueError('Date receipt contains invalid characters')

            # Formats to try parsing the date
            date_formats = [
                '%Y-%m-%d',  # 2000-01-01
                '%d.%m.%Y',  # 01.01.2000
                '%d/%m/%Y',  # 01/01/2000
                '%d-%m-%Y',  # 01-01-2000
                '%Y.%m.%d',  # 2000.01.01
                '%Y/%m/%d',  # 2000/01/01
            ]

            for fmt in date_formats:
                try:
                    parsed = datetime.strptime(value, fmt).date()
                    return parsed
                except ValueError:
                    continue

            raise ValueError(
                'Date receipt must be in one of the formats: '
                'YYYY-MM-DD, DD.MM.YYYY, DD/MM/YYYY, DD-MM-YYYY, YYYY.MM.DD, YYYY/MM/DD'
            )

        raise ValueError('Date receipt must be a valid date or string')
    
    @field_validator('user_id', mode='before')
    def validate_user_id(cls, value):
        if value is None:
            raise ValueError('user_id cannot be None')
        
        if isinstance(value, UUID):
            return value
        
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError('user_id cannot be empty')
            
            try:
                return UUID(value)
            except ValueError:
                raise ValueError('user_id must be a valid UUID string')
        
        raise ValueError('user_id must be a UUID or a valid UUID string')
    
class PassportOut(PassportBase):
    id: UUID