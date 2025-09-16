import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from src.domain.users import User
from src.infrastructure.models.users import UserModel
from src.infrastructure.repository.user_repo import UserRepository

@pytest.fixture
def mock_db_session():
    return Mock(spec=Session)

@pytest.fixture
def user_repository(mock_db_session):
    return UserRepository(db=mock_db_session)

def test_create_user_success(user_repository, mock_db_session):
    user = User(id=1, first_name="John", last_name="Doe", patronymic="Smith", phone_number="1234567890",
                birth_date="1990-01-01", passport_number="1234", passport_series="AB")
    mock_db_session.add = Mock()
    mock_db_session.commit = Mock()
    mock_db_session.refresh = Mock()

    result = user_repository.create_user(user)

    assert result == user
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()

def test_create_user_failure(user_repository, mock_db_session):
    user = User(id=1, first_name="John", last_name="Doe", patronymic="Smith", phone_number="1234567890",
                birth_date="1990-01-01", passport_number="1234", passport_series="AB")
    mock_db_session.commit.side_effect = Exception("DB Error")
    mock_db_session.rollback = Mock()

    with pytest.raises(Exception):
        user_repository.create_user(user)
    mock_db_session.rollback.assert_called_once()

def test_get_user_found(user_repository, mock_db_session):
    user_model = UserModel(id=1, first_name="John", last_name="Doe", patronymic="Smith", phone_number="1234567890",
                          birth_date="1990-01-01", passport_number="1234", passport_series="AB")
    mock_db_session.query().filter().first.return_value = user_model

    result = user_repository.get_user(1)

    assert isinstance(result, User)
    assert result.id == 1
    mock_db_session.query().filter().first.assert_called_once()

def test_get_user_not_found(user_repository, mock_db_session):
    mock_db_session.query().filter().first.return_value = None

    result = user_repository.get_user(1)

    assert result is None
    mock_db_session.query().filter().first.assert_called_once()

def test_get_user_by_full_name(user_repository, mock_db_session):
    user_model1 = UserModel(id=1, first_name="John", last_name="Doe", patronymic="Smith", phone_number="1234567890",
                           birth_date="1990-01-01", passport_number="1234", passport_series="AB")
    user_model2 = UserModel(id=2, first_name="John", last_name="Doe", patronymic="Smith", phone_number="0987654321",
                           birth_date="1990-01-02", passport_number="5678", passport_series="CD")
    
    # Mock the query chain for multiple filter calls
    mock_query = Mock()
    mock_db_session.query.return_value = mock_query
    
    mock_filter1 = Mock()  # First filter (first_name)
    mock_query.filter.return_value = mock_filter1
    
    mock_filter2 = Mock()  # Second filter (last_name)
    mock_filter1.filter.return_value = mock_filter2
    
    mock_filter3 = Mock()  # Third filter (patronymic)
    mock_filter2.filter.return_value = mock_filter3
    
    mock_filter3.all.return_value = [user_model1, user_model2]

    result = user_repository.get_user_by_full_name(first_name="John", last_name="Doe", patronymic="Smith")

    assert len(result) == 2
    assert all(isinstance(user, User) for user in result)
    assert result[0].id == 1
    assert result[1].id == 2

def test_get_user_by_phone_found(user_repository, mock_db_session):
    user_model = UserModel(id=1, first_name="John", last_name="Doe", patronymic="Smith", phone_number="1234567890",
                          birth_date="1990-01-01", passport_number="1234", passport_series="AB")
    mock_db_session.query().filter().first.return_value = user_model

    result = user_repository.get_user_by_phone("1234567890")

    assert isinstance(result, User)
    assert result.phone_number == "1234567890"
    mock_db_session.query().filter().first.assert_called_once()

def test_get_user_by_passport_found(user_repository, mock_db_session):
    user_model = UserModel(id=1, first_name="John", last_name="Doe", patronymic="Smith", phone_number="1234567890",
                          birth_date="1990-01-01", passport_number="1234", passport_series="AB")
    mock_db_session.query().filter().first.return_value = user_model

    result = user_repository.get_user_by_passport("AB", "1234")

    assert isinstance(result, User)
    assert result.passport_series == "AB"
    assert result.passport_number == "1234"

def test_update_user_success(user_repository, mock_db_session):
    user_model = UserModel(id=1, first_name="John", last_name="Doe", patronymic="Smith", phone_number="1234567890",
                          birth_date="1990-01-01", passport_number="1234", passport_series="AB")
    mock_db_session.query().filter().first.return_value = user_model
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.return_value = None

    user = User(id=1, first_name="Jane", last_name="Doe", patronymic=None, phone_number=None,
                birth_date=None, passport_number=None, passport_series=None)
    result = user_repository.update(user)

    assert result.first_name == "Jane"
    assert result.last_name == "Doe"
    assert result.patronymic == "Smith"
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()

def test_update_user_not_found(user_repository, mock_db_session):
    mock_db_session.query().filter().first.return_value = None

    user = User(id=1, first_name="Jane", last_name="Doe", patronymic=None, phone_number=None,
                birth_date=None, passport_number=None, passport_series=None)
    result = user_repository.update(user)

    assert result is None

def test_delete_user_success(user_repository, mock_db_session):
    user_model = UserModel(id=1, first_name="John", last_name="Doe", patronymic="Smith", phone_number="1234567890",
                          birth_date="1990-01-01", passport_number="1234", passport_series="AB")
    mock_db_session.query().filter().first.return_value = user_model
    mock_db_session.commit.return_value = None

    result = user_repository.delete_user(1)

    assert result is True
    mock_db_session.delete.assert_called_once()
    mock_db_session.commit.assert_called_once()

def test_delete_user_not_found(user_repository, mock_db_session):
    mock_db_session.query().filter().first.return_value = None

    result = user_repository.delete_user(1)

    assert result is None