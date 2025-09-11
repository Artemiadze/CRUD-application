def test_create_user_success(client):
    payload = {
        "full_name": "Иван Иванов",
        "phone_number": "89991234567",
        "birth_date": "1990-01-01",
        "passport": "1234 567890"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Иван Иванов"
    assert "id" in data  # id should be generated


def test_create_user_invalid(client):
    payload = {
        "full_name": "",
        "phone_number": "89991234567",
        "birth_date": "1990-01-01",
        "passport": "1234 567890"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 422  # validation error


def test_get_user_success(client):
    payload = {
        "full_name": "Alice Smith",
        "phone_number": "89995554433",
        "birth_date": "1985-05-20",
        "passport": "1111 222233"
    }

    created = client.post("/users/", json=payload).json()
    response = client.get(f"/users/id/{created['id']}")
    assert response.status_code == 200
    assert response.json()["full_name"] == "Alice Smith"


def test_get_user_not_found(client):
    response = client.get("/users/id/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Person not found"


def test_update_user(client):
    payload = {
        "full_name": "Сергей Сергеев",
        "phone_number": "89990001122",
        "birth_date": "1992-03-15",
        "passport": "2222 333344"
    }
    created = client.post("/users/", json=payload).json()
    update_payload = {"full_name": "Сергей С"}
    response = client.put(f"/users/{created['id']}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["full_name"] == "Сергей С"


def test_delete_user(client):
    payload = {
        "full_name": "Удаляемый Пользователь",
        "phone_number": "89991112233",
        "birth_date": "1995-07-10",
        "passport": "3333 444455"
    }
    created = client.post("/users/", json=payload).json()
    response = client.delete(f"/users/{created['id']}")
    assert response.status_code == 200
    assert response.json()["detail"] == "User deleted"

    response = client.get(f"/users/id/{created['id']}")
    assert response.status_code == 404
