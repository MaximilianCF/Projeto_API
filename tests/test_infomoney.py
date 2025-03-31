# tests/test_infomoney.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_infomoney_scraping():
    response = client.get("/api/webscraping/infomoney")
    assert response.status_code == 200
    data = response.json()
    assert "manchetes" in data
    assert isinstance(data["manchetes"], list)
    assert len(data["manchetes"]) > 0
