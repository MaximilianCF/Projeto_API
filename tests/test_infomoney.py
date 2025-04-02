from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_infomoney_scraping():
    response = client.get("/api/v1/webscraping/infomoney")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["dados"], list)

    json_data = response.json()
    assert "fonte" in json_data
    assert json_data["fonte"] == "InfoMoney"
    assert "dados" in json_data
    assert isinstance(json_data["dados"], list)

    if json_data["dados"]:  # Se houver manchetes
        item = json_data["dados"][0]
        assert "titulo" in item
        assert "url" in item
