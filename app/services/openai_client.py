import openai
import datetime
from dotenv import load_dotenv

openai.api_key = "SUA_API_KEY_AQUI"  # Recomendado usar .env

def gerar_codigo_analise(ticker: str) -> str:
    hoje = datetime.date.today().strftime("%Y-%m-%d")
    prompt = f"""
    Você é um analista quantitativo. Gere um código Python que:
    1. Use yfinance
    2. Baixe os preços da ação {ticker} desde o início do mês até {hoje}
    3. Plote gráfico de linha
    4. Calcule variação percentual
    Apenas retorne o código, sem explicações.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message["content"]