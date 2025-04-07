import httpx
import pytest
import respx
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_cdi():
    with respx.mock():
        respx.get("http://test/api/v1/cdi").mock(
            return_value=httpx.Response(200, json={"date": "2023-01-01", "value": 2.5})
        )

        async with AsyncClient(
            base_url="http://test",
            app=app,
            follow_redirects=True
        ) as client:
            response = await client.get("/api/v1/cdi")

        assert response.status_code == 200
        data = response.json()
        assert data == {"date": "2023-01-01", "value": 2.5}
        assert isinstance(data["value"], float)
