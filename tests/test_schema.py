import pytest
from app import schema
from datetime import date
from pydantic import ValidationError

def test_users_create_valid():
    user = schema.UsersCreate(
        full_name="Иван Иванов",
        phone_number="+7-999-123-4567",
        birth_date="1990-01-01",
        passport="1234 567890",
    )
    assert user.full_name == "Иван Иванов"
    assert user.birth_date == date(1990, 1, 1)

def test_users_create_invalid_name():
    with pytest.raises(ValidationError):
        schema.UsersCreate(
            full_name="12345",  # wrong format
            phone_number="89991234567",
            birth_date="1990-01-01",
            passport="1234 567890",
        )


def test_users_create_invalid_phone():
    with pytest.raises(ValidationError):
        schema.UsersCreate(
            full_name="Петр Петров",
            phone_number="123",  # wrong format
            birth_date="1990-01-01",
            passport="1234 567890",
        )


def test_users_create_future_birthdate():
    with pytest.raises(ValidationError):
        schema.UsersCreate(
            full_name="Иван Иванов",
            phone_number="89991234567",
            birth_date="3000-01-01",  # future date
            passport="1234 567890",
        )


def test_users_create_invalid_passport():
    with pytest.raises(ValidationError):
        schema.UsersCreate(
            full_name="Иван Иванов",
            phone_number="89991234567",
            birth_date="1990-01-01",
            passport="ABC",  # wrong format
        )