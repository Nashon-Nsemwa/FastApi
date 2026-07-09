def create_user_and_token(client, email):
    password = "password"
    client.post("/users/", json={"email": email, "password": password})
    login_response = client.post(
        "/login",
        data={"username": email, "password": password},
    )
    return login_response.json()["access_token"]


def test_vote_create_and_delete(client):
    token = create_user_and_token(client, "voter@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    post_response = client.post(
        "/posts/",
        json={"title": "Vote Post", "content": "Vote content", "published": True},
        headers=headers,
    )
    assert post_response.status_code == 201
    post_id = post_response.json()["id"]

    vote_response = client.post(
        "/vote/",
        json={"post_id": post_id, "dir": 1},
        headers=headers,
    )
    assert vote_response.status_code == 201
    assert vote_response.json()["message"] == "successfully added vote"

    duplicate_vote = client.post(
        "/vote/",
        json={"post_id": post_id, "dir": 1},
        headers=headers,
    )
    assert duplicate_vote.status_code == 409

    delete_vote = client.post(
        "/vote/",
        json={"post_id": post_id, "dir": 0},
        headers=headers,
    )
    assert delete_vote.status_code == 201
    assert delete_vote.json()["message"] == "successfully deleted vote"


def test_unauthorized_vote(client):
    token = create_user_and_token(client, "voter2@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    post_response = client.post(
        "/posts/",
        json={"title": "Vote Post 2", "content": "Vote content 2", "published": True},
        headers=headers,
    )
    assert post_response.status_code == 201
    post_id = post_response.json()["id"]

    response = client.post(
        "/vote/",
        json={"post_id": post_id, "dir": 1},
    )
    assert response.status_code == 401
