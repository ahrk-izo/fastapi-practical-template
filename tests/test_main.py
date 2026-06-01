from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check() -> None:
    """GET /health が200を返し、statusとenvironmentを含むJSONを返すことを確認する。

    Returns:
        None
    """
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "environment": "local",
    }
