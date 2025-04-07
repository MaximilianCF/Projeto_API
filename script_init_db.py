# script init_db.py

from sqlmodel import SQLModel

from app.core.database import engine
from app.core.settings import settings
# Importe os modelos necessários
from app.models.challenge import Challenge
from app.models.user import User

# from app.models.submission import Submission  # adicione outros se necessário

def init_db():
    print(f"🚀 Criando o banco em: {settings.DATABASE_URL}")
    SQLModel.metadata.create_all(engine)
    print("✅ Banco inicializado com sucesso.")

if __name__ == "__main__":
    init_db()
