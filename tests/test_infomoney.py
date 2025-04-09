import pytest
import respx
from httpx import Response, ASGITransport, AsyncClient
from app.main import app

HTML_MOCK = """
<html>
<body>
<div class="highlights__list">
    <a href="/mercados/noticia-1">Notícia 1</a>
    <a href="/mercados/noticia-2">Notícia 2</a>
</div>
</body>
</html>
"""

@pytest.mark.asyncio
@respx.mock
async def test_infomoney_scraping():
    respx.get("https://www.infomoney.com.br/mercados/").mock(
        return_value=Response(200, text=HTML_MOCK)
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/webscraping/infomoney")

    assert response.status_code == 200
    data = response.json()
    assert data["fonte"] == "InfoMoney"
    assert isinstance(data["dados"], list)
    assert data["dados"][0]["titulo"] == "Notícia 1"
