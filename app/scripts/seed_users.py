import sys
import os

# ✅ Garante que a raiz do projeto esteja no PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from sqlmodel import Session, select
from app.core.database import engine
from app.models.user import User
from passlib.context import CryptContext
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_demo_user():
    with Session(engine) as session:
        existing_user = session.exec(select(User).where(User.username == "usuario_demo")).first()

        if existing_user:
            logger.info("✅ Usuário demo já existe.")
            return

        demo_user = User(
            username="usuario_demo",
            email="demo@pulso.io",
            hashed_password=pwd_context.hash("senha_demo"),
            score=0,
            level="Bronze"
        )
        session.add(demo_user)
        session.commit()
        logger.info("🚀 Usuário demo criado com sucesso!")

if __name__ == "__main__":
    seed_demo_user()
