import pandas as pd
import requests
from sqlalchemy import create_engine, Column, Float, Date, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from io import BytesIO

# Conexão com o banco (ajuste se mudar as credenciais no docker-compose)
DATABASE_URL = "postgresql://pulso:pulso123@localhost:5432/pulsodb"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class IPCA(Base):
    __tablename__ = "ipca"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date, unique=True, nullable=False)
    valor = Column(Float, nullable=False)

Base.metadata.create_all(bind=engine)

# URL do CSV direto (IPEA IPCA mensal)
csv_url = "https://www.ipeadata.gov.br/ExibeSerie.aspx?serid=38595&module=M"

# Pega o CSV da página convertida (essa parte exige inspeção manual)
raw_url = "https://www.ipeadata.gov.br/ipeaweb.dll/ipeadata?Metodo=obterSerieCSV&CodigoSerie=SGS3653"  # substituto temporário

response = requests.get(raw_url)
df = pd.read_csv("data/ipca_exemplo.csv", sep=";", encoding="latin1")

df.columns = ["data", "valor"]
df["data"] = pd.to_datetime(df["data"], dayfirst=True, errors="coerce")
df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
df = df.dropna()

for _, row in df.iterrows():
    registro = IPCA(data=row["data"].date(), valor=row["valor"])
    session.merge(registro)  # merge evita duplicatas por data
session.commit()
session.close()

print("Ingestão concluída com sucesso.")
