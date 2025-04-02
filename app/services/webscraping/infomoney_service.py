import requests
from bs4 import BeautifulSoup

def fetch_infomoney_headlines():
    url = "https://www.infomoney.com.br/mercados/"
    headers = {"User-Agent": "PulsoBot/1.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Erro ao buscar dados do InfoMoney: {str(e)}")

    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []

    for article in soup.select("div.highlights__list > a"):
        title = article.get_text(strip=True)
        link = article.get("href")
        if title and link:
            headlines.append({
                "titulo": title,
                "url": link if link.startswith("http") else f"https://www.infomoney.com.br{link}"
            })

    return {
        "fonte": "InfoMoney",
        "dados": headlines
    }
