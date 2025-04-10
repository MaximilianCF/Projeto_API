import httpx
from bs4 import BeautifulSoup


async def fetch_infomoney_headlines():
    url = "https://www.infomoney.com.br/mercados/"
    headers = {"User-Agent": "PulsoBot/1.0"}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
    except httpx.RequestError as e:
        raise RuntimeError(f"Erro ao buscar dados do InfoMoney: {str(e)}")

    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []

    for article in soup.select("div.highlights__list > a"):
        title = article.get_text(strip=True)
        link = article.get("href")
        if title and link:
            headlines.append({
                "titulo": title,
                "url": (
                    link if link.startswith("http")
                    else f"https://www.infomoney.com.br{link}"
                )
            })

    return {"fonte": "InfoMoney", "dados": headlines}
