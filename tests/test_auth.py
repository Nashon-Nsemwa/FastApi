def test_login_success(client):
    user_payload = {"email": "auth@example.com", "password": "password"}
    client.post("/users/", json=user_payload)

    response = client.post(
        "/login",
        data={"username": user_payload["email"], "password": user_payload["password"]},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client):
    user_payload = {"email": "authfail@example.com", "password": "password"}
    client.post("/users/", json=user_payload)

    response = client.post(
        "/login",
        data={"username": user_payload["email"], "password": "wrongpassword"},
    )

    assert response.status_code == 403


def test_login_user_not_found(client):
    response = client.post(
        "/login",
        data={"username": "missing@example.com", "password": "password"},
    )
    assert response.status_code == 403
