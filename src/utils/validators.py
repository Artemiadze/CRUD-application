import re
from datetime import date, datetime
from uuid import UUID


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

def validate_birth_date(value):
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

def validate_receipt_date(value):
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

def convert_dates(obj):
    for field in ("birth_date", "receipt_date"):
        value = getattr(obj, field, None)
        if value is None:
            continue

        if isinstance(value, date):
            continue
        elif isinstance(value, datetime):
            setattr(obj, field, value.date())
        elif isinstance(value, str):
            date_formats = [
                "%Y-%m-%d",
                "%d.%m.%Y",
                "%d/%m/%Y",
                "%d-%m-%Y",
                "%Y.%m.%d",
                "%Y/%m/%d",
            ]
            parsed = None
            for fmt in date_formats:
                try:
                    parsed = datetime.strptime(value.strip(), fmt).date()
                    break
                except ValueError:
                    continue
            if parsed is None:
                raise ValueError(f"Field {field} must be a valid date string, got '{value}'")
            setattr(obj, field, parsed)
        else:
            raise TypeError(f"Field {field} must be a date, datetime, or string, got {type(value)}")

    return obj