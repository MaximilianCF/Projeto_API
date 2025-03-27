import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_get_cdi():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/cdi")
    assert response.status_code == 200
    data = response.json()
    assert "date" in data
    assert "value" in data
    assert isinstance(data["value"], float)