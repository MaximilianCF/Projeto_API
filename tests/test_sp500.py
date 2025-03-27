import pytest
import respx
from httpx import AsyncClient, ASGITransport, Response
from main import app

@pytest.mark.asyncio
@respx.mock
async def test_get_sp500_mock():
    mock_response = {
        "chart": {
            "result": [{
                "timestamp": [1711497600],
                "indicators": {
                    "quote": [{
                        "close": [5250.22]
                    }]
                }
            }],
            "error": None
        }
    }

    respx.get("https://query1.finance.yahoo.com/v8/finance/chart/^GSPC?interval=1d&range=1d").mock(
        return_value=Response(200, json=mock_response)
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/sp500")

    assert response.status_code == 200
    data = response.json()
    assert data["close"] == 5250.22