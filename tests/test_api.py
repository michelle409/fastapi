def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to the Community Posts API"


def test_register_and_fetch_user(client, registered_user):
    response = client.get(f"/users/{registered_user['id']}")
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert "password" not in response.json()


def test_duplicate_email_returns_conflict(client, registered_user):
    response = client.post("/users/", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 409


def test_post_lifecycle(client, auth_headers):
    created = client.post("/posts/", headers=auth_headers, json={"title": "First post", "content": "Hello world", "published": True})
    assert created.status_code == 201
    post_id = created.json()["id"]

    listed = client.get("/posts/", headers=auth_headers)
    assert listed.status_code == 200
    assert listed.json()[0]["Post"]["id"] == post_id
    assert listed.json()[0]["votes"] == 0

    updated = client.put(f"/posts/{post_id}", headers=auth_headers, json={"title": "Updated", "content": "Edited", "published": True})
    assert updated.status_code == 200
    assert updated.json()["title"] == "Updated"

    deleted = client.delete(f"/posts/{post_id}", headers=auth_headers)
    assert deleted.status_code == 204


def test_vote_add_and_remove(client, auth_headers):
    post = client.post("/posts/", headers=auth_headers, json={"title": "Vote me", "content": "Content"}).json()
    add = client.post("/vote/", headers=auth_headers, json={"post_id": post["id"], "dir": 1})
    assert add.status_code == 201
    assert add.json()["message"] == "successfully added vote"
    remove = client.post("/vote/", headers=auth_headers, json={"post_id": post["id"], "dir": 0})
    assert remove.status_code == 201
    assert remove.json()["message"] == "successfully deleted vote"
