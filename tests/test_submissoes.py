import io
import pytest
from httpx import ASGITransport, AsyncClient
from fastapi import Depends
from app.main import app
from app.models.user import User
from app.routes.v1 import submissoes

# ==== MOCK DO get_current_user PARA TODOS OS TESTES ====

async def fake_current_user():
    return User(id=1, username="mockuser", email="mock@user.com")

app.dependency_overrides[submissoes.get_current_user] = fake_current_user


@pytest.mark.asyncio
async def test_get_submissoes_autenticado():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/submissoes/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_submissoes_nao_autenticado():
    # Remove override temporariamente
    app.dependency_overrides = {}

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/submissoes/")

    # Restaura o mock
    app.dependency_overrides[submissoes.get_current_user] = fake_current_user

    assert response.status_code == 401, f"Unexpected status code: {response.status_code}"
    assert "Not authenticated" in response.text or "Não autenticado" in response.text


@pytest.mark.asyncio
async def test_post_submissao_csv_valido():
    file_content = "coluna1,coluna2\n1,2\n3,4"
    file = io.BytesIO(file_content.encode("utf-8"))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/submissoes/?challenge_id=1",
            files={"file": ("arquivo.csv", file, "text/csv")},
        )

    assert response.status_code == 200
    json = response.json()
    assert json["arquivo"] == "arquivo.csv"
    assert json["desafio_id"] == 1
    assert "usuario" in json
