import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def get_cambio_usd_brl():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/usdbrl")
    assert response.status_code == 200
    data = response.json()
    assert "date" in data
    assert "value" in data
    assert "currency" in data
    assert data["currency"] == "USD/BRL"