import pytest
import respx
from httpx import ASGITransport, AsyncClient, Response
from app.main import app
from app.routes.v1.ibov import ibov_cache


@pytest.mark.asyncio
async def test_get_ibov_mock():
    ibov_cache.clear()

    mock_data = {
        "chart": {
            "result": [{
                "meta": {
                    "regularMarketPrice": 128560.24,
                    "regularMarketTime": 1711497600
                }
            }],
            "error": None
        }
    }

    with respx.mock(base_url="https://query1.finance.yahoo.com", assert_all_mocked=True) as respx_mock:
        respx_mock.get("/v8/finance/chart/^BVSP", params={"interval": "1d", "range": "1d"}).mock(
            return_value=Response(200, json=mock_data)
        )

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/ibov")

        assert response.status_code == 200, f"❌ status {response.status_code} - {response.text}"
        data = response.json()
        assert data["valor"] == 128560.24
        assert "data" in data
