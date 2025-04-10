from unittest.mock import AsyncMock, patch
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_selic():
    # Simula a resposta da API do BCB
    mock_response = [{"date": "01/01/2023", "value": 13.75}]

    # Configura o mock para incluir status_code, headers e json
    mock_get = AsyncMock()
    mock_get.return_value.status_code = 200
    mock_get.return_value.headers = {"Content-Type": "application/json"}
    mock_get.return_value.json = AsyncMock(return_value=mock_response)

    with patch("httpx.AsyncClient.get", new=mock_get):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/api/v1/selic")
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        data = await response.json()  # Adicionado await aqui

        # Corrigido para acessar o primeiro elemento da lista
        assert "01/01/2023" in data[0]["date"]
        assert isinstance(data[0]["date"], str)
        assert data[0]["value"] == 13.75
        assert isinstance(data[0]["value"], float)
        