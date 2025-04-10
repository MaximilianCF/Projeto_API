# tests/test_usd_brl.py

import pytest
import respx
from httpx import ASGITransport, AsyncClient, Response
from app.main import app
from app.routes.v1.usd_brl import usdbrl_cache


@pytest.mark.asyncio
async def test_get_usdbrl_mock():
    usdbrl_cache.clear()

    mock_response = {
        "USDBRL": {
            "bid": "4.95",
            "ask": "4.97",
            "create_date": "2025-04-07 12:00:00"
        }
    }

    with respx.mock(base_url="https://economia.awesomeapi.com.br", assert_all_mocked=True) as respx_mock:
        respx_mock.get("/json/last/USD-BRL").mock(
            return_value=Response(200, json=mock_response)
        )

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/usd_brl")

        assert response.status_code == 200
        data = response.json()
        assert data["moeda"] == "USD/BRL"
        assert data["compra"] == 4.95
        assert data["venda"] == 4.97
        assert "data" in data
        assert "fonte" in data
