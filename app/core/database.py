from sqlmodel import SQLModel, create_engine, Session
import os

# 🔐 Caminho do banco (usando SQLite local por padrão)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pulso.db")

# ⚙️ Engine de conexão
engine = create_engine(
    DATABASE_URL,
    echo=True  # loga as queries no terminal (pode remover depois)
)

# 🔁 Função para criar as tabelas com base nos modelos
def create_db_and_tables():
    from app.models.user import User
    from app.models.challenge import Challenge
    from app.models.submission import Submission

    SQLModel.metadata.create_all(engine)

# 🧪 Session para uso em endpoints
def get_session():
    with Session(engine) as session:
        yield session
