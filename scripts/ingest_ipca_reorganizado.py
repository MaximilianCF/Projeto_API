import pandas as pd
from sqlalchemy import create_engine, Column, Float, Date, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Carregar CSV local
try:
    df = pd.read_csv("data/ipca_exemplo.csv", sep=";", encoding="latin1")
    df.columns = ["data", "valor"]
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df = df.dropna()
    print(f"[INFO] CSV carregado com {len(df)} linhas.")
except Exception as e:
    print(f"[ERRO] Falha ao carregar CSV: {e}")
    exit(1)

# 2. Conectar ao banco de dados
try:
    DATABASE_URL = "postgresql://pulso:pulso123@172.18.0.2:5432/pulsodb"
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base = declarative_base()
except Exception as e:
    print(f"[ERRO] Falha ao conectar ao banco: {e}")
    exit(1)

# 3. Modelo da tabela IPCA
class IPCA(Base):
    __tablename__ = "ipca"
    id = Column(Integer, primary_key=True)
    data = Column(Date, unique=True, nullable=False)
    valor = Column(Float, nullable=False)

Base.metadata.create_all(bind=engine)

# 4. Inserir os dados no banco
try:
    for _, row in df.iterrows():
        registro = IPCA(data=row["data"].date(), valor=row["valor"])
        session.merge(registro)
    session.commit()
    print("[OK] Ingestão concluída com sucesso.")
except Exception as e:
    print(f"[ERRO] Durante inserção no banco: {e}")
finally:
    session.close()