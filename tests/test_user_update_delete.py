import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_token():
    response = client.post("/api/token", json={
        "username": "usuario_demo",
        "password": "senha_demo"
    })
    return response.json()["access_token"]

def test_update_user():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = client.put("/api/users/update", headers=headers, json={
        "email": "novoemail@pulso.io",
        "level": "Prata"
    })
    assert response.status_code == 200
    assert response.json()["user"]["email"] == "novoemail@pulso.io"
    assert response.json()["user"]["level"] == "Prata"

def test_delete_user():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete("/api/users/delete", headers=headers)
    assert response.status_code == 200
    assert "deletado com sucesso" in response.json()["message"]
