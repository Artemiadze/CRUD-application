import pytest
from unittest.mock import Mock
from src.domain.users import User
from src.core.exceptions import DuplicateError, NotFoundError
from src.services.user_service import UserService

@pytest.fixture
def mock_repo():
    return Mock()

@pytest.fixture
def user_service(mock_repo):
    return UserService(repo=mock_repo)

def test_create_user_success(user_service, mock_repo):
    user = User(id=1, first_name="John", last_name="Doe", patronymic="Smith", phone_number="1234567890",
                birth_date="1990-01-01", passport_number="1234", passport_series="AB")
    mock_repo.get_user_by_full_name.return_value = []
    mock_repo.get_user_by_phone.return_value = None
    mock_repo.get_user_by_passport.return_value = None
    mock_repo.create_user.return_value = user

    result = user_service.create_user(user)

    assert result == user
    mock_repo.create_user.assert_called_once_with(user)

def test_create_user_duplicate_full_name(user_service, mock_repo):
    user = User(id=1, first_name="John", last_name="Doe", patronymic="Smith", phone_number="1234567890",
                birth_date="1990-01-01", passport_number="1234", passport_series="AB")
    mock_repo.get_user_by_full_name.return_value = [user]

    with pytest.raises(DuplicateError, match="full_name"):
        user_service.create_user(user)

def test_create_user_duplicate_phone(user_service, mock_repo):
    user = User(id=1, first_name="John", last_name="Doe", patronymic="Smith", phone_number="1234567890",
                birth_date="1990-01-01", passport_number="1234", passport_series="AB")
    mock_repo.get_user_by_full_name.return_value = []
    mock_repo.get_user_by_phone.return_value = user

    with pytest.raises(DuplicateError, match="phone_number"):
        user_service.create_user(user)

def test_create_user_duplicate_passport(user_service, mock_repo):
    user = User(id=1, first_name="John", last_name="Doe", patronymic="Smith", phone_number="1234567890",
                birth_date="1990-01-01", passport_number="1234", passport_series="AB")
    mock_repo.get_user_by_full_name.return_value = []
    mock_repo.get_user_by_phone.return_value = None
    mock_repo.get_user_by_passport.return_value = user

    with pytest.raises(DuplicateError, match="passport"):
        user_service.create_user(user)

def test_get_user_success(user_service, mock_repo):
    user = User(id=1, first_name="John", last_name="Doe", patronymic="Smith", phone_number="1234567890",
                birth_date="1990-01-01", passport_number="1234", passport_series="AB")
    mock_repo.get_user.return_value = user

    result = user_service.get_user(1)

    assert result == user
    mock_repo.get_user.assert_called_once_with(1)

def test_update_user_success(user_service, mock_repo):
    existing_user = User(id=1, first_name="John", last_name="Doe", patronymic="Smith", phone_number="1234567890",
                        birth_date="1990-01-01", passport_number="1234", passport_series="AB")
    updated_user = User(id=1, first_name="Jane", last_name="Doe", patronymic=None, phone_number="1234567890",
                        birth_date="1990-01-01", passport_number="1234", passport_series="AB")
    mock_repo.get_user.return_value = existing_user
    mock_repo.get_user_by_full_name.return_value = []
    mock_repo.get_user_by_phone.return_value = None
    mock_repo.get_user_by_passport_number.return_value = None
    mock_repo.get_user_by_passport_series.return_value = None
    mock_repo.update.return_value = updated_user

    result = user_service.update_user(updated_user)

    assert result == updated_user
    mock_repo.update.assert_called_once_with(updated_user)



def test_update_user_duplicate_full_name(user_service, mock_repo):
    existing_user = User(id=1, first_name="John", last_name="Doe", patronymic="Smith", phone_number="1234567890",
                        birth_date="1990-01-01", passport_number="1234", passport_series="AB")
    updated_user = User(id=1, first_name="Jane", last_name="Doe", patronymic="Smith", phone_number="1234567890",
                        birth_date="1990-01-01", passport_number="1234", passport_series="AB")
    mock_repo.get_user.return_value = existing_user
    mock_repo.get_user_by_full_name.return_value = [updated_user]

    with pytest.raises(DuplicateError, match="full_name"):
        user_service.update_user(updated_user)

def test_delete_user_success(user_service, mock_repo):
    user = User(id=1, first_name="John", last_name="Doe", patronymic="Smith", phone_number="1234567890",
                birth_date="1990-01-01", passport_number="1234", passport_series="AB")
    mock_repo.get_user.return_value = user
    mock_repo.delete_user.return_value = True

    result = user_service.delete_user(1)

    assert result is True
    mock_repo.delete_user.assert_called_once_with(1)

def test_delete_user_not_found(user_service, mock_repo):
    mock_repo.get_user.return_value = None
    with pytest.raises(NotFoundError, match="User with id=1 not found"):
        user_service.delete_user(1)