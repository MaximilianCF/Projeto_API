# tests/test_ipca.py

import pytest
import httpx
import respx
from httpx import AsyncClient
from app.main import app
from app.routes.v1.registry import include_v1_routes

include_v1_routes(app)

@pytest.mark.asyncio
async def test_ipca_ok():
    with respx.mock() as mock:
        mock.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json").respond(
            status_code=200,
            json=[{"data": "01/03/2025", "valor": "4,12"}],
        )
        async with httpx.AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/v1/ipca")
        
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        data = response.json()
        assert data["indicador"] == "IPCA"
        assert data["valor"] == 4.12
        assert data["data"] == "01/03/2025"
        assert isinstance(data["valor"], float)
    