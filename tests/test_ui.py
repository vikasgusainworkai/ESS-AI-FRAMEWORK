from fastapi.testclient import TestClient

from ess_app.main import app

client = TestClient(app)


def test_index_serves_users_page() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    page = response.text
    assert "<title>User Management</title>" in page
    assert "/api/users" in page
    for element_id in ['id="user-form"', 'id="users-body"', 'id="search"']:
        assert element_id in page


def test_index_does_not_render_user_data_as_html() -> None:
    # User values are inserted with textContent, never innerHTML.
    response = client.get("/")
    assert response.status_code == 200
    assert "innerHTML" not in response.text


def test_index_not_in_api_schema() -> None:
    assert "/" not in client.get("/openapi.json").json()["paths"]
