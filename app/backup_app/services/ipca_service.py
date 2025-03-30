import requests
import pandas as pd
import openai
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_ipca_data():
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json"
    response = requests.get(url)
    data = response.json()

    df = pd.DataFrame(data)
    df['data'] = pd.to_datetime(df['data'], dayfirst=True)
    df['valor'] = df['valor'].astype(float)
    df.sort_values('data', ascending=False, inplace=True)

    return df.head(3).to_dict(orient='records')


def generate_ipca_analysis(ipca_data):
    prompt = f"""
    Os dados recentes do IPCA são os seguintes:
    {ipca_data}

    Gere uma análise econômica concisa, como se fosse para um investidor que deseja entender rapidamente o que está acontecendo com a inflação no Brasil.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um analista econômico especialista em mercado brasileiro."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=300
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Erro ao gerar análise: {str(e)}"
