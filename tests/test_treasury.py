import pytest
import respx
from httpx import ASGITransport, AsyncClient, Response
from app.main import app
from app.routes.v1.treasury import treasury_cache


@pytest.mark.asyncio
async def test_get_treasury_mock():
    treasury_cache.clear()

    mock_data = {
        "observations": [
            {
                "date": "2025-04-05",
                "value": "4.28"
            }
        ]
    }

    with respx.mock(base_url="https://api.stlouisfed.org", assert_all_mocked=True) as respx_mock:
        respx_mock.get("/fred/series/observations").mock(
            return_value=Response(200, json=mock_data)
        )

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/treasury")

        assert response.status_code == 200, f"❌ status {response.status_code} - {response.text}"
        data = response.json()
        assert data["valor"] == 4.28
        assert data["data"] == "2025-04-05"
