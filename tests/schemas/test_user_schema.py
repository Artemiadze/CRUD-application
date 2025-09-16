import pytest
from datetime import date
from src.schemas.user_schema import UsersCreate, UsersUpdate, UsersOut

def test_users_create_valid_data():
    data = {
        "first_name": "ivan",
        "last_name": "petrov",
        "patronymic": "sergeevich",
        "phone_number": "+71234567890",
        "birth_date": "01.01.2000",
        "passport_series": "1234",
        "passport_number": "123456"
    }
    user = UsersCreate(**data)
    assert user.first_name == "Ivan"
    assert user.last_name == "Petrov"
    assert user.patronymic == "Sergeevich"
    assert user.phone_number == "+71234567890"
    assert user.birth_date == date(2000, 1, 1)
    assert user.passport_series == "1234"
    assert user.passport_number == "123456"

def test_users_create_invalid_first_name():
    with pytest.raises(ValueError, match="first_name must contain only alphabetic characters"):
        UsersCreate(first_name="Ivan123", last_name="Petrov", patronymic="Sergeevich", phone_number="+71234567890",
                    birth_date="01.01.2000", passport_series="1234", passport_number="123456")

def test_users_create_empty_phone_number():
    with pytest.raises(ValueError, match="Phone number cannot be empty or None"):
        UsersCreate(first_name="Ivan", last_name="Petrov", patronymic="Sergeevich", phone_number="",
                    birth_date="01.01.2000", passport_series="1234", passport_number="123456")

def test_users_create_invalid_phone_length():
    with pytest.raises(ValueError, match="Phone number must contain exactly 11 digits"):
        UsersCreate(first_name="Ivan", last_name="Petrov", patronymic="Sergeevich", phone_number="+712345678",
                    birth_date="01.01.2000", passport_series="1234", passport_number="123456")

def test_users_create_underage():
    with pytest.raises(ValueError, match="User must be at least 14 years old"):
        UsersCreate(first_name="Ivan", last_name="Petrov", patronymic="Sergeevich", phone_number="+71234567890",
                    birth_date="01.01.2012", passport_series="1234", passport_number="123456")

def test_users_create_invalid_passport_series_length():
    with pytest.raises(ValueError, match="passport_series must be exactly 4 characters long with whitespace"):
        UsersCreate(first_name="Ivan", last_name="Petrov", patronymic="Sergeevich", phone_number="+71234567890",
                    birth_date="01.01.2000", passport_series="123", passport_number="123456")

def test_users_update_valid_partial_data():
    data = {
        "first_name": "john",
        "last_name": None,
        "patronymic": None,
        "phone_number": None,
        "birth_date": None,
        "passport_series": None,
        "passport_number": None
    }
    user = UsersUpdate(**data)
    assert user.first_name == "John"
    assert user.last_name is None
    assert user.patronymic is None
    assert user.phone_number is None
    assert user.birth_date is None
    assert user.passport_series is None
    assert user.passport_number is None

def test_users_update_invalid_phone_number():
    with pytest.raises(ValueError, match="Phone number must contain exactly 11 digits"):
        UsersUpdate(first_name=None, last_name=None, patronymic=None, phone_number="+712345678",
                    birth_date=None, passport_series=None, passport_number=None)

def test_users_out_valid_data():
    data = {
        "id": 1,
        "first_name": "ivan",
        "last_name": "petrov",
        "patronymic": "sergeevich",
        "phone_number": "+71234567890",
        "birth_date": "01.01.2000",
        "passport_series": "1234",
        "passport_number": "123456"
    }
    user = UsersOut(**data)
    assert user.id == 1
    assert user.first_name == "Ivan"
    assert user.last_name == "Petrov"
    assert user.patronymic == "Sergeevich"
    assert user.phone_number == "+71234567890"
    assert user.birth_date == date(2000, 1, 1)
    assert user.passport_series == "1234"
    assert user.passport_number == "123456"