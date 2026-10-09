from typing import Any

from fastapi.testclient import TestClient

from ess_app.main import app

client = TestClient(app)

ADA = {"name": "Ada Lovelace", "email": "ada@example.com", "role": "admin"}


def create(**overrides: Any) -> dict[str, Any]:
    response = client.post("/api/users", json={**ADA, **overrides})
    assert response.status_code == 201, response.text
    body: dict[str, Any] = response.json()
    return body


def fields(response: Any) -> set[str]:
    return {d["field"] for d in response.json()["details"]}


# --- happy paths ---


def test_create_returns_user() -> None:
    user = create(email="  Ada@Example.com ")
    assert user["email"] == "ada@example.com"
    assert user["status"] == "active"
    assert user["role"] == "admin"
    assert user["id"]


def test_list_and_search() -> None:
    ada = create()
    grace = create(name="Grace Hopper", email="grace@navy.mil", role="user", status="inactive")
    assert client.get("/api/users").json() == [ada, grace]
    assert client.get("/api/users", params={"q": "GRACE"}).json() == [grace]
    assert client.get("/api/users", params={"role": "admin"}).json() == [ada]
    assert client.get("/api/users", params={"status": "inactive"}).json() == [grace]
    assert client.get("/api/users", params={"q": "nobody"}).json() == []


def test_get_user() -> None:
    ada = create()
    response = client.get(f"/api/users/{ada['id']}")
    assert response.status_code == 200
    assert response.json() == ada


def test_patch_user() -> None:
    ada = create()
    response = client.patch(f"/api/users/{ada['id']}", json={"name": "Ada King", "role": "user"})
    assert response.status_code == 200
    assert response.json() == {**ada, "name": "Ada King", "role": "user"}


def test_deactivate_user() -> None:
    ada = create()
    response = client.post(f"/api/users/{ada['id']}/deactivate")
    assert response.status_code == 200
    assert response.json()["status"] == "inactive"
    assert client.get(f"/api/users/{ada['id']}").json()["status"] == "inactive"


def test_delete_user() -> None:
    ada = create()
    response = client.delete(f"/api/users/{ada['id']}")
    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/api/users/{ada['id']}").status_code == 404


# --- duplicate emails ---


def test_duplicate_email_on_create_is_409_case_insensitive() -> None:
    create()
    response = client.post("/api/users", json={**ADA, "email": "ADA@EXAMPLE.COM"})
    assert response.status_code == 409
    assert response.json()["error"] == "email_already_exists"
    assert len(client.get("/api/users").json()) == 1


def test_duplicate_email_on_patch_is_409() -> None:
    ada = create()
    create(email="grace@example.com")
    response = client.patch(f"/api/users/{ada['id']}", json={"email": "Grace@example.com"})
    assert response.status_code == 409
    assert response.json()["error"] == "email_already_exists"


# --- validation ---


def test_create_validation_reports_each_field() -> None:
    response = client.post(
        "/api/users", json={"name": " ", "email": "nope", "role": "root", "status": "gone"}
    )
    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "validation_error"
    assert fields(response) == {"name", "email", "role", "status"}
    assert all(d["message"] for d in body["details"])


def test_validation_does_not_echo_input() -> None:
    response = client.post("/api/users", json={**ADA, "email": "leak-me-not"})
    assert response.status_code == 422
    assert "leak-me-not" not in response.text


def test_missing_fields_rejected() -> None:
    response = client.post("/api/users", json={})
    assert response.status_code == 422
    assert fields(response) == {"name", "email", "role"}


def test_unknown_field_rejected() -> None:
    response = client.post("/api/users", json={**ADA, "is_admin": True})
    assert response.status_code == 422
    assert fields(response) == {"is_admin"}


def test_malformed_json_rejected() -> None:
    response = client.post(
        "/api/users", content="{not json", headers={"content-type": "application/json"}
    )
    assert response.status_code == 422
    assert response.json()["error"] == "validation_error"


def test_patch_validation_and_null() -> None:
    ada = create()
    assert client.patch(f"/api/users/{ada['id']}", json={"email": "bad"}).status_code == 422
    response = client.patch(f"/api/users/{ada['id']}", json={"name": None})
    assert response.status_code == 422
    assert client.get(f"/api/users/{ada['id']}").json() == ada


def test_invalid_query_filter_rejected() -> None:
    response = client.get("/api/users", params={"role": "root"})
    assert response.status_code == 422
    assert fields(response) == {"role"}


# --- not found ---


def test_unknown_id_is_404_everywhere() -> None:
    for method, path in [
        ("GET", "/api/users/missing"),
        ("PATCH", "/api/users/missing"),
        ("POST", "/api/users/missing/deactivate"),
        ("DELETE", "/api/users/missing"),
    ]:
        response = client.request(method, path, json={"name": "X"} if method == "PATCH" else None)
        assert response.status_code == 404, (method, path)
        assert response.json()["error"] == "user_not_found"
