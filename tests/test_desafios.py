import pytest
from httpx import ASGITransport, AsyncClient

from app.core.security.jwt_auth import create_access_token, get_current_user
from app.main import app

# Mocka o retorno do get_current_user para evitar checagens de usuário real
app.dependency_overrides[get_current_user] = lambda: {"id": 1}

def debug_routes():
    print("\n\n--- Rotas Registradas no app ---")
    for route in app.routes:
        print(f"  • {route.path}")
    print("--- Fim das rotas ---\n\n")

@pytest.mark.asyncio
async def test_get_desafios_autenticado():
    debug_routes()

    token = create_access_token(data={"sub": "1"})
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/api/v1/desafios/",
            headers={"Authorization": f"Bearer {token}"}
        )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_desafios_nao_autenticado():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/desafios/")

    assert response.status_code == 401
