import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.models.user import User
from app.routes.v1 import leaderboard


# ==== MOCK DO get_current_user PARA TODOS OS TESTES ====

async def fake_current_user():
    return User(id=1, username="mockuser", email="mock@user.com")

app.dependency_overrides[leaderboard.get_current_user] = fake_current_user


@pytest.mark.asyncio
async def test_leaderboard_authenticated():
    """Testa o acesso autenticado ao leaderboard."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/leaderboard/")

    assert response.status_code == 200
    json_data = response.json()
    assert isinstance(json_data, list)
    # Como a rota retorna ranking_falso, vamos verificar isso
    assert len(json_data) == 3
    assert json_data[0]["username"] == "alice"
    assert json_data[0]["pontuacao"] == 95.2
    assert json_data[1]["username"] == "bob"
    assert json_data[1]["pontuacao"] == 89.4
    assert json_data[2]["username"] == "carol"
    assert json_data[2]["pontuacao"] == 77.8


@pytest.mark.asyncio
async def test_leaderboard_unauthenticated():
    """Testa acesso sem token — deve retornar 401."""
    # Remove override temporariamente
    app.dependency_overrides = {}

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/leaderboard/")

    # Restaura o mock
    app.dependency_overrides[leaderboard.get_current_user] = fake_current_user

    assert response.status_code == 401, f"Esperado 401 Unauthorized, obtido {response.status_code}"
    assert "Not authenticated" in response.text or "Não autenticado" in response.text
