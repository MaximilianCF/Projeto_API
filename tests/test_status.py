# tests/test_status.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_status():
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "API" in data["message"]

