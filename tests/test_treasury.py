import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_get_treasury():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/treasury-10y")
    assert response.status_code in [200, 404]
    data = response.json()
    assert "date" in data
    assert "yield_pct" in data
    assert isinstance(data["yield_pct"], float)