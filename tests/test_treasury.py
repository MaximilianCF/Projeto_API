import pytest
from httpx import AsyncClient, ASGITransport
from main import app
import respx

@pytest.mark.asyncio
@respx.mock
async def test_get_treasury():
    # Mock para a URL externa da API do FRED
    mock_response = {
        "observations": [
            {"date": "2024-03-27", "value": "4.75"}
        ]
    }

    respx.get("https://api.stlouisfed.org/fred/series/observations").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/treasury-10y")

    assert response.status_code == 200
    assert response.json() == {
        "date": "2024-03-27",
        "yield_pct": 4.75
    }
