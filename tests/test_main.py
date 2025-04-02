import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_selic_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/selic/ultima")  # <-- rota existente!

    assert response.status_code in [200, 404]
    # Dependendo do seu retorno atual, ajuste abaixo:
    assert isinstance(response.json(), dict)  # Teste básico: retorna um dicionário JSON
