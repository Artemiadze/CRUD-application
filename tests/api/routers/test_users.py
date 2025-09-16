import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from src.core.exceptions import NotFoundError
from src.api.routers.users import router
from src.schemas.user_schema import UsersUpdate, UsersOut
from src.domain.users import User

from fastapi import FastAPI

app = FastAPI()
app.include_router(router)

client = TestClient(app)

# Тестовые данные
test_user_data = {
    "id": 1,
    "first_name": "Ivan",
    "last_name": "Ivanov",
    "patronymic": "Petrovich",
    "phone_number": "+79995553322",
    "birth_date": "1984-01-01",
    "passport_series": "4321",
    "passport_number": "987654"
}

test_user_data_serializable = test_user_data.copy()

test_user_update = UsersUpdate(
    first_name="Petr"
)

@pytest.fixture
def mock_user_service():
    with patch("src.api.routers.users.UserService") as MockService:
        service = MockService.return_value
        service.create_user.return_value = User(**test_user_data)
        service.get_user.return_value = User(**test_user_data)
        service.get_user_by_full_name.return_value = [User(**test_user_data)]
        service.update_user.return_value = User(**{**test_user_data, "first_name": "Petr"})
        service.delete_user.return_value = None
        yield service

@pytest.fixture
def mock_db():
    with patch("src.api.routers.users.get_db") as mock:
        yield mock

""""
def test_create_user(mock_user_service, mock_db):
    mock_user_service.create_user.return_value = UsersOut(**test_user_data_serializable)
    response = client.post("/users/", json=test_user_data.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Ivan"
"""

def test_get_user(mock_user_service, mock_db):
    response = client.get("/users/id/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    mock_user_service.get_user.assert_called_once_with(1)

def test_get_user_not_found(mock_user_service, mock_db):
    mock_user_service.get_user.side_effect = NotFoundError("User", 999)
    response = client.get("/users/id/999")
    assert response.status_code == 404

def test_get_user_by_full_name(mock_user_service, mock_db):
    response = client.get("/users/find", params={"first_name": "Ivan"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["first_name"] == "Ivan"

def test_update_user(mock_user_service, mock_db):
    response = client.put("/users/1", json=test_user_update.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Petr"
    mock_user_service.update_user.assert_called_once()

def test_delete_user(mock_user_service, mock_db):
    response = client.delete("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "User deleted successfully"
    mock_user_service.delete_user.assert_called_once_with(1)