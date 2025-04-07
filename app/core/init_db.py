import asyncio
import logging
from sqlmodel import SQLModel, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import engine, AsyncSessionLocal
from app.models.user import User
from app.core.security import get_password_hash
from app.core import settings

# Importa os modelos para registrar no metadata
from app.models import (
    cdi, challenge, ibov, indicator_metadata, ipca, leaderboard,
    selic, sp500, submission, treasury, usd_brl
)

# Configura o logger
logger = logging.getLogger("init_db")
logger.setLevel(logging.INFO)

DATABASE_URL = "postgresql+asyncpg://pulso:pulso123@localhost:5432/pulsodb"

async def init_db():
    logger.info(f"🔌 Conectando ao banco de dados: {DATABASE_URL}")

    # Cria as tabelas de forma assíncrona
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    logger.info("🗂️ Tabelas criadas com sucesso.")

    # Verifica e cria o usuário admin, se necessário
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).limit(1))
        user_exists = result.first()

        if not user_exists:
            admin = User(
                username="pulso",
                email="admin@admin.com",
                hashed_password=get_password_hash("pulso123"),
                score=0,
                level="iniciante",
            )
            session.add(admin)
            await session.commit()
            logger.info("✅ Usuário admin criado.")
        else:
            logger.info("ℹ️ Usuário admin já existe.")

    logger.info("🎉 Banco de dados pronto para uso.")


if __name__ == "__main__":
    asyncio.run(init_db())
