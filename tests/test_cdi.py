import pytest
import respx
import httpx
from httpx import AsyncClient
from app.main import app
from app.routes.v1.registry import include_v1_routes

include_v1_routes(app)

@pytest.mark.asyncio
async def test_cdi():
    with respx.mock() as mock:
        mock.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados/ultimos/1?formato=json").respond(
            status_code=200,
            json=[{"data": "01/01/2023", "valor": "2,5"}],  # ⬅️ Formato correto da API do BCB
        )
        async with httpx.AsyncClient(app=app, base_url="http://test", follow_redirects=True) as client:
            response = await client.get("/api/v1/cdi")

        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        data = response.json()
        assert data == {"date": "2023-01-01", "value": 2.5}
        assert isinstance(data["value"], float)