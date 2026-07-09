def test_create_user(client):
    payload = {"email": "user@example.com", "password": "password"}
    response = client.post("/users/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert "id" in data
    assert "created_at" in data


def test_get_user(client):
    payload = {"email": "reader@example.com", "password": "password"}
    create_response = client.post("/users/", json=payload)
    user_id = create_response.json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == payload["email"]
