import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_get_treasury(mocker):
    # Mockando função externa que causa erro interno
    mocker.patch("routes.treasury.funcao_que_falha", return_value={"valor": 4.5})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/treasury-10y")

    assert response.status_code == 200
    assert response.json() == {"valor": 4.5}
