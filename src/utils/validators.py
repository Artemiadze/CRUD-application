import re
from datetime import date, datetime
from uuid import UUID
from typing import Any


DATE_FORMATS = [
    '%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y',
    '%d-%m-%Y', '%Y.%m.%d', '%Y/%m/%d',
]

def validate_first_name(value):
    if value is None or not value.strip():
        return value  # Skip it if the field is not provided.
        
    if not isinstance(value, str):
        raise ValueError('first_name must be a string')
        
    if not re.match(r'^[a-zA-Zа-яА-Я]*$', value):
        raise ValueError('first_name must contain only alphabetic characters')
        
    return value.title()

def validate_last_name(value):
    if value is None or not value.strip():
        raise ValueError('last_name cannot be empty or None')
        
    if not isinstance(value, str):
        raise ValueError('last_name must be a string')
        
    if not re.match(r'^[a-zA-Zа-яА-Я]*$', value):
        raise ValueError('last_name must contain only alphabetic characters')
        
    return value.title()

def validate_patronymic(value):      
    if not isinstance(value, str):
        raise ValueError('patronymic must be a string')
        
    if not re.match(r'^[a-zA-Zа-яА-Я]*$', value):
        raise ValueError('patronymic must contain only alphabetic characters')
        
    return value.title()

def validate_phone_number(value):
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

def validate_passport_series(value):
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

def validate_passport_number(value):
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

def parse_date(value: Any, field_name: str, future_allowed: bool = True) -> date:
    if value is None:
        raise ValueError(f"{field_name} cannot be None")

    if isinstance(value, date):
        if not future_allowed and value > date.today():
            raise ValueError(f"{field_name} cannot be in the future")
        return value

    if isinstance(value, datetime):
        value = value.date()
        if not future_allowed and value > date.today():
            raise ValueError(f"{field_name} cannot be in the future")
        return value

    if isinstance(value, str):
        value = value.strip()
        if not value:
            raise ValueError(f"{field_name} cannot be empty")
        if not re.fullmatch(r'[\d.\-\/ ]+', value):
            raise ValueError(f"{field_name} contains invalid characters")

        for fmt in DATE_FORMATS:
            try:
                parsed = datetime.strptime(value, fmt).date()
                if not future_allowed and parsed > date.today():
                    raise ValueError(f"{field_name} cannot be in the future")
                return parsed
            except ValueError:
                continue

        raise ValueError(
            f"{field_name} must be in one of the formats: "
            "YYYY-MM-DD, DD.MM.YYYY, DD/MM/YYYY, DD-MM-YYYY, YYYY.MM.DD, YYYY/MM/DD"
        )

    raise TypeError(f"{field_name} must be a date, datetime, or string, got {type(value)}")

def convert_dates(obj):
    for field, future_allowed in (("birth_date", False), ("receipt_date", True)):
        value = getattr(obj, field, None)
        if value is not None:
            setattr(obj, field, parse_date(value, field, future_allowed))
    return obj

def validate_user_id(value):
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