import pytest
from httpx import ASGITransport, AsyncClient

from app.core.security.jwt_auth import create_access_token
from app.main import app


@pytest.mark.asyncio
async def test_get_submissoes_autenticado():
    token = create_access_token(data={"sub": "1"})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/api/v1/submissoes/",
            headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_submissoes_nao_autenticado():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/submissoes/")
    assert response.status_code == 401
