from fastapi.testclient import TestClient

from ess_app.main import app


@app.get("/_test/boom")
def boom() -> None:
    raise RuntimeError("secret connection string should never leak")


def test_unhandled_error_hides_internals() -> None:
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/_test/boom")
    assert response.status_code == 500
    assert response.json() == {"error": "internal_error"}
    assert "secret" not in response.text
