import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_query_happy_path(client):
    payload = {"question": "What is the SLA response time for Sev-1 incidents?"}
    response = client.post("/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert isinstance(data["sources"], list)
    assert len(data["sources"]) > 0

def test_query_invalid_input(client):
    # Missing required 'question' parameter -> expect 422
    response = client.post("/query", json={})
    assert response.status_code == 422