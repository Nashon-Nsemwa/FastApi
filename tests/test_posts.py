def create_user_and_token(client, email):
    password = "password"
    client.post("/users/", json={"email": email, "password": password})
    login_response = client.post(
        "/login",
        data={"username": email, "password": password},
    )
    return login_response.json()["access_token"]


def test_unauthorized_create_post(client):
    response = client.post(
        "/posts/",
        json={"title": "No Auth", "content": "no auth", "published": True},
    )
    assert response.status_code == 401


def test_create_and_get_post(client):
    token = create_user_and_token(client, "poster@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/posts/",
        json={"title": "Test Post", "content": "Test content", "published": True},
        headers=headers,
    )
    assert create_response.status_code == 201
    post_data = create_response.json()
    assert post_data["title"] == "Test Post"
    assert post_data["content"] == "Test content"
    assert post_data["owner_id"] == 1

    list_response = client.get("/posts/", headers=headers)
    assert list_response.status_code == 200
    posts = list_response.json()
    assert len(posts) == 1
    assert posts[0]["Post"]["id"] == post_data["id"]

    get_response = client.get(f"/posts/{post_data['id']}", headers=headers)
    assert get_response.status_code == 200
    single_post = get_response.json()
    assert single_post["Post"]["id"] == post_data["id"]


def test_post_update_and_delete_with_authorization(client):
    owner_token = create_user_and_token(client, "owner@example.com")
    owner_headers = {"Authorization": f"Bearer {owner_token}"}

    new_post = client.post(
        "/posts/",
        json={"title": "Owner Post", "content": "Owner content", "published": True},
        headers=owner_headers,
    )
    assert new_post.status_code == 201
    post_id = new_post.json()["id"]

    other_token = create_user_and_token(client, "other@example.com")
    other_headers = {"Authorization": f"Bearer {other_token}"}

    update_forbidden = client.put(
        f"/posts/{post_id}",
        json={"title": "New Title", "content": "New content", "published": False},
        headers=other_headers,
    )
    assert update_forbidden.status_code == 403

    delete_forbidden = client.delete(f"/posts/{post_id}", headers=other_headers)
    assert delete_forbidden.status_code == 403

    update_response = client.put(
        f"/posts/{post_id}",
        json={"title": "Updated Title", "content": "Updated content", "published": True},
        headers=owner_headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Title"

    delete_response = client.delete(f"/posts/{post_id}", headers=owner_headers)
    assert delete_response.status_code == 204
